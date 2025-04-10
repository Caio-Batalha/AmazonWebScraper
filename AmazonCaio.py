from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import datetime
import csv 
import pandas as pd
import time
import smtplib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

project_name = "my_project"
full_path = os.path.join("/Users/caiobatalha", 'AmazonCaio.py')
print(full_path)




# I wan't to add a option where the user types the product name he wants, maybe multiple products at once (let's do it later)

# Set up Firefox WebDriver
firefox_options = Options()
firefox_options.binary_location = "/Users/caiobatalha/Desktop/Firefox.app/Contents/MacOS/firefox"

# Uncomment the next line if you want it to run in the background
firefox_options.add_argument("--headless")

# Point to your geckodriver location (That is the bridge between Firefox and Selenium)
service = Service("/opt/homebrew/bin/geckodriver")
driver = webdriver.Firefox(service=service, options=firefox_options)

# Open the Amazon page
URL = 'https://www.amazon.com.br/dp/B0C4HLNJJ1?th=1'  #replace with the product link you are interested
driver.get(URL)

# Wait until the product title is present
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "productTitle")))
except:
    print("Timed out waiting for the product title.")


# Get the page source
html = driver.page_source

# Close the browser
#driver.quit()

# Parse the page with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")



# Getting product information using BeautifulSoup
title = soup.find(id="productTitle")
if title:
    print('The product title is:', title.get_text(strip=True))
    title = title.get_text(strip=True)

else:
    print("Product title not found!")


# Finding the price
price_elem = soup.find(class_="a-price-whole")
decimalPrice = soup.find(class_="a-price-fraction")


    # Combine prices and convert to float
if price_elem is not None and decimalPrice is not None:
    price = float(f"{price_elem.get_text(strip=True)}{decimalPrice.get_text(strip=True)}")
    print(f"The product price is: ${price}")
else:
    print("Could not find the full price")

ratings = soup.find(class_="a-icon a-icon-star a-star-4 cm-cr-review-stars-spacing-big")
if ratings:
    ratings = float(ratings.get_text(strip=True).split()[0])  # Extract and convert to float
    print('The product average ratings are:', ratings)
else:
    print('Product rating not found')

# Create a Timestamp for your output to track when data was collected
today = datetime.date.today()
print(today)

# Create CSV and write headers and data into the file
header = ['Title', 'Price', 'Ratings', 'Date']
data = [title, price, ratings, today]


with open('AmazonWSDatasetWORKING.csv', 'w', newline='', encoding='UTF8') as f: #risk of deleting my data
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)


# So I won't have to keep opening my csv file (might delete this later)
DataFrame = pd.read_csv(r'/Users/caiobatalha/AmazonWSDatasetWORKING.csv')

print(DataFrame)

# Appending data to the csv
with open('AmazonWSDatasetWORKING.csv', 'a+', newline='', encoding='UTF8') as f:  #should I just use it in side my function?
    writer = csv.writer(f)
    writer.writerow(data)

#Creating a function so I can run with a set timer
def DataUpdates():
    # Set up Firefox WebDriver
    firefox_options = Options()
    firefox_options.binary_location = "/Users/caiobatalha/Desktop/Firefox.app/Contents/MacOS/firefox"

    # Uncomment the next line if you want it to run in the background
    firefox_options.add_argument("--headless")

    # Point to your geckodriver location (That is the bridge between Firefox and Selenium)
    service = Service("/opt/homebrew/bin/geckodriver")
    driver = webdriver.Firefox(service=service, options=firefox_options)

    # Open the Amazon page
    driver.get(URL)

    # Get the page source
    html = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Getting product information using BeautifulSoup
    title = soup.find(id="productTitle")
    if title:
        print('The product title is:', title.get_text(strip=True))
        title = title.get_text(strip=True)

    else:
        print("Product title not found!")

    # Finding the price
    price_elem = soup.find(class_="a-price-whole")
    decimalPrice = soup.find(class_="a-price-fraction")


    # Combine prices and convert to float
    if price_elem is not None and decimalPrice is not None:
        price = float(f"{price_elem.get_text(strip=True)}{decimalPrice.get_text(strip=True)}")
        print(f"The product price is: ${price}")
    else:
        print("Could not find the full price")


    # Create a Timestamp for your output to track when data was collected
    today = datetime.date.today()
    print(today)

    # Create CSV and write headers and data into the file
    data = [title, price, ratings, today]

    # So I won't have to keep opening my csv file (might delete this later)
    DataFrame = pd.read_csv(r'/Users/caiobatalha/AmazonWSDatasetWORKING.csv')

    print(DataFrame)

    # Appending data to the csv
    with open('AmazonWSDatasetWORKING.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# Runs check_price after a set time and inputs data into your CSV
#while(True):
    #DataUpdates()
    #time.sleep(86400)





    

# I could create conditions to send email if the price of products drop
# Plot graphics showing the price changes 
# New similar program showing prices from different major websites