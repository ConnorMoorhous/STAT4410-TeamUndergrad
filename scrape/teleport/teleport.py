import requests
import pandas as pd

# create main data frame
df = pd.DataFrame()

# get cities to search for from csv
cities = pd.read_csv("cities.csv")['city'].tolist()

for city in cities:

    cityName = city

    # search for city
    searchUrl = 'https://api.teleport.org/api/cities/?search=' + cityName
    searchResults = requests.get(searchUrl).json()['_embedded']['city:search-results']

    # find matching search result
    for result in searchResults:
        isMatch = False
        for name in result.get('matching_alternate_names'):
            if cityName == name.get('name'):
                isMatch = True
                break
        
        if isMatch:
            cityUrl = result.get('_links').get('city:item').get('href')
            cityJson = requests.get(cityUrl).json()['_links']

            # get first-level administrative division and country names
            admin1 = cityJson.get('city:admin1_division').get('name')
            country = cityJson.get('city:country').get('name')

            # get scores
            if cityJson.get('city:urban_area') != None:
                scoresUrl = cityJson['city:urban_area']['href'] +'scores'
                scores = requests.get(scoresUrl).json()

                # create temp df with scores
                dfTemp = pd.DataFrame(scores['categories'])

                # add city, admin1, and country names to data frame
                dfTemp.insert(0, "city", cityName, True)
                dfTemp.insert(1, "admin1", admin1, True)
                dfTemp.insert(2, "country", country, True)

                # add temp df to main df
                df = pd.concat([df, dfTemp], axis=0, ignore_index=True)

# export to csv
df.to_csv('..\\data\\raw\\teleport_raw.csv')