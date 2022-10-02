from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By


def chromedriver():
    chrome_driver_path = "webdriver/chromedriver.exe"

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    s = Service(chrome_driver_path)

    return webdriver.Chrome(service=s, options=chrome_options)


def edgedriver():
    edge_driver_path = "webdriver/msedgedriver.exe"

    edge_options = Options()
    edge_options.add_argument("headless")
    edge_options.add_argument("disable-gpu")

    s = Service(edge_driver_path)

    return webdriver.Edge(service=s, options=edge_options)
