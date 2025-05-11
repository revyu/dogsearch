import asyncpg
import asyncio
import os
import sys
from dotenv import load_dotenv
from app.database.db import get_db_connection, close_db_connection
from app.geocoder.geocoder import geocode, extract_region, standardize_address

# Добавляем корневую директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
load_dotenv()

# __________________________________________________________________________________
# Мини-сервер, который асинхронно обрабатывает адрес добавленного питомца.
# 1) Использует геокодер для определения широты, долготы и региона
# 1) Выполняет вставки в таблицы addresses и regions, избегая избыточных записей
# __________________________________________________________________________________

# Обновляет адрес питомцу
async def update_pet(conn, pet_id, address_id):
    await conn.execute("""
        UPDATE pets
        SET address_id = $2
        WHERE pet_id = $1
    """, pet_id, address_id)

# Добавляет адрес в базу данных
async def append_address(conn, pet_id, address):
    location = geocode(address)

    try:
        # Если не получена геолокация, добавляем "пустышку" (status = 0)
        if not location:
            address_id = await conn.fetchrow("""
                INSERT INTO addresses (addr_text)
                VALUES ($1)
                RETURNING address_id
            """, address)
            await update_pet(conn, pet_id, address_id)
            print("Адрес неразрешим (добавлен без геолокации)")
            return True

        # Проверяем на наличие этого адреса в базе данных
        address_text = standardize_address(location)
        match_ = await conn.fetchrow("""
            SELECT address_id
            FROM addresses
            WHERE addr_text = $1
        """, address_text)

        # Если такой адрес уже есть, обновляем питомца
        if match_:
            await update_pet(conn, pet_id, match_["address_id"])
            return True

        # Проверяем на наличие региона в базе данных
        region_text = extract_region(location)
        match_ = await conn.fetchrow("""
            SELECT region_id
            FROM regions
            WHERE reg_text = $1
        """, region_text)

        # Если такой регион уже есть, берём его ID
        if match_:
            region_id = match_["region_id"]
        # Иначе - добавляем новый регион
        else:
            region_id = (await conn.fetchrow("""
                INSERT INTO regions (reg_text)
                VALUES ($1)
                RETURNING region_id
            """, region_text))["region_id"]

        # Добавляем новый адрес с ассоциированным регионом
        address_id = (await conn.fetchrow("""
            INSERT INTO addresses (addr_text, region_id, latitude, longitude, status)
            VALUES ($1, $2, $3, $4, 1)
            RETURNING address_id
        """, address_text, region_id, location.latitude, location.longitude))["address_id"]

        # Обновляем питомца
        await update_pet(conn, pet_id, address_id)
        return True

    except Exception as e:
        print(f"Возникла ошибка при обработке адреса: {str(e)}")
        return False



# Очередь для хранения значений
queue = asyncio.Queue()

# Хэндлер для обработки запроса клиента
async def client_handler(reader, writer):
    try:
        # Чтение данных от клиента
        data = await reader.read(100)
        message = data.decode()
        # Ожидаем получить строку и число, разделённые пробелом
        pet_id, address = message.split(maxsplit=1)
        # Добавляем пару в очередь
        await queue.put((pet_id, address))
        # Отправляем подтверждение клиенту
        writer.write("Данные добавлены в очередь\n".encode())
        await writer.drain()
    except Exception as e:
        writer.write(f"Ошибка: {e}\n".encode())
        await writer.drain()
    finally:
        writer.close()



# Функция обработки очереди
async def process_queue(conn):
    while True:
        if not queue.empty():
            # Получаем элемент из очереди
            pet_id, address = await queue.get()

            print(f"Обрабатываем: {pet_id} - {address}")
            await append_address(conn, pet_id, address)

            # После обработки сообщения помечаем задачу как завершенную
            queue.task_done()

        # Задержка, чтобы не блокировать выполнение
        await asyncio.sleep(1)

# Основная функция для запуска сервера
async def main():
    conn = await get_db_connection()
    # Запуск процесса обработки очереди
    asyncio.create_task(process_queue(conn))

    # Создание TCP-сервера
    server = await asyncio.start_server(client_handler, os.getenv("GEOCODER_SERVER_URL"), os.getenv("GEOCODER_SERVER_PORT"))

    addr = server.sockets[0].getsockname()
    print(f"Сервер запущен на {addr}")

    # Ожидание завершения работы сервера
    async with server:
        await server.serve_forever()
    await close_db_connection(conn)

# Запуск основного асинхронного цикла
if __name__ == "__main__":
    asyncio.run(main())