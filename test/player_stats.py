import statsapi
import pandas as pd
import json

# Write pitching stats to a JSON file
def save_pitching_stats(pitching, player_id, year):
    filename = f'pitching_stats_{player_id}_{year}.json'
    with open(filename, 'w') as f:
        json.dump(pitching, f, indent=4)

# After your existing code, add:


def save_pitching_statscsv(pitching, player_id, year):
    filename = f'pitching_stats_{player_id}_{year}.csv'
    # Convert the pitching stats dictionary to a DataFrame
    df = pd.DataFrame([pitching])
    df.to_csv(filename, index=False)

# After your existing code, add:




player_id=660271
year = 2022
pitching=[]
hitting=[]
fielding=[]

stats = statsapi.get('people', {'personIds': player_id, 'season': year, 'hydrate': f'stats(group=[hitting,pitching,fielding],type=season,season={year})'})['people'][0]
for stat in stats['stats']:
    print(stat['group']['displayName'])
    if stat['group']['displayName'] == 'hitting':
        hitting.append(stat['splits'][0]['stat'])
    elif stat['group']['displayName'] == 'pitching':
        pitching.append(stat['splits'][0]['stat'])
    elif stat['group']['displayName'] == 'fielding':
        fielding.append(stat['splits'][0]['stat'])

print(hitting[0])

if pitching:  # Check if pitching array is not empty
    save_pitching_statscsv(pitching[0], player_id, year)
#print(stats['stats'])