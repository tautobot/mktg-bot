from aqa.src.tiktok.pages.home_page import TiktokHomePage

from aqa.src.base import BaseTest
from aqa.utils.enums import URL


class Test(BaseTest):

    def setUp_fixture(self):
        # self.login_page                 = LoginWebPortalPage(self.driver)
        self.home_page                  = TiktokHomePage(self.driver)

    def test_login_tiktok(self):
        self.setUp_fixture()
        self.home_page.login_w_qr(URL.TIKTOK)

    # def test_wait_tiktok_to_see_qr(self):
    #     time.sleep(1000)
