import asyncio
import json
import time
from parser7 import get_pet_ids_from_map, parse_pet_details

# Читаем параметр интервала обновления из конфигурационного файла
CONFIG_FILE = "config.json"


def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config.get("update_interval", 300)  # По умолчанию 5 минут
    except FileNotFoundError:
        print("Файл конфигурации не найден. Используется значение по умолчанию (300 сек).")
        return 300
    except json.JSONDecodeError:
        print("Ошибка чтения config.json. Используется значение по умолчанию (300 сек).")
        return 300


async def save_to_database(pet_data):
    """
    Здесь должен быть код для сохранения данных в базу данных.

    """
    print(f"Данные питомца {pet_data['name'] or pet_data['id']} сохранены в базу данных (заглушка).")


async def fetch_and_store_pets():
    while True:
        print("Запуск обновления данных...")
        pet_ids = await get_pet_ids_from_map()

        for pet_id in pet_ids:
            pet_data = await parse_pet_details(pet_id)
            await save_to_database(pet_data)

        interval = load_config()
        print(f"Ожидание {interval} секунд перед следующим обновлением...")
        time.sleep(interval)  # Пауза перед следующим циклом


if __name__ == "__main__":
    asyncio.run(fetch_and_store_pets())