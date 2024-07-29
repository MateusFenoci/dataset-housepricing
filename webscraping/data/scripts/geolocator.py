import googlemaps


def get_cordinates(adress,api_key):
    gmaps = googlemaps.Client(key=api_key)

    # Geocoding an address
    geocode_result = gmaps.geocode(adress)

    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]

    return lat,lon
