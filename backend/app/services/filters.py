import asyncpg
import os
import asyncio
import sys
import math
from dotenv import load_dotenv
from app.services.geocoder import geocode
from app.database.db import get_db_connection, close_db_connection

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
load_dotenv()

#
#
#
# class LocationOption:
#     def __int__(self, latitude, longitude, radius):
#         self.latitude = latitude
#         self.longitude = longitude
#         self.radius = radius
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# async def describe_table(table_name: str):
#     conn = await get_db_connection()
#     try:
#         query = '''
#             SELECT column_name, data_type, is_nullable
#             FROM information_schema.columns
#             WHERE table_name = $1
#         '''
#         rows = await conn.fetch(query, table_name)
#         for row in rows:
#             print(f"{row['column_name']} | {row['data_type']} | Nullable: {row['is_nullable']}")
#     finally:
#         await close_db_connection(conn);
#
#
#
#
# def HaversineDistance(lat1, lon1, lat2, lon2):
#     """
#     Вычисляет расстояние между двумя точками по формуле гаверсинуса (в километрах).
#     """
#     R = 6371  # Радиус Земли в километрах
#
#     phi1 = math.radians(lat1)
#     phi2 = math.radians(lat2)
#     delta_phi = math.radians(lat2 - lat1)
#     delta_lambda = math.radians(lon2 - lon1)
#
#     a = math.sin(delta_phi / 2) ** 2 + \
#         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
#
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#
#     return R * c
#
# # Просто добавляет в бд информацию о координатах
# async def UpdateGeolocation():
#     conn = await get_db_connection()
#     try:
#         query = '''
#             SELECT
#                 address_text
#             FROM
#                 addresses
#                     '''
#         rows = await conn.fetch(query)
#         result = [dict(row) for row in rows]
#
#     finally:
#         await close_db_connection(conn)
#
#     for row in result:
#         latitude, longitude = GetCoordinates(row["address_text"])
#         conn = await get_db_connection()
#         try:
#             query = '''
#                     UPDATE addresses
#                     SET latitude = $1, longitude = $2
#                     WHERE address_text = $3
#                 '''
#             await conn.execute(query, latitude, longitude, row["address_text"])
#         finally:
#             await conn.close()
#
#
# async def FetchPets():
#     conn = await get_db_connection()
#     try:
#         query = '''
#             SELECT
#                 p.pet_id,
#                 a.latitude,
#                 a.longitude
#             FROM
#                 pets p
#             JOIN
#                 addresses a ON p.address = a.address_text
#         '''
#         rows = await conn.fetch(query)
#         result = [dict(row) for row in rows]
#         return result
#     finally:
#         await close_db_connection(conn)
#
# async def FilterPetsByDistance(user_lat, user_lon, max_distance_km, pets):
#     """
#     Фильтрует питомцев, оставляя только тех, кто в пределах max_distance_km от пользователя.
#     Возвращает список pet_id.
#     """
#     pet_ids = []
#     for pet in pets:
#         distance = HaversineDistance(
#             user_lat,
#             user_lon,
#             pet['latitude'],
#             pet['longitude']
#         )
#         if distance <= max_distance_km:
#             pet_ids.append(pet['pet_id'])
#     return pet_ids

async def describe_database():
    conn = await get_db_connection()
    try:
        # Получаем все таблицы в public-схеме
        tables_query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """
        tables = await conn.fetch(tables_query)

        for table_row in tables:
            table_name = table_row['table_name']
            print(f"\n📦 Таблица: {table_name}")

            # Получаем столбцы таблицы
            columns_query = """
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = $1
                ORDER BY ordinal_position;
            """
            columns = await conn.fetch(columns_query, table_name)
            for col in columns:
                print(f"  🧩 {col['column_name']} | {col['data_type']} | Nullable: {col['is_nullable']}")

            # Получаем внешние ключи
            fkeys_query = """
                SELECT
                    kcu.column_name,
                    ccu.table_name AS foreign_table,
                    ccu.column_name AS foreign_column
                FROM
                    information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_name = kcu.table_name
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_name = $1;
            """
            fkeys = await conn.fetch(fkeys_query, table_name)
            for fk in fkeys:
                print(f"  🔗 FK: {fk['column_name']} → {fk['foreign_table']}.{fk['foreign_column']}")

            # Получаем последовательности, связанные с таблицей
            sequences_query = """
                SELECT
                    s.relname AS sequence_name,
                    a.attname AS column_name
                FROM
                    pg_class s
                    JOIN pg_depend d ON d.objid = s.oid
                    JOIN pg_class t ON d.refobjid = t.oid
                    JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = d.refobjsubid
                WHERE
                    s.relkind = 'S'
                    AND t.relname = $1;
            """
            sequences = await conn.fetch(sequences_query, table_name)
            for seq in sequences:
                print(f"  🔢 Sequence: {seq['sequence_name']} → column {seq['column_name']}")

    finally:
        await conn.close()


async def print_all_rows_from_table(table_name: str):
    conn = await get_db_connection()
    try:
        # Экранируем имя таблицы (безопасно, но без SQL-инъекций всё равно не используем пользовательский ввод напрямую)
        query = f'SELECT * FROM "{table_name}"'
        rows = await conn.fetch(query)
        if not rows:
            print(f"\n📦 Таблица: {table_name} пуста.")
            return
        print(f"\n📦 Таблица: {table_name} содержит {len(rows)} строк:")
        for row in rows:
            print("  ", dict(row))
    except Exception as e:
        print(f"⚠ Ошибка при получении данных из {table_name}: {e}")
    finally:
        await conn.close()


async def delete_all_rows_from_table(table_name: str):
    conn = await get_db_connection()
    try:
        # Экранируем имя таблицы для предотвращения SQL-инъекций
        query = f'DELETE FROM "{table_name}"'
        result = await conn.execute(query)
        print(f"\n✅ Все строки из таблицы {table_name} были удалены.")
    except Exception as e:
        print(f"⚠ Ошибка при удалении данных из {table_name}: {e}")
    finally:
        await conn.close()


async def main():
    # await delete_all_rows_from_table("pets")
    # await delete_all_rows_from_table("addresses")
    # await delete_all_rows_from_table("users")
    # await delete_all_rows_from_table("regions")

    await print_all_rows_from_table("pets")
    await print_all_rows_from_table("addresses")
    await print_all_rows_from_table("users")
    await print_all_rows_from_table("regions")




if __name__ == "__main__":
    asyncio.run(main())