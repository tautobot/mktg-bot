# features/environment.py

from aqa.webdriver.selenium_webdriver import webdriver_local, webdriver_docker
from config_local import CHROME_DRI_ENV


def before_all(context):
    context.driver = webdriver_local() if CHROME_DRI_ENV == 'local' else webdriver_docker()


def after_all(context):
    # cleanup after tests run
    context.driver.quit()