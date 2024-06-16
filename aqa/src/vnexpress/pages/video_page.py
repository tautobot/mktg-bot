from selenium.webdriver.common.by import By

from aqa.utils.enums import URL
from aqa.utils.webdriver_util import wait_element, take_element_screenshot, isDisplayedLocator, wait


class VNEHomePage:
    def __init__(self, driver):
        self.driver                  = driver
        self.video_json              = By.XPATH, '//script[@type="application/ld+json" and contains(text(),"contentUrl")]/text()'
        self.video_text              = By.XPATH, '//script[contains(text(),".m3u8")]/text()'
        self.video_title             = By.ID, 'title_brandsafe_video'
        self.video_lead              = By.ID, 'lead_brandsafe_video'


    def get_video_link(self, url):
        pass
