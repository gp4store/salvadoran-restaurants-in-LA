import folium
import pandas as pd


def create_clustered_restaurant_map(csv_file):

    try:
        # Load and filter data
        df = pd.read_csv(csv_file)
        
        # Create map centered on the data        
        center_lat = df['latitude'].mean()
        center_lon = df['longitude'].mean()
       
        loc = "High Rated Salvadoran Restaurants across Los Angeles"
        title_html = f'<h3 align="center" style="font-size:24px; padding: 20px;"><b>{loc}</b></h3>'
       
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start = 10,
            tiles ='CartoDB positron')
        
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Add markers to cluster
        for idx, row in df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"""
                <div style="width: 200px">
                    <b>{row['name']}</b><br>
                    Rating: {row['rating']}⭐<br>
                    Address: {row.get('address', row.get('vicinity', 'N/A'))}
                </div>
                """,
                tooltip=f"{row['name']} - {row['rating']}⭐"
            ).add_to(m)
        return m
        
    except Exception as e:
        print(f"Error creating map: {e}")
        return None

# Create the map
map_obj = create_clustered_restaurant_map("filtered_rating_restaurants.csv")
if map_obj:
    map_obj.save('high_salvadoran_restaurants_la.html')
    print("Interactive map saved as 'high_salvadoran_restaurants_la.html'")