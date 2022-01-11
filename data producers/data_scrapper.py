import numpy as np
import cv2
import os
import webbrowser
from bs4 import BeautifulSoup
import requests

import datetime
from browser_classes import *


def collect_data(url: str, folder_loc: str):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    rating_window = soup.find('ul', class_="rating rating-large clearfix")
    stars = rating_window.findAll('li', class_='active')
    star_num = len(stars)
    half_stars = rating_window.findAll('li', class_='inactive')
    half_star_num = len(half_stars)
    location = soup.find('h1', class_='nomargin page-title').text.replace('  ', '')

    # finding the local time
    time_window = soup.find('span', class_='msw-js-time')
    time_zone = int(time_window.attrs.get('data-timezone'))       # the time in the location
    time_loc = datetime.datetime.now()
    time_delta = datetime.timedelta(seconds=-7200 + time_zone)
    time_loc = time_loc + time_delta
    weekday = time_loc.weekday()                                  # the day of the week (Monday == 0, Sunday == 6)

    # finding the sunrise and sunset times
    sun_times_table = soup.find('div', class_='row msw-tide-tables')
    sun_times_table = sun_times_table.findAll('td', class_='text-right')
    sunrise_time = sun_times_table[5].text.replace('  ', '')        # sunrise time in the location
    sunrise_time = convert_time(sunrise_time)
    sunset_time = sun_times_table[6].text.replace('  ', '')         # sunrise time in the location
    sunset_time = convert_time(sunset_time)
    # finding the weather conditions
    weather_box = soup.find('p', class_='nomargin-bottom')
    weather = weather_box.find('i').text                            # weather description at the location
    # writing an output file inside the data folder
    with open(os.path.join(folder_loc, 'data.txt'), 'w') as f:
        f.write(f"{location}\n")
        f.write(f"Stars: {str(star_num)}\n")
        f.write(f"Half stars: {str(half_star_num)}\n")
        f.write(f"Time: {time_loc.strftime('%H:%M')}\n")
        f.write(f"Sunrise: {str(sunrise_time[0])}:{str(sunrise_time[1])}\n")
        f.write(f"Sunset: {str(sunset_time[0])}:{str(sunset_time[1])}\n")
        f.write(f"Weekday: {str(weekday)}\n")
        f.write(f"Weather: {str(weather)}\n")
    print(f'File saved: {location}')
    # in case the sample is taken after sundown or before dawn return False, otherwise return True
    if sunrise_time[0] * 60 + sunrise_time[1] <= time_loc.time().hour * 60 + time_loc.time().minute <=\
            sunset_time[0] * 60 + sunset_time[1]:
        return True
    else:
        return False


def convert_time(str_time: str):
    suffix = str_time[-2:]
    mins = int(str_time[-4:-2])
    hour = int(str_time[:2])
    if suffix == 'PM':
        hour += 12
    return [hour, mins]


# ------------------------------------- main ------------------------------------------------ #
if __name__ == '__main__':
    url_list_txt = open(os.path.join(os.getcwd(), 'URL list 2.txt'), "r")
    url_list = url_list_txt.readlines()
    photo_set_num = 10                              # number of photos to take for each camera
    photo_delay = 1                                 # delay in seconds between each to photos
    selenium_files_path = 'C:\Documents\Selenium Drivers'
    for url in url_list:
        batch_name = os.path.join(os.getcwd(), 'photos', datetime.datetime.now().strftime("%d-%m-%Y %H-%M"))
        if not os.path.exists(batch_name):
            os.makedirs(batch_name)
        day_flag = collect_data(url, batch_name)
        if day_flag:
            recorder = ChromeRecorder(selenium_files_path)
            recorder.open_page(url)
            time.sleep(1)
            for i in range(photo_set_num):
                recorder.take_screenshot(os.path.join(batch_name, str(i + 1) + '.png'))
                time.sleep(photo_delay)
            recorder.teardown()
