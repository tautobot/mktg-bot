import unittest

from aqa.webdriver.selenium_webdriver import webdriver_local, webdriver_docker
from config_local import CHROME_DRI_ENV


class BaseTest(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self._outcome = None

    def setUp(self):
        self.driver = webdriver_local() if CHROME_DRI_ENV == 'local' else webdriver_docker()
