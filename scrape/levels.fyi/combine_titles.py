import pandas as pd

titles = ['software-engineer','product-designer','product-manager','data-scientist','software-engineering-manager','technical-program-manager','solution-architect','security-analyst','information-technologist','program-manager','project-manager','data-science-manager','product-design-manager','technical-writer','sales-engineer','biomedical-engineer','civil-engineer','hardware-engineer','mechanical-engineer','geological-engineer']

df = pd.DataFrame()

for title in titles:
    dfTemp = pd.read_csv(f'levels.fyi\\titles\\levels_{title}.csv')
    df = pd.concat([df, dfTemp], ignore_index = True)

df.to_csv('..\\data\\raw\\levels.fyi_scraped.csv')