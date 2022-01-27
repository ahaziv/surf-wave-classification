import numpy as np
import cv2 as cv
import os
import webbrowser
import csv
from bs4 import BeautifulSoup
import requests
import shutil
import datetime
from browser_classes import *
from apscheduler.schedulers.blocking import BlockingScheduler


def collect_data(url: str, timezone: int, crop_coor: str):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    # extracting the rating
    rating_window = soup.find('ul', class_="rating rating-large clearfix")
    stars = rating_window.findAll('li', class_='active')
    star_num = len(stars)
    half_stars = rating_window.findAll('li', class_='inactive')
    half_star_num = len(half_stars)
    location = soup.find('h1', class_='nomargin page-title').text.replace('  ', '')

    # extracting swell height
    swell = rating_window.find('li', class_='rating-text text-dark').text.replace('  ', '')

    # extracting the local time
    time_window = soup.find('span', class_='msw-js-time')
    time_zone = int(time_window.attrs.get('data-timezone'))       # the time in the location
    time_loc = datetime.datetime.now()
    time_delta = datetime.timedelta(seconds=-timezone + time_zone)
    time_loc = time_loc + time_delta
    weekday = time_loc.weekday()                                  # the day of the week (Monday == 0, Sunday == 6)

    # extracting the sunrise and sunset times
    sun_times_table = soup.find('div', class_='row msw-tide-tables')
    sun_times_table = sun_times_table.findAll('div', class_='col-lg-6 col-md-6 col-sm-6 col-xs-6')
    sun_times_table = sun_times_table[1].findAll('td', class_='text-right')
    sunrise_time = sun_times_table[1].text.replace('  ', '')        # sunrise time in the location
    sunrise_time = convert_time(sunrise_time)
    sunset_time = sun_times_table[2].text.replace('  ', '')         # sunrise time in the location
    sunset_time = convert_time(sunset_time)
    # finding the weather conditions
    weather_box = soup.find('p', class_='nomargin-bottom')
    weather = weather_box.find('i').text                            # weather description at the location
    # writing an output file inside the data folder
    data = [location, url, str(star_num), str(half_star_num), swell, datetime.datetime.now().strftime('%d-%m-%Y %H'),
            time_loc.strftime('%H:%M'), str(sunrise_time[0]) + ':' + str(sunrise_time[1]),
            str(sunset_time[0]) + ':' + str(sunset_time[1]), str(weekday), weather, crop_coor]
    # in case the sample is taken after sundown or before dawn return False, otherwise return True
    if sunrise_time[0] * 60 + sunrise_time[1] <= time_loc.time().hour * 60 + time_loc.time().minute <=\
            sunset_time[0] * 60 + sunset_time[1]:
        return True, data
    else:
        return False, []


def convert_time(str_time: str):
    suffix = str_time[-2:]
    mins = int(str_time[-4:-2])
    hour = int(str_time[:2])
    if suffix == 'PM':
        hour += 12
    return [hour, mins]


def scrap_data():
    out_file_path = os.path.join(os.getcwd(), 'images')
    url_list_txt = open(os.path.join(os.getcwd(), 'URL list.txt'), "r")
    url_list = url_list_txt.readlines()
    photo_set_num = 20  # number of photos to take for each camera
    photo_delay = 10  # delay in seconds between each to photos
    crop_sze = [512, 256]  # the images size desired output
    scale_fac = 0.5  # image resize scale
    flag_crop = True
    flag_save = True

    # open the existing csv file in the processed data folder and find the number of images already stored
    if os.path.isfile(os.path.join(out_file_path, 'labels.csv')):
        with open(os.path.join(out_file_path, 'labels.csv'), mode='r', newline='') as csvfile:
            file_reader = csv.reader(csvfile)
            csv_counter = len(list(file_reader))
    else:
        with open(os.path.join(out_file_path, 'labels.csv'), mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Picture no.', 'Location', 'URL', 'Stars', 'Half_stars', 'Swell', 'Session',
                                 'Local_time', 'Sunrise', 'Sunset', 'Weekday', 'Weather', 'Crop_Point'])
            csv_counter = 1

    selenium_files_path = 'C:\Documents\Selenium Drivers'
    time_zone_fac = 7200  # change according to your oun relevant timezone
    for url in url_list:
        temp = url.split(' ')
        url = temp[0]
        strt_pnt = [int(temp[2]), int(temp[3])]
        day_flag, col_data = collect_data(url, time_zone_fac, f'{strt_pnt[0]} {strt_pnt[1]}')
        if day_flag:
            recorder = ChromeRecorder(selenium_files_path)
            recorder.open_page(url)
            time.sleep(3)
            for i in range(photo_set_num):
                img_path = os.path.join(out_file_path, 'image' + str(csv_counter) + '.png')
                recorder.take_screenshot(img_path)
                img = cv.imread(img_path, cv.IMREAD_UNCHANGED)
                # crop area of interest
                if flag_crop:
                    img = img[strt_pnt[1]:strt_pnt[1] + crop_sze[1], strt_pnt[0]:strt_pnt[0] + crop_sze[0], :]

                    # resize image
                    width = int(img.shape[1] * scale_fac)
                    height = int(img.shape[0] * scale_fac)
                    dim = (width, height)
                    img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

                    if flag_save:
                        cv.imwrite(img_path, img)
                        with open(os.path.join(out_file_path, 'labels.csv'), mode='a', newline='') as csvfile:
                            csv_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                            csv_writer.writerow(['image' + str(csv_counter) + '.png\n'] + col_data)

                csv_counter += 1
                time.sleep(photo_delay)
            recorder.teardown()


# ------------------------------------- main ------------------------------------------------ #
if __name__ == '__main__':
    flag_schedule = False
    hour_int = 3
    if flag_schedule:
        scheduler = BlockingScheduler(timezone="Israel")
        scheduler.add_job(scrap_data, 'interval', hours=hour_int, next_run_time=datetime.datetime.now())
        scheduler.start()
        for job in scheduler.get_jobs():
            job.modify(next_run_time=datetime.utcnow())
    else:
        scrap_data()


