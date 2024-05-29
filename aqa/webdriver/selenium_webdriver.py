import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config_local import headless
from selenium.webdriver.chrome.service import Service

filepath = os.path.dirname(__file__)
IMPLICITLY_WAIT = 5


def options():
    chrome_options = Options()
    if headless == 'yes':
        chrome_options.add_argument("--headless")
    else:
        pass

    return chrome_options


def webdriver_local():
    chrome_options = options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(IMPLICITLY_WAIT)
    driver.maximize_window()
    return driver


def webdriver_docker():
    options().add_argument(webdriver.ChromeOptions)
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options()
    )
    driver.implicitly_wait(IMPLICITLY_WAIT)
    driver.maximize_window()
    return driver
