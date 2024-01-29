# surf-wave-classification - work in progress
This small project aims to classify surf wave quality using a deep convolutional neural net. Scripts include:
- Data scrappers used to obtain train and test images.
- Data edditing tools assisting in manual trimming of bad data and image cropping.
- A pytorch dataset and script used to find data normalization parameters.
- The neural net.
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
# Data editting tools
Scrapping the images is not always a reliable process, websites are prone to freeze/crash unexpectedly, thus producing unusable data. Additional camera issues may arise from environametal conditions such as fog or rain, or camera mulfunctions. 
For thses reasons it is highly recommended to manually browse through all images and delete any corrupted data.
After removing the data the scripts provided in ![images to data](https://github.com/ahaziv/surf-wave-classification/blob/main/data%20producers/image%20to%20data.py) will assist with two main functions:
1. Reorganize both image names and label files according to deleted data.
2. Crop and downsample images using a popup click tool, producing a 124X256 pxl images, ready as input for the CNN.

# Dataset
![wave1](https://github.com/ahaziv/surf-wave-classification/blob/main/image344.png) ![wave2](https://github.com/ahaziv/surf-wave-classification/blob/main/image335.png)
 of waves along with a csv label file containing info about the camera location, wave quality, date and some other additional info.
The dataset produced consist of 7412 RGB images from 32 different camera locations. Wave quality ratings ranged between 0 and 4. Distribution of ratings/locations can be seen below.
![wave1](https://github.com/ahaziv/surf-wave-classification/blob/main/Wave%20Grades%20Distribution.png)
As can be seen grade distribution is very uneven, which will most likely cause issues when predicting high ratings.

# CNN
To predict wave rating from image, a classification CNN was used. This implementation is not ideal since wave ratings are a continuous function and not a number of classes. But for the sake of an educational project, I implemented it according to the principles of KISS (keep it simple - stupid)
