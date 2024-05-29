from datetime import timedelta

from aqa.src.pages.web_portal.claim_page import WebPortalClaimPage
from aqa.src.pages.web_portal.home_page import WebPortalHomePage
from aqa.src.pages.web_portal.know_your_benefits_page import WebPortalKnowYourBenefitsPage
from aqa.src.pages.web_portal.login_page import LoginWebPortalPage
from aqa.src.pages.web_portal.submit_claim_page import EbWebPortalSubmitClaimPage
from aqa.src.tests.base import BaseTest
from aqa.utils.enums import url, account, path
from aqa.utils.helper import sgt_today, set_default_password, kyc
from aqa.utils.webdriver_util import wait_for_loading_venta
from aqa.utils.generic import read_cell_in_excel_file

excel_file = f'{path.fixture_dir}/health_template.xlsx'

class Test(BaseTest):

    def setUp_fixture(self):
        self.employee_email = read_cell_in_excel_file(excel_file, 'K2')
        self.employee_pwd   = account.default_pwd
        set_default_password(self.employee_email)
        kyc(self.employee_email)

        self.web_portal_login_page                  = LoginWebPortalPage(self.driver)
        self.web_portal_home_page                   = WebPortalHomePage(self.driver)
        self.web_portal_know_your_benefits_page     = WebPortalKnowYourBenefitsPage(self.driver)
        self.web_portal_claim_page                  = WebPortalClaimPage(self.driver)
        self.web_portal_submit_claim_page           = EbWebPortalSubmitClaimPage(self.driver)

    def test_verify_health_benefits(self):
        self.setUp_fixture()

        self.web_portal_login_page.login_web_portal(self.employee_email, self.employee_pwd, url.url_web_portal_phl)
        wait_for_loading_venta(self.driver)

        self.web_portal_home_page.click_on_health_product()
        wait_for_loading_venta(self.driver)

        member_id         = self.web_portal_know_your_benefits_page.get_member_id()
        start_date        = self.web_portal_know_your_benefits_page.get_start_date()
        assert member_id  == 'PENDING'
        assert start_date == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')

        #check Your Benefits section
        benefit_list                                   = self.web_portal_know_your_benefits_page.get_your_benefits()
        assert benefit_list[0].text.replace("\n", ' ') == 'Inpatient Benefit Covers inpatient treatment including pre and post hospitalization and other related benefits.'
        assert benefit_list[1].text.replace("\n", ' ') == 'Outpatient Benefit Covers consultations and treatments provided by a specialist or medical practitioner including emergency treatment and minor surgeries when an overnight stay in hospital is not necessary.'
        assert benefit_list[2].text.replace("\n", ' ') == 'Annual Physical Examination Benefit Helps you to discover the general status of your health through regular checkup carried out at/provided by certain accredited APE providers.'
        assert len(benefit_list)                       == 3

    def test_claim_ip_on_web_portal(self):
        self.setUp_fixture()

        self.web_portal_login_page.login_web_portal(self.employee_email, self.employee_pwd, url.url_web_portal_phl)
        wait_for_loading_venta(self.driver)

        self.web_portal_home_page.go_to_claim_page()
        wait_for_loading_venta(self.driver)

        self.web_portal_claim_page.choose_health_product()
        self.web_portal_claim_page.choose_ip_popup()

        self.web_portal_submit_claim_page.choose_date_of_accident()
        self.web_portal_submit_claim_page.input_eb_inpatient_required_document()
        self.web_portal_submit_claim_page.input_disbursement_details()
        self.web_portal_submit_claim_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.web_portal_submit_claim_page.is_claim_successful() is True

    def test_claim_op_on_web_portal(self):
        self.setUp_fixture()

        self.web_portal_login_page.login_web_portal(self.employee_email, self.employee_pwd, url.url_web_portal_phl)
        wait_for_loading_venta(self.driver)

        self.web_portal_home_page.go_to_claim_page()
        wait_for_loading_venta(self.driver)

        self.web_portal_claim_page.choose_health_product()
        self.web_portal_claim_page.choose_op_popup()

        self.web_portal_submit_claim_page.choose_date_of_accident()
        self.web_portal_submit_claim_page.input_eb_outpatient_required_document()
        self.web_portal_submit_claim_page.input_disbursement_details()
        self.web_portal_submit_claim_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.web_portal_submit_claim_page.is_claim_successful() is True
