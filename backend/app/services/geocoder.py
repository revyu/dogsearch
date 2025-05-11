from geopy.geocoders import Nominatim




def geocode(address):
    geolocator = Nominatim(user_agent="myGeocoder")
    return geolocator.geocode(address, addressdetails=True)