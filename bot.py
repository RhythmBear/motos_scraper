from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, NoSuchFrameException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import requests
import csv
import time
import os
import pickle

class MotosBot:

    def __init__(self):
        # Initialize Chrome Driver
        self.browser = self.initialize_chrome_driver()
        self.action = ActionChains(self.browser)

       
    def initialize_chrome_driver(self):
        # Chrome driver path
        # driver_path = "chromedriver.exe"

        # Create Chrome options instance
        options = Options()
        
        # options.add_argument(r'--profile-directory=Default')
        options.add_argument("--start-maximized")

        # Adding argument to disable the AutomationControlled flag
        # options.add_argument("--disable-blink-features=AutomationControlled")

        # Exclude the collection of enable-automation switches
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Turn-off userAutomationExtension
        # options.add_experimental_option("useAutomationExtension", False)

        # Run in the headless browser
        options.headless = False
        # proxies = self.get_proxies_list()
        options.add_argument(f"proxy-server=192.3.54.198:3128")
        # print(f"Working with IP --> {proxies[0]}")

        options.add_argument("--user-data-dir=/home/rhythmbear/.config/google-chrome/Default")

        # Setting the driver path and requesting a page
        driver = uc.Chrome(# service=ChromeService()
             options=options)

        # Changing the property of the navigator value for webdriver to undefined
        # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver
    
    def get_proxies_list(self):
        # Proxies URL 
        proxy_url = "https://proxylist.geonode.com/api/proxy-list?filterUpTime=90&speed=fast&google=false&limit=5&page=1&sort_by=lastChecked&sort_type=desc"
        response = requests.get(proxy_url)
        data = response.json()
        
        data_list = data['data']
        proxies_list = [f"{item['ip']}" for item in data_list]

        print(proxies_list)

        return proxies_list

    def load_page(self, url):
        print('Loading Car Page...')
        self.browser.get(url)

    def get_car_details(self):
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        print(soup.title.get)

    def get_car_details_dict(self) -> dict:

        print("Retrieving Car Details...")
        car_name = self.browser.find_element(By.XPATH, "//h1").text
        parent_desc = self.browser.find_elements(By.XPATH, "//div[@class='row is-m is-compact']")
        result_dict = {}
        result_dict['car_name'] = car_name
        for item in parent_desc:
            try:
                desc = item.find_element(By.XPATH, ".//div[@class='col is-7 p0']").text
                ans = item.find_element(By.XPATH, ".//div[@class='col is-5 p0 font-b']").text
            except NoSuchElementException:
                continue
            else:
                result_dict[desc] = ans

        return result_dict
    
    def save_to_csv(self, data):
        print("Saving to CSV...")
        # Open the CSV file in write mode
        with open('car_data.csv', 'w', newline='') as csvfile:
            # Create a csv writer object
            writer = csv.writer(csvfile)
            # Write the header row (keys of the dictionary)
            writer.writerow(data.keys())
            # Write a data row with the values from the dictionary
            writer.writerow(data.values())

        print("Data successfully exported to car_data.csv")

    def get_new_cars_for_brand_model(self, brand, model) -> list:
        # Get the current title of the page
        title = self.browser.find_element(By.XPATH, "//h1").text
        
        # Assert that the page was succesfully loaded and we are on the right page.
        assert brand.title() in title
        assert model.title() in title 
        
        # Get the Table that has the cars details
        car_table = self.browser.find_element(By.XPATH, "//table[@class='table m24t usedcarsTable versions font14']")

        car_table_rows = car_table.find_elements(By.XPATH, ".//tr")
        
        # print(f"Found {len(car_table_rows) - 1} new cars for {brand} - {model}")

        # Get the car body type 
        car_body_type = self.browser.find_element(By.XPATH, "//div[@class='col is-4 p16']/div/span[contains(text(), 'Body Style')]//parent::div//following-sibling::p").text
        # print(car_body_type)
        car_results = []
        
        # Loop through each row in the table and get the car details.
        for row in car_table_rows:
            new_car = {}
            try:
                car_summary = row.find_element(By.XPATH, ".//td/div[@class='m8t font-n']")
            except:
                print(row.text)
            else:
                car_sum = car_summary.text.split(", ")
            
                car_name = row.find_element(By.XPATH, ".//td/div/a").text
                car_link = row.find_element(By.XPATH, ".//td/div/a").get_attribute("href")
                car_price = row.find_element(By.XPATH, ".//td/div[@class='font-b']").text
            
                year = car_sum[0]
                fuel_type = car_sum[1]
                transmission = car_sum[2]
                print(year, fuel_type, transmission, car_link, car_name, car_price)
                
                # Create New Car Entry
                new_car['link'] = car_link
                new_car['year'] = year
                new_car['make'] = brand 
                new_car['model'] = car_name
                new_car['variant'] = car_name
                new_car['body_type'] = car_body_type
                new_car['transmission'] = transmission
                new_car['fuel_type'] = fuel_type
                new_car['price'] = car_price

                car_results.append(new_car)

        # print(car_results)
        # print("I got to the end")

        return car_results
        


