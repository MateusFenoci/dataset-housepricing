import googlemaps
from .api_key import key

def get_lat_lon(endereco):
    gmaps = googlemaps.Client(key=key)
    geocode_result = gmaps.geocode(endereco)
    if not geocode_result:
        raise ValueError('Endereço não encontrado')
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    return lat, lon

def get_features(lat,long,radius=500):

    # List with the points of interest for the house pricing
    keypoints = [
    'school',             # Escolas
    'hospital',           # Hospitais
    'supermarket',        # Supermercados
    'subway_station',     # Estações de metrô
    'train_station',      # Estações de trem
    'bus_station',        # Estações de ônibus
    'park',               # Parques
    'restaurant',         # Restaurantes
    'shopping_mall',      # Shopping centers
    'gym',                # Academias
    'police',             # Delegacias de polícia
    'university',         # Universidades
    'doctor',             # Médicos
    'parking',            # Estacionamento
    'pet_store',          # Pet shop
    'car_repair',         # Oficinas de reparação de automóveis
    'atm',                # Caixas eletrônicos
    'cafe',               # Cafés
]

    gmaps = googlemaps.Client(key=key)

    # Dictionary to store the number of points of interest
    keypoint_counts = {points_of_interest: 0 for points_of_interest in keypoints}

    # Iterate through each point of interest
    for place_type in keypoints:
        try:
            # Perform a nearby search with the point of interest filter
            places_result = gmaps.places_nearby(location=(lat, long), radius=radius, type=place_type)
            
            # Count the number of points of interest
            keypoint_count = len(places_result.get('results', []))
            keypoint_counts[place_type] = keypoint_count
            
            # Sleep to handle API rate limits 30.000 request per minute
            #time.sleep(0.1)  

        # Handle exceptions
        except googlemaps.exceptions.ApiError as e:
            print(f"API error for type '{place_type}': {e}")
        except Exception as e:
            print(f"Unexpected error for type '{place_type}': {e}")
            
    return keypoint_counts




