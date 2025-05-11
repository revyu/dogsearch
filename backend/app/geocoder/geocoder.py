from geopy.geocoders import Nominatim

def geocode(address):
    geolocator = Nominatim(user_agent="myGeocoder")
    return geolocator.geocode(address, addressdetails=True)

def extract_region(location) -> str | None:
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