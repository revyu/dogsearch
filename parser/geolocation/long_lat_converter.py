import requests

VK_ACCESS_TOKEN = "your_access_token"
API_VERSION = "5.131"


def get_lat_lon_vk(address):
    url = "https://api.vk.com/method/maps.search"
    params = {
        "q": address,
        "v": API_VERSION,
        "access_token": VK_ACCESS_TOKEN
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        # Достаем первую найденную точку
        place = data["response"]["places"]["items"][0]
        lat, lon = place["latitude"], place["longitude"]
        return lat, lon
    except (KeyError, IndexError):
        return None, None


# Тест запроса
address = "Москва, Красная площадь, 1"
latitude, longitude = get_lat_lon_vk(address)

print(f"Широта: {latitude}, Долгота: {longitude}")
