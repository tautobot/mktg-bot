import unittest

from aqa.webdriver.selenium_webdriver import webdriver_local, webdriver_docker
from config import CHROME_DRI_ENV


class BaseTest(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self._outcome = None

    def setUp(self):
        if 'local' in CHROME_DRI_ENV:
            self.driver = webdriver_local()
        else:
            self.driver = webdriver_docker()
