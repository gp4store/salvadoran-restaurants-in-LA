import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
if not API_KEY:
    raise ValueError("Please set your GOOGLE_PLACES_API_KEY environment variable")

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

try:
    la_areas = [
        ('Downtown LA', '34.052235,-118.243683'),
        ('Hollywood', '34.0928,-118.3287'),
        ('Beverly Hills', '34.0736,-118.4004'),
        ('Santa Monica', '34.0195,-118.4912'),
        ('Pasadena', '34.1478,-118.1445'),
        ('Long Beach', '33.7701,-118.1937'),
        ('Glendale', '34.1425,-118.2551'),
        ('Burbank', '34.1808,-118.3090'),
        ('Koreatown', '34.0579,-118.3009'),
        ('East LA', '34.0239,-118.1817'),
    ]

    keywords = ['salvadoran', 'pupusas', 'pupuseria', 'salvadorean']
    all_places = {}

    for area_name, location in la_areas:
        print(f"Searching {area_name}...")
        
        for keyword in keywords:
            params = {
                'key': API_KEY,
                'location': location,
                'radius': 10000,  # 10km radius per area
                'keyword': keyword
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            print(f"  {keyword}: {data.get('status')} - {len(data.get('results', []))} results")
            
            if data['status'] != 'OK':
                if data['status'] == 'REQUEST_DENIED':
                    print(f"  ERROR: {data.get('error_message', 'Request denied')}")
                continue
                
            for place in data['results']:
                place_id = place.get('place_id')
                if place_id not in all_places:
                    all_places[place_id] = place

    print(f"\nTotal unique places found: {len(all_places)}")

    # Create DataFrame AFTER collecting all results
    if all_places:
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
        
        # Save to CSV
        df.to_csv("salvadoran_restaurants.csv", index=False)
        print("Data saved to 'salvadoran_restaurants.csv'")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except Exception as e:
    print(f"Error: {e}")