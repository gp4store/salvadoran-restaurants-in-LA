import requests
import os
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
if not API_KEY:
    raise ValueError("Please set your GOOGLE_PLACES_API_KEY environment variable")

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

def get_all_results(url, params):
    """Get all results using pagination (up to 60 results per search)"""
    all_results = []
    
    # First request
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    if data['status'] != 'OK':
        print(f"    Error: {data['status']} - {data.get('error_message', '')}")
        return []
    
    all_results.extend(data.get('results', []))
    results_count = len(data.get('results', []))
    
    # Get additional pages (Google allows up to 3 pages = 60 results max)
    page = 1
    while 'next_page_token' in data and page < 3:
        print(f"    Getting page {page + 1}...")
        time.sleep(2)  # Required delay between requests
        
        # Remove old pagetoken and add new one
        paginated_params = params.copy()
        if 'pagetoken' in paginated_params:
            del paginated_params['pagetoken']
        paginated_params['pagetoken'] = data['next_page_token']
        
        response = requests.get(url, params=paginated_params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'OK':
            page_results = data.get('results', [])
            all_results.extend(page_results)
            results_count += len(page_results)
        
        page += 1
    
    print(f"    Total results: {results_count}")
    return all_results

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

    keywords = ['salvadoran', 'pupusas', 'pupuseria', 'salvadorean', 'pulgarsito']
    all_places = {}

    for area_name, location in la_areas:
        print(f"\nSearching {area_name}...")
        
        for keyword in keywords:
            print(f"  Keyword: {keyword}")
            
            params = {
                'key': API_KEY,
                'location': location,
                'radius': 15000,
                'keyword': keyword
            }
            
            # Get all paginated results for this search
            results = get_all_results(url, params)
            
            # Add to our collection (avoiding duplicates)
            for place in results:
                place_id = place.get('place_id')
                if place_id not in all_places:
                    all_places[place_id] = place

    print(f"\nTotal unique places found: {len(all_places)}")

    # Create DataFrame
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
        print(f"Final dataset: {len(df)} unique Salvadoran restaurants")
        
        # Save to CSV
        df.to_csv("unfiltered_rating_restaurants.csv", index=False)
        print("Data saved to unfiltered_rating_restaurants.csv")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except Exception as e:
    print(f"Error: {e}")