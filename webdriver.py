from selenium import webdriver
from selenium.webdriver.common.by import By


def chromedriver():
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    chrome_driver_path = "webdriver/chromedriver.exe"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    s = Service(chrome_driver_path)

    return webdriver.Chrome(service=s, options=chrome_options)


def edgedriver():
    from selenium.webdriver.edge.options import Options
    from selenium.webdriver.edge.service import Service

    edge_driver_path = "webdriver/msedgedriver.exe"

    edge_options = Options()
    edge_options.add_argument("headless")
    edge_options.add_argument("disable-gpu")

    s = Service(edge_driver_path)

    return webdriver.Edge(service=s, options=edge_options)


def firefoxdriver():
    from os import path
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service

    ff_driver_path = "webdriver/geckodriver.exe"

    ff_options = Options()
    ff_options.add_argument("--headless")
    ff_options.add_argument("--disable-gpu")

    s = Service(ff_driver_path, log_path=path.devnull)

    return webdriver.Edge(service=s, options=ff_options)
