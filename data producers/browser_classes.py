import time
from selenium.webdriver.firefox import service
from selenium.webdriver.chrome import service
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import service


class ChromeRecorder():
    def __init__(self, path: str):
        chrome_dr_path = os.path.join(path, 'chromedriver.exe')
        chrome_options = webdriver.ChromeOptions()
        userdatadir = r'C:\Users\ahazi\AppData\Local\Google\Chrome\User Data' #\Profile 4'
        chrome_options.add_argument(f"--user-data-dir={userdatadir}")
        self.driver = webdriver.Chrome(executable_path=chrome_dr_path, chrome_options=chrome_options)
        time.sleep(1)
        self.vars = {}

    def teardown(self):
        self.driver.quit()

    def open_page(self, url: str):
        self.driver.get(url)
        self.driver.set_window_size(956, 1600)
        time.sleep(1)
        element = self.driver.find_element(By.CSS_SELECTOR, ".jw-video")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        time.sleep(2)

    def take_screenshot(self, location):
        self.driver.get_screenshot_as_file(location)


class FirefoxRecorder():
    def __init__(self, ser: str):
        ser = service.Service(os.path.join(ser, '\geckodriver.exe'))
        self.driver = webdriver.Firefox(ser)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def open_page(self):
        self.driver.get("https://magicseaweed.com/Sao-Torpes-Pier-Surf-Report/4743/")
        self.driver.set_window_size(956, 1200)
        self.driver.find_element(By.CSS_SELECTOR, ".jw-video").click()
        self.driver.find_element(By.CSS_SELECTOR, ".jw-video").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".jw-video")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()