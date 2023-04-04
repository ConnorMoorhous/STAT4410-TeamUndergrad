from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from time import sleep
import re
import math
import pandas as pd
import datetime

driver = webdriver.Edge(service = Service('drivers\\msedgedriver.exe'))
titles = ['software-engineer','product-designer','product-manager','data-scientist','software-engineering-manager','technical-program-manager','solution-architect','security-analyst','information-technologist','program-manager','project-manager','data-science-manager','product-design-manager','technical-writer','sales-engineer','biomedical-engineer','civil-engineer','hardware-engineer','mechanical-engineer','geological-engineer']
locations = pd.read_csv("teleport\\cities.csv")['location'].tolist()

def numPages(driver):
    try:
        indexInfo = driver.find_element(By.CSS_SELECTOR, 'label[id="limit-select"]').find_element(By.XPATH, "..").find_element(By.XPATH, "..").text
    except:
        return -1
    totalEntries = int(indexInfo.split(' of ')[1].replace(',', ''))
    return math.ceil(totalEntries/50)

def waitForData(driver, title, offset):
    try:
        driver.get(f"https://www.levels.fyi/t/{title}?countryId=254&country=254&offset={offset}&limit=50")
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'svg[data-icon="lock"]')
        print("Waiting...")
        sleep(300)
        driver.get(f"https://www.levels.fyi/t/{title}?countryId=254&country=254&offset={offset}&limit=50")
        sleep(1)
    except:
        pass

# extract data
for title in titles:
    df = pd.DataFrame()

    driver.get(f"https://www.levels.fyi/t/{title}?countryId=254&country=254&offset=0&limit=50")
    sleep(2)
    
    # unlock salary data
    if title == titles[0]:
        try:
            addSalaryBtn = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[3]/div/div[2]/table/tbody/tr[5]/td/div/div/button')
            addSalaryBtn.location_once_scrolled_into_view
            addSalaryBtn.click()
            sleep(1)

            salaryConfirmBtn = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[3]/div/div[2]/table/tbody/tr[5]/td/div/div/button')
            salaryConfirmBtn.location_once_scrolled_into_view
            salaryConfirmBtn.click()
            sleep(1)
        except:
            pass

    # find number of pages
    totalPages = numPages(driver)
    if totalPages == -1:
        waitForData(driver, title, 0)

    for page in range(totalPages):
        if page > 0:
            searchUrl = f"https://www.levels.fyi/t/{title}?countryId=254&country=254&offset={page*50}&limit=50"
            driver.get(searchUrl)
            sleep(2)
            if numPages(driver) == -1:
                waitForData(driver, title, page*50)

        rows = len(driver.find_elements(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr"))
        columns = len(driver.find_elements(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[2]/td"))
        now = datetime.datetime.now()

        for row in range(1, (rows + 1)):
            company = city = state = date = level = tag = xp = companyXp = compensation = salary = stocks = bonus = type = sex = race = education = None

            for column in range(1, (columns + 1)):
                XPath = "/html[1]/body[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[" + str(row) + "]/td[" + str(column) + "]"
                cellText = driver.find_element(By.XPATH, XPath).text

                if column == 1:
                    tokens = re.split('\n| \| ', cellText)
                    company = tokens[0]

                    try:
                        loc = tokens[1].split(', ')
                        city = loc[0]
                        state = loc[1]
                    except:
                        city = "hidden" # if entry is fully hidden

                    try:
                        dateTokens = tokens[2].split(' ')
                        if len(dateTokens) > 1:
                            if dateTokens[1].__contains__('hour'):
                                newTime = now - datetime.timedelta(hours = int(dateTokens[0]))
                            elif dateTokens[1].__contains__('day'):
                                newTime = now - datetime.timedelta(days = int(dateTokens[0]))
                            date = newTime.strftime('%m/%d/%Y')
                        else:
                            date = tokens[2]
                    except:
                        date = "ad" # if entry is an ad
                        break

                elif column == 2:
                    tokens = cellText.split('\n')
                    level = tokens[0]
                    tag = tokens[1]

                elif column == 3:
                    tokens = cellText.split('\n')
                    xp = tokens[0]
                    companyXp = tokens[1]

                elif column == 4:
                    tokens = re.split('$|\n| \| ', cellText)
                    if tokens[0].__contains__('+'):
                        compensation = tokens[1]
                        salary = tokens[2]
                        stocks = tokens[3]
                        bonus = tokens[4]
                    else:
                        compensation = tokens[0]
                        salary = tokens[1]
                        stocks = tokens[2]
                        bonus = tokens[3]

            if date == "ad" or city == "hidden":
                continue
                
            # expand entry
            driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/table[1]/tbody/tr[" + str(row) + "]").click()

            # extract extra information
            try:
                type = driver.find_element(By.CSS_SELECTOR, 'svg[data-testid="WorkIcon"]').find_element(By.XPATH, '..').text
            except:
                pass

            try:
                sex = driver.find_element(By.CSS_SELECTOR, 'svg[data-icon="mars-and-venus"]').find_element(By.XPATH, '..').text
            except:
                pass

            try:
                race = driver.find_element(By.CSS_SELECTOR, 'svg[data-icon="earth-americas"]').find_element(By.XPATH, '..').text
            except:
                pass

            try:
                education = driver.find_element(By.CSS_SELECTOR, 'svg[data-icon="graduation-cap"]').find_element(By.XPATH, '..').text
            except:
                pass

            # collapse entry
            driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/table[1]/tbody/tr[" + str(row) + "]").click()

            # create and add entry to df
            entry = pd.DataFrame({
                'date': [date],
                'company': [company],
                'level': [level],
                'title': [title],
                'total_annual_compensation': [compensation],
                'city': [city],
                'state': [state],
                'years_of_experience': [xp],
                'years_at_company': [companyXp],
                'tag': [tag],
                'base_salary': [salary],
                'stock_grant_value': [stocks],
                'bonus': [bonus],
                'gender': [sex],
                'race': [race],
                'education' : [education],
                'type': [type]
            })
            df = pd.concat([df, entry], ignore_index = True)

    df.to_csv(f'levels.fyi\\titles\\levels_{title}.csv')