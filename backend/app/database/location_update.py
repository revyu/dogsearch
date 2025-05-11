import asyncpg
import asyncio
import os
import sys
from dotenv import load_dotenv
from app.database.db import get_db_connection, close_db_connection
from app.services.geocoder import geocode

# Добавляем корневую директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
load_dotenv()

def extract_region_geocode(location) -> str | None:
    if not location or not hasattr(location, "raw"):
        return None

    address = location.raw.get("address")
    if not address:
        return None

    country = address.get("country")
    city = (
        address.get("city") or
        address.get("town") or
        address.get("village") or
        address.get("municipality") or
        address.get("locality") or
        address.get("hamlet")
    )

    if country and city:
        return f"{country}, {city}"
    elif country:
        return country
    elif city:
        return city
    else:
        return None

def standardize_address(location) -> str:
    # Извлекаем компоненты из location.raw["address"]
    address_info = location.raw.get("address", {})

    # Стандартизируем компоненты адреса
    standardized_address = []

    # Сначала страна
    if "country" in address_info:
        standardized_address.append(address_info['country'])

    # Затем город (если есть)
    if "city" in address_info:
        standardized_address.append(f"г. {address_info['city']}")
    elif "town" in address_info:
        standardized_address.append(f"г. {address_info['town']}")
    elif "village" in address_info:
        standardized_address.append(f"с. {address_info['village']}")

    # Улица и номер дома
    if "road" in address_info:
        standardized_address.append(f"ул. {address_info['road']}")
    if "house_number" in address_info:
        standardized_address.append(f"д. {address_info['house_number']}")

    # Формируем и возвращаем стандартизированный адрес
    return ', '.join(standardized_address)

async def update_locations(conn, address_id):

    print(f"Processing {address_id}")
    try:
        address = await conn.fetchrow("""
            SELECT addr_text
            FROM addresses
            WHERE address_id = $1
        """, address_id)

        if not address:
            raise Exception(f"An address with address_id: {address_id} does not exist!")
        address_text = address["addr_text"]

        location = geocode(address_text)
        if not location:
            return

        reg_id = None
        region_name = extract_region_geocode(location)
        if not region_name:
            raise Exception(f"Cannot extract region from '{address_text}'")

        region = await conn.fetchrow("""
            SELECT region_id
            FROM regions
            WHERE reg_text = $1
        """, region_name)

        if region:
            reg_id = region["region_id"]
        else:
            reg_id = (await conn.fetchrow("""
                INSERT INTO regions (reg_text)
                VALUES ($1)
                RETURNING region_id
            """, region_name))["region_id"]

        await conn.execute("""
            UPDATE addresses
            SET
                latitude = $2,
                longitude = $3,
                addr_text = $4,
                region_id = $5
            WHERE 
                address_id = $1
        """, address_id, location.latitude, location.longitude, standardize_address(location), reg_id)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def main():
    conn = await get_db_connection()
    rows = await conn.fetch("""SELECT address_id FROM addresses""")
    print(rows)
    for row in rows:
        await update_locations(conn, row["address_id"])

    await close_db_connection(conn)


if __name__ == "__main__":
    asyncio.run(main())