# surf-wave-classification

# Data scrapper
This code scraps data automatically from https://magicseaweed.com/. Extracted info includes current wave ratings, local time, weather conditions and takes several screenshots from the webcam video. Data scrapping is done using the beautifulsoup (https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library, while opening the video inteface is done via selenium (https://www.selenium.dev/).
All data is stored in folders named by each session time, IMPORTANT - this code was run on GMT+2 time zone, manual change of timezone is required within the timeZoneFac variable in the data_scrapper script.
## Using preffered webbrowsers
As magicseaweed includes adds on thier videos using an addblocker while running this script is highly reccomended. This script support only chrome and firefox webbrowsers. The script will run the default user folder for each browser, so make sure to install an addblocker and make it your default option.
Note - other installed browser addons may interfere unexpectedly with the script, thus opening a dedicated user for data scrapping might be the best option.
## Web drivers
you can download the relevant drivers for the web scrapper form the following links:
chorme - https://sites.google.com/chromium.org/driver/
firefox - https://github.com/mozilla/geckodriver/releases
note - the firefox class scrapper does not open the default browser for an unkown reason. 
