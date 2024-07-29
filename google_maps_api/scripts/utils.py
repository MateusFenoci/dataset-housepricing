import googlemaps
import csv
import time





def get_features(api_key,lat,long,radius):

    # List with the points of interest for the house pricing
    keypoints = [
    'accounting', 'airport', 'amusement_park', 'art_gallery', 'atm', 'bakery',
    'bank', 'bar', 'beauty_salon', 'bus_station',
    'cafe', 'car_repair', 'car_wash', 'church', 'clothing_store', 'convenience_store', 'dentist', 'department_store',
    'doctor', 'electrician', 'electronics_store', 'fire_station',
    'furniture_store', 'gas_station', 'gym', 'hair_care', 'hardware_store', 'health',
    'home_goods_store', 'hospital', 'insurance_agency', 'jewelry_store', 'laundry', 'lawyer',
    'library', 'liquor_store', 'lodging', 'meal_delivery',
    'meal_takeaway', 'movie_theater', 'moving_company', 'museum',
    'night_club', 'painter', 'park', 'parking', 'pet_store', 'pharmacy', 'physiotherapist',
    'plumber', 'police', 'post_office', 'real_estate_agency', 'restaurant',
    'school', 'shoe_store', 'shopping_mall', 'spa', 'stadium', 'store', 'subway_station',
    'supermarket', 'taxi_stand', 'train_station', 'university',
    'veterinary_care'
    ]

    gmaps = googlemaps.Client(key=api_key)

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





if __name__ == "__main__":
    key = 'AIzaSyAI3YFnFiW9r3CVYONXX9Jb3nJUync6Qhc'
    # Ibmec BH latitude and longitude
    latitude = -19.92864689130775  
    longitude = -43.93039249888748  
    radius = 100  
    print(get_features(key,latitude,longitude,radius))