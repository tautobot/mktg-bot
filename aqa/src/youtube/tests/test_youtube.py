from aqa.src.youtube.pages.home_page import HomePage
from aqa.src.base import BaseTest
from aqa.utils.webdriver_util import wait_for_loading
from aqa.utils.enums import URL, Languages, LoginTypes


class Test(BaseTest):

    def setUp_fixture(self):
        self.home_page = HomePage(self.driver)

    def test_login_adsense_lazada(self):
        self.setUp_fixture()
        self.home_page.login(URL.YOUTUBE, Languages.EN, LoginTypes.ACCOUNT)
        wait_for_loading()

