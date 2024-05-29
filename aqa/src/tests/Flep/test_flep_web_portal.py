from datetime import timedelta

from aqa.src.pages.web_portal.claim_page import WebPortalClaimPage
from aqa.src.pages.web_portal.home_page import WebPortalHomePage
from aqa.src.pages.web_portal.know_your_benefits_page import WebPortalKnowYourBenefitsPage
from aqa.src.pages.web_portal.login_page import LoginWebPortalPage
from aqa.src.pages.web_portal.submit_claim_page import SgInsuranceWebPortalSubmitClaimPage
from aqa.src.tests.base import BaseTest
from aqa.utils.enums import path, url, account
from aqa.utils.helper import set_default_password, sgt_today
from aqa.utils.webdriver_util import wait_for_loading_venta
from aqa.utils.generic import read_cell_in_excel_file

file_name  = 'flep_template.xlsx'
excel_file = f'{path.fixture_dir}/{file_name}'

class Test(BaseTest):

    def setUp_fixture(self):
        self.login_page                 = LoginWebPortalPage(self.driver)
        self.home_page                  = WebPortalHomePage(self.driver)
        self.know_your_benefits_page    = WebPortalKnowYourBenefitsPage(self.driver)
        self.claim_page                 = WebPortalClaimPage(self.driver)
        self.claim_detail_page          = SgInsuranceWebPortalSubmitClaimPage(self.driver)

    def test_flep_hospital_accident_claim(self):
        self.setUp_fixture()
        email = read_cell_in_excel_file(excel_file, 'H2')
        pwd = account.default_pwd
        set_default_password(email)

        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_flep_product()
        self.claim_page.click_on_proceed_btn()
        self.claim_page.choose_hospital_type()

        wait_for_loading_venta(self.driver)
        self.claim_detail_page.flep_input_accident_claim_detail()
        self.claim_detail_page.flep_hospital_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_flep_hospital_illness_claim(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H2')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_flep_product()
        self.claim_page.click_on_proceed_btn()
        self.claim_page.choose_hospital_type()

        wait_for_loading_venta(self.driver)
        self.claim_detail_page.flep_input_illness_claim_detail()
        self.claim_detail_page.flep_hospital_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_flep_medical_accident_claim(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H2')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_flep_product()
        self.claim_page.click_on_proceed_btn()
        self.claim_page.choose_medical_type()

        wait_for_loading_venta(self.driver)
        self.claim_detail_page.flep_input_accident_claim_detail()
        self.claim_detail_page.flep_medical_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_flep_medical_illness_claim(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H2')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_flep_product()
        self.claim_page.click_on_proceed_btn()
        self.claim_page.choose_medical_type()

        wait_for_loading_venta(self.driver)
        self.claim_detail_page.flep_input_illness_claim_detail()
        self.claim_detail_page.flep_medical_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_verify_product_information(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, f'H7')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_flep_product()

        wait_for_loading_venta(self.driver)
        start_date                  = self.know_your_benefits_page.get_start_date()
        policy_status               = self.know_your_benefits_page.get_policy_status()
        # monthly_auto_renewal        = self.know_your_benefits_page.get_monthly_auto_renewal()
        assert start_date           == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')
        assert policy_status        == 'IN FORCE'
        # assert monthly_auto_renewal == 'OFF'
        # assert self.know_your_benefits_page.is_renewable() is True

        benefit_list = self.know_your_benefits_page.get_your_benefits()
        assert benefit_list[0].text.replace("\n", ' ') == 'Inpatient Benefit $80/Day for Hospitalization (incl. HL) From Day 1, up to 60 days per year. Read More'
        assert benefit_list[1].text.replace("\n", ' ') == 'Outpatient Benefit $80/Day for Outpatient Medical Leave. From Day 5, up to 14 days per year. Read More'

    # def test_renew_policy(self):
    #     self.setUp_fixture()
    #
    #     email = read_cell_in_excel_file(excel_file, f'H3')
    #     pwd = account.default_pwd
    #     set_default_password(email)
    #     self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)
    #
    #     wait_for_loading_venta(self.driver)
    #     self.home_page.click_on_flep_product()
    #
    #     wait_for_loading_venta(self.driver)
    #     self.know_your_benefits_page.click_renew_btn()
    #
    #     wait_for_loading_venta(self.driver)
    #     # verify price
    #     actual_price = self.know_your_benefits_page.get_renew_price()
    #     assert actual_price['premium']       == '$25.00/month'
    #     assert actual_price['gst']           == '$2.00'
    #     assert actual_price['total_premium'] == '$27.00/month'
    #     assert actual_price['charge_amount'] == '$27.00/month'
    #
    #     self.know_your_benefits_page.add_payment_detail()
    #     wait_for_loading_venta(self.driver)
    #
    #     self.know_your_benefits_page.click_on_pay_now_btn()
    #     assert self.know_your_benefits_page.is_renewal_successful() is True

    # def test_cancel_renewal(self):
    #     self.setUp_fixture()
    #
    #     email = read_cell_in_excel_file(excel_file, f'H4')
    #     pwd = account.default_pwd
    #     set_default_password(email)
    #     self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)
    #
    #     wait_for_loading_venta(self.driver)
    #     self.home_page.click_on_flep_product()
    #
    #     wait_for_loading_venta(self.driver)
    #     start_date                  = self.know_your_benefits_page.get_start_date()
    #     policy_status               = self.know_your_benefits_page.get_policy_status()
    #     monthly_auto_renewal        = self.know_your_benefits_page.get_monthly_auto_renewal()
    #     assert start_date           == (sgt_today() + timedelta(days=32)).strftime('%d %b %Y')
    #     assert policy_status        == 'PROCESSING'
    #     assert monthly_auto_renewal == 'OFF'
    #
    #     wait_for_loading_venta(self.driver)
    #     self.know_your_benefits_page.click_renew_btn()
    #     self.know_your_benefits_page.add_payment_detail()
    #
    #     wait_for_loading_venta(self.driver)
    #     self.know_your_benefits_page.click_on_pay_now_btn()
    #
    #     wait_for_loading_venta(self.driver)
    #     assert self.know_your_benefits_page.is_renewal_successful() is True
    #
    #     wait_for_loading_venta(self.driver)
    #     assert self.know_your_benefits_page.is_cancelable() is True
    #
    #     self.know_your_benefits_page.click_cancel_btn()
    #     self.know_your_benefits_page.click_confirm_btn()
    #
    #     wait_for_loading_venta(self.driver)
    #     assert self.know_your_benefits_page.is_cancel_renewal_successful() is True
    #     self.know_your_benefits_page.click_back_to_home_button()
    #
    #     renewal_after_cancel        = self.know_your_benefits_page.get_monthly_auto_renewal()
    #     assert renewal_after_cancel == 'OFF'
    #     assert self.know_your_benefits_page.is_renewable() is True

    # def test_verify_user_cannot_renew_without_card(self):
    #     self.setUp_fixture()
    #
    #     email = read_cell_in_excel_file(excel_file, 'H5')
    #     pwd = account.default_pwd
    #     set_default_password(email)
    #     self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)
    #
    #     wait_for_loading_venta(self.driver)
    #     self.home_page.click_on_flep_product()
    #
    #     wait_for_loading_venta(self.driver)
    #     self.know_your_benefits_page.click_renew_btn()
    #
    #     wait_for_loading_venta(self.driver)
    #     # verify price
    #     actual_price = self.know_your_benefits_page.get_renew_price()
    #     assert actual_price['premium']       == '$25.00/month'
    #     assert actual_price['gst']           == '$2.00'
    #     assert actual_price['total_premium'] == '$27.00/month'
    #     assert actual_price['charge_amount'] == '$27.00/month'
    #
    #     self.know_your_benefits_page.click_on_pay_now_btn()
    #     assert self.know_your_benefits_page.payment_method_required_error_msg() is True

    # def test_verify_user_already_has_card_can_renew_without_card(self):
    #     self.setUp_fixture()
    #
    #     email = read_cell_in_excel_file(excel_file, 'H6')
    #     pwd = account.default_pwd
    #     set_default_password(email)
    #     self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)
    #
    #     wait_for_loading_venta(self.driver)
    #     self.home_page.active_Ecard()
    #
    #     wait_for_loading_venta(self.driver)
    #     self.home_page.click_on_got_it_btn()
    #     self.home_page.click_on_flep_product()
    #
    #     wait_for_loading_venta(self.driver)
    #     self.know_your_benefits_page.click_renew_btn()
    #
    #     wait_for_loading_venta(self.driver)
    #     # verify price
    #     actual_price = self.know_your_benefits_page.get_renew_price()
    #     assert actual_price['premium']       == '$25.00/month'
    #     assert actual_price['gst']           == '$2.00'
    #     assert actual_price['total_premium'] == '$27.00/month'
    #     assert actual_price['charge_amount'] == '$27.00/month'
    #
    #     assert self.know_your_benefits_page.is_already_has_card() is True
    #
    #     self.know_your_benefits_page.click_on_pay_now_btn()
    #     assert self.know_your_benefits_page.is_renewal_successful() is True
