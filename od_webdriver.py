from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

CHROME = "./webdriver/chromedriver.exe"
EDGE = "./webdriver/msedgedriver.exe"
FIREFOX = "./webdriver/geckodriver.exe"


def browserDriver(headless=True):
    from pathlib import Path

    if Path(CHROME).exists():
        return chromedriver(headless)
    elif Path(EDGE).exists():
        return edgedriver(headless)
    elif Path(FIREFOX).exists():
        return firefoxdriver(headless)
    else:
        return "Błąd: brak pliku sterownika przeglądarki!"


def chromedriver(headless=True):
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    chrome_driver_path = CHROME

    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

    s = Service(chrome_driver_path)

    return webdriver.Chrome(service=s, options=chrome_options)


def edgedriver(headless=True):
    from selenium.webdriver.edge.options import Options
    from selenium.webdriver.edge.service import Service

    edge_driver_path = EDGE

    edge_options = Options()
    if headless:
        edge_options.add_argument("headless")
        edge_options.add_argument("disable-gpu")

    s = Service(edge_driver_path)

    return webdriver.Edge(service=s, options=edge_options)


def firefoxdriver(headless=True):
    from os import path
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service

    ff_driver_path = FIREFOX

    ff_options = Options()
    if headless:
        ff_options.add_argument("--headless")
        ff_options.add_argument("--disable-gpu")

    s = Service(ff_driver_path, log_path=path.devnull)

    return webdriver.Edge(service=s, options=ff_options)
