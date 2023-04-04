import pandas as pd
import requests

data = requests.get('https://www.levels.fyi/js/salaryData.json').json()
df = pd.DataFrame(data)
df.to_csv('C:\\Users\\14025\OneDrive - University of Nebraska at Omaha\\Classes\\SP23\\STAT 4410 - Introduction to Data Science\\STAT 4410 Project - Team Undergrad\\Project Folder\\salaryData.csv')