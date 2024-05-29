from aqa.src.pages.web_portal.claim_page import WebPortalClaimPage
from aqa.src.pages.web_portal.home_page import WebPortalHomePage
from aqa.src.pages.web_portal.know_your_benefits_page import WebPortalKnowYourBenefitsPage
from aqa.src.pages.web_portal.login_page import LoginWebPortalPage
from aqa.src.pages.web_portal.submit_claim_page import SgInsuranceWebPortalSubmitClaimPage
from aqa.src.tests.base import BaseTest
from aqa.utils.enums import path, url, account
from aqa.utils.helper import set_default_password
from aqa.utils.webdriver_util import wait_for_loading_venta
from aqa.utils.generic import read_cell_in_excel_file

file_name = 'pml_template.xlsx'
excel_file = f'{path.fixture_dir}/{file_name}'

class Test(BaseTest):

    # because PML and Flep have the same UI and logic for Claim, so we'll reuse it
    def setUp_fixture(self):
        self.login_page                 = LoginWebPortalPage(self.driver)
        self.home_page                  = WebPortalHomePage(self.driver)
        self.know_your_benefits_page    = WebPortalKnowYourBenefitsPage(self.driver)
        self.claim_page                 = WebPortalClaimPage(self.driver)
        self.claim_detail_page          = SgInsuranceWebPortalSubmitClaimPage(self.driver)

    def test_pml_hospital_accident_claim(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H2')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_pml_product()
        self.claim_page.choose_hospital_type()

        wait_for_loading_venta(self.driver)
        self.claim_detail_page.flep_input_accident_claim_detail()
        self.claim_detail_page.flep_hospital_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_pml_hospital_illness_claim(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H3')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_pml_product()
        self.claim_page.choose_hospital_type()

        wait_for_loading_venta(self.driver)
        self.claim_detail_page.flep_input_illness_claim_detail()
        self.claim_detail_page.flep_hospital_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_pml_medical_accident_claim(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H6')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_pml_product()
        self.claim_page.choose_medical_type()

        wait_for_loading_venta(self.driver)
        self.claim_detail_page.flep_input_accident_claim_detail()
        self.claim_detail_page.flep_medical_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_pml_medical_illness_claim(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H6')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_pml_product()
        self.claim_page.choose_medical_type()

        wait_for_loading_venta(self.driver)
        self.claim_detail_page.flep_input_illness_claim_detail()
        self.claim_detail_page.flep_medical_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True
