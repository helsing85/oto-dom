from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def chromedriver():
    chrome_driver_path = "webdriver/chromedriver.exe"
    s = Service(chrome_driver_path)

    return webdriver.Chrome(service=s)
