import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAI3YFnFiW9r3CVYONXX9Jb3nJUync6Qhc')

# Geocoding an address
geocode_result = gmaps.geocode('Cruzeiro, Belo Horizonte')

lat = geocode_result[0]["geometry"]["location"]["lat"]
lon = geocode_result[0]["geometry"]["location"]["lng"]

