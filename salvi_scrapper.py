import requests
import os
import pandas as pd



API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
if not API_KEY:
    raise ValueError("Please set your GOOGLE_PLACES_API_KEY environment variable")

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

params = {
    'key': API_KEY,
    'location': '34.052235,-118.243683',
    'radius': 50000,
}

keywords = ['salvadoran', 'pupusas', 'pupuseria', 'salvadorean']
all_places = {}


try:
    for keyword in keywords:
        params['keyword'] = keyword
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != 'OK':
            continue
            
        for place in data['results']:
            place_id = place.get('place_id')
            if place_id not in all_places:
                all_places[place_id] = place
    
    # Create DataFrame
    restaurants_data = []
    for place in all_places.values():
        restaurants_data.append({
            'place_id': place.get('place_id', ''),
            'name': place['name'],
            'rating': place.get('rating', None),
            'latitude': place.get('geometry', {}).get('location', {}).get('lat', None),
            'longitude': place.get('geometry', {}).get('location', {}).get('lng', None),
            'vicinity': place.get('vicinity', ''),
        })
    
    df = pd.DataFrame(restaurants_data)
    print(f"Found {len(df)} unique Salvadoran restaurants")
    
    df.to_csv("salvadoran_restaurants.csv", index=False)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")