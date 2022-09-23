from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def chromedriver():
    chrome_driver_path = "chromedriver/chromedriver.exe"
    s = Service(chrome_driver_path)

    return webdriver.Chrome(service=s)
