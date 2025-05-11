import asyncpg
import asyncio
import os
import sys
from dotenv import load_dotenv

# Добавляем корневую директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.services.parser import get_pet_ids_from_map, parse_pet_details
load_dotenv()



# Клиентский метод запроса на обработку адреса для питомца _________________________
async def address_append_request(pet_id, address):
    # Создаем подключение к серверу
    reader, writer = await asyncio.open_connection(os.getenv("GEOCODER_SERVER_URL"), os.getenv("GEOCODER_SERVER_PORT"))
    # Формируем сообщение для отправки
    message = f"{pet_id} {address}"
    # Отправляем сообщение на сервер
    writer.write(message.encode())
    await writer.drain()
    # Закрываем соединение
    writer.close()
    await writer.wait_closed()
# __________________________________________________________________________________



async def get_db_connection():
    return await asyncpg.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST')
    )

async def close_db_connection(connection):
    await connection.close()

async def process_pet(conn, pet_data):
    try:
        # Отладочная информация
        print(f"\nОбработка питомца:")
        print(f"ID: {pet_data['id']}")
        print(f"Телефон владельца: {pet_data.get('owner_phone')}")

        # Сначала обрабатываем пользователя (владельца)
        user_id = None
        if pet_data.get("owner_phone"):  # Используем .get() для безопасного получения
            print(f"Найден телефон: {pet_data['owner_phone']}")
            
            # Проверяем, существует ли пользователь
            user = await conn.fetchrow("""
                SELECT id FROM users 
                WHERE phone = $1
            """, pet_data["owner_phone"])
            
            if user:
                print(f"Найден существующий пользователь с ID: {user['id']}")
                user_id = user['id']
            else:
                print("Создаем нового пользователя...")
                # Создаем нового пользователя
                try:
                    user = await conn.fetchrow("""
                        INSERT INTO users (phone, created_at) 
                        VALUES ($1, CURRENT_TIMESTAMP)
                        RETURNING id
                    """, pet_data["owner_phone"])
                    user_id = user['id']
                    print(f"Создан новый пользователь с ID: {user_id}")
                except Exception as e:
                    print(f"Ошибка при создании пользователя: {str(e)}")
        else:
            print("Телефон владельца не указан")


        # Добавляем питомца
        print(f"Добавляем питомца с user_id: {user_id}")

        await conn.execute("""
            INSERT INTO pets (
                pet_id, name, gender, descriptions, 
                images, user_id
            ) VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (pet_id) DO UPDATE SET
                name = $2,
                gender = $3,
                descriptions = $4,
                images = $5,
                user_id = $6
        """, 
        pet_data["id"],
        pet_data["name"],
        pet_data["gender"],
        pet_data["descriptions"],
        pet_data["images"],
        user_id)
        
        print("Питомец успешно добавлен/обновлен")

        await address_append_request(pet_data["id"], pet_data["address"])
        return True
    except Exception as e:
        print(f"Ошибка при обработке питомца {pet_data['id']}: {str(e)}")
        return False

async def main():
    conn = await get_db_connection()
    try:
        # 1. Создаем таблицы если их нет
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                vk_id INTEGER,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                phone VARCHAR(20) UNIQUE  -- Добавляем UNIQUE для телефона
            )
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                pet_id TEXT PRIMARY KEY,
                name TEXT,
                gender TEXT,
                descriptions TEXT[],
                images TEXT[],
                address TEXT,
                user_id INTEGER REFERENCES users(id)
            )
        """)
        
        # 2. Получаем список питомцев
        pet_ids = await get_pet_ids_from_map()
        total_pets = len(pet_ids)
        print(f"Всего найдено питомцев: {total_pets}")
        
        # 3. Определяем количество питомцев для обработки
        try:
            num_pets = int(input(f"Введите количество питомцев для парсинга (максимум {total_pets}): "))
            num_pets = min(num_pets, total_pets)
        except ValueError:
            print("Неверный ввод. Будет обработано 10 питомцев.")
            num_pets = 10
        
        # 4. Обрабатываем питомцев
        success_count = 0
        for i, pet_id in enumerate(pet_ids[:num_pets], 1):
            print(f"\nОбработка питомца {i}/{num_pets} (ID: {pet_id})")
            
            # Создаем новое соединение для каждого питомца
            if conn.is_closed():
                conn = await get_db_connection()
                
            try:
                pet_data = await parse_pet_details(pet_id)
                if pet_data and await process_pet(conn, pet_data):
                    success_count += 1
            except Exception as e:
                print(f"Ошибка при обработке питомца {pet_id}: {str(e)}")
                # Пересоздаем соединение при ошибке
                if not conn.is_closed():
                    await conn.close()
                conn = await get_db_connection()
                
        print("\nПарсинг завершен!")
        print(f"Успешно обработано: {success_count} из {num_pets} питомцев")
        
    finally:
        if not conn.is_closed():
            await conn.close()

if __name__ == "__main__":
    asyncio.run(main()) 