import pandas as pd
from scripts.utils import  get_features
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAmEJLxvcZ0jxyJ3gqn60L6T-2l37WFQXg')

# Geocoding an address
geocode_result = gmaps.geocode('Rua alfenas, Cruzeiro, Belo Horizonte')

lat = geocode_result[0]["geometry"]["location"]["lat"]
lon = geocode_result[0]["geometry"]["location"]["lng"]

info = pd.DataFrame([get_features(lat,lon,500)])

info.to_csv(f"teste.csv",mode = "w", header=False ,index=False)
print(info.head)
        
    