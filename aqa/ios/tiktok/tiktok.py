import unittest
from aqa.webdriver.appium_weddriver import *


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = ios_webdriver(app_name='pocket')

    def tearDown(self): self.driver.quit()

    def test_login(self):
        self.driver.get('https://www.tiktok.com/login/')
