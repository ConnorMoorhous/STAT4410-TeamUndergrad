import pandas as pd

locations = pd.read_csv("location_list.csv")['levels.locs.'].tolist()

df = pd.DataFrame()

for loc in locations:
    tokens = loc.split(',')
    if len(tokens) < 3:
        entry = pd.DataFrame({
            'location': [loc],
            'city': [tokens[0]],
            'state': [tokens[1]]
        })
        df = pd.concat([df, entry], ignore_index = True)

df.to_csv('cities.csv')