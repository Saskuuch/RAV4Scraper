urls = ['https://www.salmonarmtoyota.com', 'https://www.peacecountrytoyota.ca']
subquery = ['/new/keywords/rav4','/used/keywords/rav4']

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time

cars = []

def toyotaScrape1(url, dealer):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"}
    request = requests.get(url = url, headers=headers)

    soup = BeautifulSoup(request.content, 'html.parser')
    lookupClass = 'vehicle-list-cell listing-page-row-padding-0'


    table = soup.find('div', attrs = {'id': 'vehicleList'})
    for row in table.find_all('div', attrs = {'class': lookupClass}):
        price = row.find_all('span', attrs = {'itemprop': 'price'})
        milage = row.find('span', attrs={'class':'mileage-used-list'})
        year = row.find('span', attrs={'itemprop':'releaseDate'})
        make = row.find('span', attrs={'itemprop':'manufacturer'})
        model = row.find('span', attrs={'itemprop': 'model'})
        url = row['itemid']

        tempCar = {'price':price, 'milage':milage, 'year' : year, 'make':make, 'model':model, 'url': url, 'dealer': dealer}
        for key, value in tempCar.items():
            tempCar[key] = re.sub(r"<.*?>", "", str(value))
        cars.append(tempCar)

for url in urls:
    for query in subquery:
        toyotaScrape1(url + query, url)

def toyotaScrape2(url, dealer):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"}
    request = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(request.content, 'html.parser')

    table = soup.find('div', attrs={'class': 'divSpan divSpan12 lstListingWrapper'}).find('ul')
    for row in table.find_all('li'):
        price = row.find('div', attrs={'class': 'carPrice'}).find('span')
        milage = row.find('span', attrs={'class': 's-km'})
        year = row.find('input', attrs={'name':'vehicledata'})['data-year']
        make = row.find('input', attrs={'name':'vehicledata'})['data-make']
        model = row.find('input', attrs={'name':'vehicledata'})['data-model']
        vin = row.find('input', attrs={'name':'vehicledata'})['data-vin']
        url = row.find('a', attrs = {'class': 'carTitle shrink-grow'})['href']

        tempCar = {'price': price, 'milage': milage, 'year': year, 'make': make, 'model': model, 'url': url,
                   'dealer': dealer, 'vin': vin}
        for key, value in tempCar.items():
            tempCar[key] = re.sub(r"<.*?>", "", str(value))
        cars.append(tempCar)

def toyotaScrape3(url, dealer):
    soup = BeautifulSoup(loadJS(url), 'html.parser')
    table = soup.find('div', attrs={'class': 'resultCard'})

    for row in table.find_all('a', attrs={'class': 'carCard'}):
        print(row)
        price = row.find('span', attrs={'class': 'sale-price srp-price'})
        milage = row.find('span', attrs={'class': 'carMiles srp-mileage'})
        year = row.find('p', attrs={'class': 'carMake srp-fullname'})
        make = 'Toyota'
        model = row.find('p', attrs={'class': 'carMake srp-fullname'})
        vin = row.find('span', attrs={'class': 'srp-vin'})
        try:
            url = row['href']
        except:
            print('That didnt work')


        tempCar = {'price': price, 'milage': milage, 'year': year, 'make': make, 'model': model, 'url': url,
                   'dealer': dealer, 'vin': vin}
        print(tempCar)
        for key, value in tempCar.items():
            tempCar[key] = re.sub(r"<.*?>", "", str(value))
        cars.append(tempCar)


def loadJS(url):
    options = Options()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # Path to your ChromeDriver
    service = Service()

    # Start driver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the page
    driver.get(url)

    # Optional: wait for JavaScript to load (simple way)
    time.sleep(3)  # Wait 3 seconds (better to use WebDriverWait — see below)
    return driver.page_source


toyotaScrape2('https://www.sargenttoyota.ca/inventory.html?filterid=a1b13q0-10x0-0-0+W3sidHNlYXJjaCI6W3sibiI6ImZpZWxkc2VhcmNoIiwidiI6InJhdjQiLCJzIjoxfV19XQ==', 'https://www.sargenttoyota.ca')
toyotaScrape2('https://www.terracetoyota.ca/inventory.html?filterid=a8q0-10x0-0-0+W3sidHNlYXJjaCI6W3sibiI6ImZpZWxkc2VhcmNoIiwidiI6InJhdjQiLCJzIjoxfV19XQ==', 'https://www.terracetoyota.ca')
toyotaScrape3('https://www.quesneltoyota.ca/used-inventory?status=used&search=rav4', 'https://www.quesneltoyota.ca')
toyotaScrape3('https://www.quesneltoyota.ca/new-inventory?make=toyota&status=new&search=rav4', 'https://www.quesneltoyota.ca')
today = datetime.date.today()
today = today.strftime("%Y-%m-%d")
df = pd.DataFrame(cars)
df.to_csv('./Output/' + today + ".csv")
print(df)