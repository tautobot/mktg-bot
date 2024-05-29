from datetime import timedelta
from random import choice

from aqa.src.pages.tiktok.home_page import TiktokHomePage

from aqa.src.pages.web_portal.know_your_benefits_page import WebPortalKnowYourBenefitsPage
from aqa.src.pages.web_portal.login_page import LoginWebPortalPage
from aqa.src.pages.web_portal.submit_claim_page import SgInsuranceWebPortalSubmitClaimPage
from aqa.src.tests.base import BaseTest
from aqa.utils.helper import set_default_password, sgt_today
from aqa.utils.webdriver_util import wait_for_loading_venta, wait_for_loading
from aqa.utils.generic import read_cell_in_excel_file
from aqa.utils.enums import path, url, account, URL

# file_name  = 'pa_template.xlsx'
# excel_file = f'{path.fixture_dir}/{file_name}'


class Test(BaseTest):

    def setUp_fixture(self):
        # self.login_page                 = LoginWebPortalPage(self.driver)
        self.home_page                  = TiktokHomePage(self.driver)

    def test_login_tiktok(self):
        self.setUp_fixture()
        self.home_page.login_w_qr(URL.TIKTOK_HOME)
        wait_for_loading()
        