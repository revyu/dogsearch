import asyncpg
import asyncio
import os
import sys
from dotenv import load_dotenv

# Добавляем корневую директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.services.parser import get_pet_ids_from_map, parse_pet_details

load_dotenv()

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
        await conn.execute("""
            INSERT INTO pets (
                pet_id, name, gender, descriptions, 
                images, address
            ) VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (pet_id) DO UPDATE SET
                name = $2,
                gender = $3,
                descriptions = $4,
                images = $5,
                address = $6
                
        """, 
        pet_data["id"],
        pet_data["name"],
        pet_data["gender"],
        pet_data["descriptions"],
        pet_data["images"],
        pet_data["address"])
        
        return True
    except Exception as e:
        print(f"Ошибка при обработке питомца {pet_data['id']}: {str(e)}")
        return False

async def main():
    # Добавляем инициализацию базы данных
    conn = await get_db_connection()
    try:
       
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                pet_id TEXT PRIMARY KEY,
                name TEXT,
                gender TEXT,
                descriptions TEXT[],
                images TEXT[],
                address TEXT
            )
        """)
        
        # Остальной код main()...
        pet_ids = await get_pet_ids_from_map()
        total_pets = len(pet_ids)
        print(f"Всего найдено питомцев: {total_pets}")
        
        num_pets = min(10, total_pets)  # Обрабатываем первые 5 питомцев
        print(f"Будет обработано питомцев: {num_pets}")
        
        success_count = 0
        for i, pet_id in enumerate(pet_ids[:num_pets], 1):
            print(f"Обработка питомца {i}/{num_pets} (ID: {pet_id})")
            pet_data = await parse_pet_details(pet_id)
            if await process_pet(conn, pet_data):
                success_count += 1
                
        print("\nПарсинг завершен!")
        print(f"Успешно обработано: {success_count} из {num_pets} питомцев")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main()) 