## create a webscrapper that will get the html data from a webpage and save it into a new html.
## The html page where the scrapper html page will be stored is called car_website.html
## The website is https://autochek.africa/ke/cars-for-sale?price_high=12000000&page_number=1

import requests
from bs4 import BeautifulSoup

# get the data from the website
url = 'https://autochek.africa/ke/cars-for-sale?price_high=12000000&page_number=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# create a new html file to store the data
html_file = open('car_website.html', 'w')
html_file.write(soup.prettify())
html_file.close()

print('The data has been saved in car_website.html')

# The data has been saved in car_website.html
