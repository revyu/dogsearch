import asyncpg
import os
import asyncio
import sys
import math
from dotenv import load_dotenv
from app.services.geocoder import GetCoordinates
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
load_dotenv()

async def ConnectDB():
    return await asyncpg.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST')
    )


def HaversineDistance(lat1, lon1, lat2, lon2):
    """
    Вычисляет расстояние между двумя точками по формуле гаверсинуса (в километрах).
    """
    R = 6371  # Радиус Земли в километрах

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# Просто добавляет в бд информацию о координатах
async def UpdateGeolocation():
    conn = await ConnectDB()
    try:
        query = '''
            SELECT 
                address_text
            FROM 
                addresses
                    '''
        rows = await conn.fetch(query)
        result = [dict(row) for row in rows]

    finally:
        await conn.close()

    for row in result:
        latitude, longitude = GetCoordinates(row["address_text"])
        conn = await ConnectDB()
        try:
            query = '''
                    UPDATE addresses
                    SET latitude = $1, longitude = $2
                    WHERE address_text = $3
                '''
            await conn.execute(query, latitude, longitude, row["address_text"])
        finally:
            await conn.close()


async def FetchPets():
    conn = await ConnectDB()
    try:
        query = '''
            SELECT 
                p.pet_id, 
                a.latitude, 
                a.longitude
            FROM 
                pets p
            JOIN 
                addresses a ON p.address = a.address_text
        '''
        rows = await conn.fetch(query)
        result = [dict(row) for row in rows]
        return result
    finally:
        await conn.close()

async def FilterPetsByDistance(user_lat, user_lon, max_distance_km, pets):
    """
    Фильтрует питомцев, оставляя только тех, кто в пределах max_distance_km от пользователя.
    Возвращает список pet_id.
    """
    pet_ids = []
    for pet in pets:
        distance = HaversineDistance(
            user_lat,
            user_lon,
            pet['latitude'],
            pet['longitude']
        )
        if distance <= max_distance_km:
            pet_ids.append(pet['pet_id'])
    return pet_ids

async def main():
    pets_with_location = await FetchPets()
    for pet in pets_with_location:
        print(pet)




if __name__ == "__main__":
    asyncio.run(main())