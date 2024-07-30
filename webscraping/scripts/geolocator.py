import googlemaps

def get_coordinates(address, api_key):
    """
    Obtém as coordenadas (latitude e longitude) de um endereço usando a API do Google Maps.

    :param address: Endereço a ser geocodificado
    :param api_key: Chave da API do Google Maps
    :return: Tupla com latitude e longitude
    """
    gmaps = googlemaps.Client(key=api_key)
    geocode_result = gmaps.geocode(address)
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]
    return latitude, longitude
