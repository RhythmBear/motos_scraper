from bot import MotosBot
import time
import csv

ford_url = "https://uae.yallamotor.com/new-cars/ford/edge/2-0t-trend"

new_bot = MotosBot()

new_bot.load_page(ford_url)
results = new_bot.get_car_details_dict()
new_bot.save_to_csv(results)

time.sleep(5)