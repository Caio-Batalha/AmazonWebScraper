# Scrapes data from Amazon, updates the price, and sends an email when the price drops


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
import random
import os


full_path = os.path.join("/Users/caiobatalha", 'AmazonCaio.py')
print(full_path)


# List of proxy servers
proxies = [
    "123.45.67.89:8080",
    "98.76.54.32:3128",
    "111.22.33.44:8000",
    # ... add more proxies servers 
]

# Pick a random proxy (Avoid being recognized as a bot)
selected_proxy = random.choice(proxies)
ip, port = selected_proxy.split(":")

# Set up Firefox options adjusting to the proxy server
options = Options()
options.add_argument("--headless") #Comment this line if you want to see the opened browser
options.set_preference("network.proxy.type", 1)
options.set_preference("network.proxy.http", ip)
options.set_preference("network.proxy.http_port", int(port))
options.set_preference("network.proxy.ssl", ip)
options.set_preference("network.proxy.ssl_port", int(port))
options.set_preference("network.proxy.socks_remote_dns", True)

# Set Firefox binary location and geckodriver path
options.binary_location = "/Users/caiobatalha/Desktop/Firefox.app/Contents/MacOS/firefox"
service = Service("/opt/homebrew/bin/geckodriver")

# Start browser
driver = webdriver.Firefox(service=service, options=options)

# Now open your Amazon URL
URL = 'https://www.amazon.com.br/dp/B0C4HLNJJ1?th=1'
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
header = ['Title', 'Price', 'Date']
data = [title, price, today]


with open('AmazonWSDataset.csv', 'w', newline='', encoding='UTF8') as f: #risk of deleting my data
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)


# Appending data to the csv
with open('AmazonWSDataset.csv', 'a+', newline='', encoding='UTF8') as f:  #should I just use this chunk inside DataUpdates()?
    writer = csv.writer(f)
    writer.writerow(data)

#Creating a function so I can run with a set timer
def DataUpdates():

    # List of proxy servers
    proxies = [
        "123.45.67.89:8080",
        "98.76.54.32:3128",
        "111.22.33.44:8000",
     # ... add more
    ]

    # Pick a random proxy (Avoid being recognized as a bot)
    selected_proxy = random.choice(proxies)
    ip, port = selected_proxy.split(":")

    # Set up Firefox options adjusting to the proxy server
    options = Options()
    options.add_argument("--headless") #Comment this line if you want to see the opened browser
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.http", ip)
    options.set_preference("network.proxy.http_port", int(port))
    options.set_preference("network.proxy.ssl", ip)
    options.set_preference("network.proxy.ssl_port", int(port))
    options.set_preference("network.proxy.socks_remote_dns", True)

    # Set Firefox binary location and geckodriver path
    options.binary_location = "/Users/caiobatalha/Desktop/Firefox.app/Contents/MacOS/firefox"
    service = Service("/opt/homebrew/bin/geckodriver")

    # Start browser
    driver = webdriver.Firefox(service=service, options=options)

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
    data = [title, price,today]

    # Appending data to the csv
    with open('AmazonWSDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

    # Email notification if price drops at least 5%
    # Load previous price from CSV (last line)
    try:
        df = pd.read_csv(r'/Users/caiobatalha/AmazonWSDataset.csv')
        last_price = df.iloc[-1]['Price']
    
        # Check if price dropped 5% or more
        if price < last_price * 0.95:
            drop_percentage = ((last_price - price) / last_price) * 100
            print(f"Price dropped by {drop_percentage}% or more! Sending email.")
        
            # Set up with your own email credentials 
            sender_email = "sender_email@gmail.com"
            receiver_email = "receiver_email@gmail.com"
            password = "sender_email_password"  

            subject = "Price Drop Alert!"
            body = (f"The price dropped from ${last_price} to ${price} ({round(drop_percentage, 2)}% drop).\n"f"Buy now at: {URL}")

            message = f"Subject: {subject}\n\n{body}"

            # Send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print(f"Email alert skipped or failed: {e}")


#Runs DataUpdates() after a set time and inputs data into your CSV
while(True):
    DataUpdates()
    time.sleep(86400) # once in every 24 hours




