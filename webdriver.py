from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def chromedriver():
    chrome_driver_path = "webdriver/chromedriver.exe"

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    s = Service(chrome_driver_path)

    return webdriver.Chrome(service=s, options=chrome_options)
