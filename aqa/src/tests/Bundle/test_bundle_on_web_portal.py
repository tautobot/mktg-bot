from datetime import timedelta

from aqa.src.pages.web_portal.claim_page import WebPortalClaimPage
from aqa.src.pages.web_portal.home_page import WebPortalHomePage
from aqa.src.pages.web_portal.know_your_benefits_page import WebPortalKnowYourBenefitsPage
from aqa.src.pages.web_portal.login_page import LoginWebPortalPage
from aqa.src.pages.web_portal.my_insurance_page import WebPortalMyInsurancePage
from aqa.src.pages.web_portal.submit_claim_page import PhlInsuranceWebPortalSubmitClaimPage
from aqa.src.tests.base import BaseTest
from aqa.utils.generic import read_cell_in_excel_file
from aqa.utils.helper import sgt_today, set_default_password, kyc
from aqa.utils.webdriver_util import wait_for_loading_venta
from aqa.utils.enums import url, path, account

file_name  = 'bundle_template.xlsx'
excel_file = f'{path.fixture_dir}/{file_name}'


class Test(BaseTest):

    def setUp_fixture(self):
        self.email = read_cell_in_excel_file(excel_file, 'H2')
        self.pwd   = account.default_pwd
        set_default_password(self.email)
        kyc(self.email)

        self.login_page                     = LoginWebPortalPage(self.driver)
        self.home_page                      = WebPortalHomePage(self.driver)
        self.my_insurance_page              = WebPortalMyInsurancePage(self.driver)
        self.know_your_benefits_page        = WebPortalKnowYourBenefitsPage(self.driver)
        self.claim_page                     = WebPortalClaimPage(self.driver)
        self.submit_claim_page              = PhlInsuranceWebPortalSubmitClaimPage(self.driver)

    def test_your_coverage_section(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        products                = self.home_page.get_product_list()
        assert len(products)    == 4
        assert products[0].text == 'Personal Accident'
        assert products[1].text == 'Freelancer Earnings Protection'
        assert products[2].text == 'Term Life'
        assert products[3].text == 'Essentials'

    def test_my_insurance(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_my_insurance_page()

        wait_for_loading_venta(self.driver)
        self.my_insurance_page.click_on_active_tab()

        list_insurance       = self.my_insurance_page.get_list_active_product()
        list_product_name    = self.my_insurance_page.get_list_product_name()
        list_coverage_status = self.my_insurance_page.get_list_coverage_status()
        list_start_date      = self.my_insurance_page.get_list_start_date()

        assert len(list_insurance)          == 4
        assert list_product_name[0].text    in ['Personal Accident', 'FLEP', 'Term Life']
        assert list_coverage_status[0].text == 'ON'
        assert list_start_date[0].text      == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')

        assert list_product_name[1].text    in ['Personal Accident', 'FLEP', 'Term Life']
        assert list_coverage_status[1].text == 'ON'
        assert list_start_date[1].text      == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')

        assert list_product_name[2].text    in ['Personal Accident', 'FLEP', 'Term Life']
        assert list_coverage_status[2].text == 'ON'
        assert list_start_date[2].text      == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')

        assert list_product_name[3].text    in ['Personal Accident', 'FLEP', 'Term Life']
        assert list_coverage_status[3].text == 'ON'
        assert list_start_date[3].text      == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')

    def test_pa_info(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_pa_product()

        member_id         = self.know_your_benefits_page.get_member_id()
        start_date        = self.know_your_benefits_page.get_start_date()
        assert member_id  == read_cell_in_excel_file(excel_file, 'O2')
        assert start_date == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')

        #check Your Benefits section
        benefit_list                                   = self.know_your_benefits_page.get_your_benefits()
        assert len(benefit_list)                       == 4
        assert benefit_list[0].text.replace("\n", ' ') == '1 Accidental Death ₱ 42,500'
        assert benefit_list[1].text.replace("\n", ' ') == '2 Accidental Disablement ₱ 37,400'
        assert benefit_list[2].text.replace("\n", ' ') == '3 Unprovoked Murder and Assault ₱ 37,400'
        assert benefit_list[3].text.replace("\n", ' ') == '4 Accident Medical Expense (AME) ₱ 10,000'

    def test_flep_info(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_flep_product()

        member_id         = self.know_your_benefits_page.get_member_id()
        start_date        = self.know_your_benefits_page.get_start_date()
        assert member_id  == read_cell_in_excel_file(excel_file, 'O2')
        assert start_date == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')

        #check Your Benefits section
        benefit_list                                   = self.know_your_benefits_page.get_your_benefits()
        assert len(benefit_list)                       == 2
        assert benefit_list[0].text.replace("\n", ' ') == 'Inpatient Benefit ₱500/Day for Hospitalization (incl. HL) From Day 2, up to 60 days per year. Read More'
        assert benefit_list[1].text.replace("\n", ' ') == 'Outpatient Benefit ₱500/Day for Outpatient Medical Leave. From Day 5, up to 14 days per year. Read More'

    def test_essentials_info(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_essentials_product()

        member_id         = self.know_your_benefits_page.get_member_id()
        start_date        = self.know_your_benefits_page.get_start_date()
        assert member_id  == read_cell_in_excel_file(excel_file, 'N2')
        assert start_date == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')

        #check Your Benefits section
        benefit_list                                   = self.know_your_benefits_page.get_your_benefits()
        assert len(benefit_list)                       == 1
        assert benefit_list[0].text.replace("\n", ' ') == 'GP Consults Enjoy unlimited GP consults for FREE to ensure you’re always ready to work!'

    def test_termLife_info(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_termlife_product()

        wait_for_loading_venta(self.driver)
        member_id         = self.know_your_benefits_page.get_member_id()
        start_date        = self.know_your_benefits_page.get_start_date()
        assert member_id  == read_cell_in_excel_file(excel_file, 'O2')
        assert start_date == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')

        #check Your Benefits section
        benefit_list                = self.know_your_benefits_page.get_your_benefits()
        assert benefit_list[0].text == '₱ 10,000 Death due any cause'
        assert benefit_list[1].text == '₱ 50,000 Death due to COVID'
        assert len(benefit_list)    == 2

    def test_pa_claim_ip(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_pa_product()
        self.claim_page.choose_ip_popup()

        self.submit_claim_page.input_claim_details()
        self.submit_claim_page.input_accident_claim()
        self.submit_claim_page.upload_insurance_required_document()
        self.submit_claim_page.input_disbursement_details()
        self.submit_claim_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.submit_claim_page.is_claim_successful() is True

    def test_pa_claim_op(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_pa_product()
        self.claim_page.choose_op_popup()

        self.submit_claim_page.input_claim_details()
        self.submit_claim_page.input_accident_claim()
        self.submit_claim_page.upload_insurance_required_document()
        self.submit_claim_page.input_disbursement_details()
        self.submit_claim_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.submit_claim_page.is_claim_successful() is True

    def test_flep_claim_ip(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_flep_product()
        self.claim_page.choose_ip_popup()

        self.submit_claim_page.input_claim_details()
        self.submit_claim_page.input_accident_claim()
        self.submit_claim_page.upload_insurance_required_document()
        self.submit_claim_page.input_disbursement_details()
        self.submit_claim_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.submit_claim_page.is_claim_successful() is True

    def test_flep_claim_op(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_flep_product()
        self.claim_page.choose_op_popup()

        self.submit_claim_page.input_claim_details()
        self.submit_claim_page.input_accident_claim()
        self.submit_claim_page.upload_insurance_required_document()
        self.submit_claim_page.input_disbursement_details()
        self.submit_claim_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.submit_claim_page.is_claim_successful() is True

    def test_termlife_other_causes_claim(self):
        self.setUp_fixture()

        self.login_page.login_web_portal(self.email, self.pwd, url.url_web_portal_phl)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_termlife_product()

        self.submit_claim_page.choose_due_to_other_causes()
        self.submit_claim_page.choose_date_incident()
        self.submit_claim_page.upload_termlife_required_document()
        self.submit_claim_page.input_disbursement_details()
        self.submit_claim_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.submit_claim_page.is_claim_successful() is True
