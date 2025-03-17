from geopy.geocoders import Nominatim


def get_coordinates(address):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(address)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None


# Пример использования
address = "Норильск Озёрная 13"
latitude, longitude = get_coordinates(address)

if latitude and longitude:
    print(f"Широта: {latitude}, Долгота: {longitude}")
else:
    print("Адрес не найден.")