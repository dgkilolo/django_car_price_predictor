## create a web scrapper to get the data from a car website.
## The data will be stored in a csv file
## The data will be used to train a model to predict the price of a car
## This is the link to the website: https://autochek.africa/ke/cars-for-sale?price_high=12000000&page_number=1
## An example of this html file is already stored in 'car_website.html'
## The data to be scrapped are:
## 1. Car name
## 2. Car price
## 3. Car year
## 4. Car mileage
## 5. Car fuel type
## 7. Car transmission
## 8. Car engine size
## 9. Car image url
## use beautifulsoup to scrap the data

import requests
from bs4 import BeautifulSoup
import csv

# how many pages do you want to scrape
pages = 3

# create a csv file to store the data
# csv_file = open('Combined_Data.csv', 'a')
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(['Make', 'Model', 'YOM', 'Mileage', 'Engine_Size', 'Fuel_Type', 'Transmission', 'Price', 'Car_Image_URL'])


for page in range(pages):
    # get the data from the website
    url_page = page + 1
    url = f'https://autochek.africa/ke/cars-for-sale?price_high=12000000&page_number={url_page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # open the file to store the data
    csv_file = open('Combined_Data.csv', 'a')
    csv_writer = csv.writer(csv_file)

    # div with vehicle image
    car_image_data = soup.find_all('div', class_='MuiBox-root css-1jke4yk')

    # div with vehicle detatils
    car_data = soup.find_all('div', class_='MuiBox-root css-qym38b')

    car_count = len(car_image_data)

    for i in range(car_count):

        car = car_data[i]
        car_img = car_image_data[i]

        car_make = car.find('h6', class_='MuiTypography-root MuiTypography-h6 css-1g399u0').text.split(' ')[1]
        car_model = ' '.join(car.find('h6', class_='MuiTypography-root MuiTypography-h6 css-1g399u0').text.split(' ')[2:])
        car_price = int(car.find('p', class_='MuiTypography-root MuiTypography-body1 css-1bztvjj').text.split(' ')[1].replace(',', ''))
        car_year = car.find('h6', class_='MuiTypography-root MuiTypography-h6 css-1g399u0').text.split(' ')[0]
        car_mileage = int(car.find_all('span', class_='MuiChip-label MuiChip-labelSmall css-1pjtbja')[1].text.split(' ')[0].replace('K', ''))*1000
        car_fuel_type = ''
        car_transmission = 'Automatic'
        car_engine_size = int(car.find_all('span', class_='MuiChip-label MuiChip-labelSmall css-1pjtbja')[2].text.split(' ')[0].replace('Cc', ''))
        car_image_url = car_img.find('span').noscript.img['src']
        if car_make == 'Toyota' and car_model == 'Land Cruiser':
            car_fuel_type = 'Diesel'
        elif car_make == 'Toyota' and car_engine_size > 2750 and car_engine_size < 2999:
            car_fuel_type = 'Diesel'
        elif car_make == 'Toyota' and car_model == 'Hilux':
            car_fuel_type = 'Diesel'
        elif car_make == 'Mazda' and car_model == 'CX-5' and car_engine_size > 2100:
            car_fuel_type = 'Diesel'
        elif car_make == 'Mazda' and car_model == 'CX-3' and car_engine_size > 1450:
            car_fuel_type = 'Diesel'
        elif car_make == 'Mazda' and car_model == 'Demio' and car_engine_size > 1450:
            car_fuel_type = 'Diesel'
        elif car_make == 'Mazda' and car_engine_size > 2100:
            car_fuel_type = 'Diesel'
        elif car_make == 'Isuzu':
            car_fuel_type = 'Diesel'
        elif car_make == 'Nissan' and car_model == 'Navara':
            car_fuel_type = 'Diesel'
        elif car_make == 'Volvo' and car_engine_size == 2000:
            car_fuel_type = 'Diesel'
        else:
            car_fuel_type = 'Petrol'

        csv_writer.writerow([car_make, car_model, car_year, car_mileage, car_engine_size, car_fuel_type, car_transmission, car_price, car_image_url])

    csv_file.close()

    print('The data has been saved in Combined_Data.csv')
# The data has been saved in car_data.csv