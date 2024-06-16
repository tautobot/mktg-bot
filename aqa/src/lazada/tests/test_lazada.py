from aqa.src.lazada.pages.adsense_login_page import LazadaAdsensePage
from aqa.src.base import BaseTest
from aqa.utils.webdriver_util import wait_for_loading
from aqa.utils.enums import URL, Languages, LoginTypes


# file_name  = 'pa_template.xlsx'
# excel_file = f'{path.fixture_dir}/{file_name}'


class Test(BaseTest):

    def setUp_fixture(self):
        self.home_page = LazadaAdsensePage(self.driver)

    def test_login_adsense_lazada(self):
        print(f"self: {self}")
        self.setUp_fixture()
        self.home_page.login(URL.LAZADA_ADSENSE, Languages.EN, LoginTypes.ACCOUNT)
        wait_for_loading()

