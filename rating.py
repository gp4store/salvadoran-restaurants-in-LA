import pandas as pd

'''Data quality check since we are just working with the values
on the rating column we are checking if theres no out of range
values'''

df = pd.read_csv("unfiltered_rating_restaurants.csv")
mask = df['rating'].between(1, 5)

if mask.all():
    print('All ratings are valid (between 1 and 5)')
else:
    invalid_count = (~mask).sum()
    print(f'Found {invalid_count} invalid ratings out of {len(df)} total')

try:
        unfiltered_rating = "unfiltered_rating_restaurants.csv"
        # Reading original raw restaurant dataset
        df = pd.read_csv(unfiltered_rating)
        
        # Cleaning dataset for restaurants that have 4.5 or 5 stars rating
        # Replacing long place_id with 0, 1, 2, .. values
        filtered_rating = df[df['rating'] >= 4.5]
        filtered_rating.loc[:, 'place_id'] = range(len(filtered_rating))
        filtered_rating.to_csv('filtered_rating_restaurants.csv', index=False)
        
        print(f'Original dataset rows {len(df)}')
        print(f'Filtered rating dataset {len(filtered_rating)}')

except FileNotFoundError:
    print('No unfiltered raw dataset found')