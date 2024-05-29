from aqa.src.pages.web_portal.claim_page import WebPortalClaimPage
from aqa.src.pages.web_portal.home_page import WebPortalHomePage
from aqa.src.pages.web_portal.know_your_benefits_page import WebPortalKnowYourBenefitsPage
from aqa.src.pages.web_portal.login_page import LoginWebPortalPage
from aqa.src.pages.web_portal.submit_claim_page import SgInsuranceWebPortalSubmitClaimPage
from aqa.src.tests.base import BaseTest
from aqa.utils.enums import url, account
from aqa.utils.helper import sgt_today, set_default_password, build_coverage
from aqa.utils.webdriver_util import wait_for_loading_venta
from aqa.utils.generic import read_file
from config_local import WORKING_DIR_FIXTURE


class Test(BaseTest):

    def setUp_fixture(self):
        build_coverage()

        self.login_page                     = LoginWebPortalPage(self.driver)
        self.home_page                      = WebPortalHomePage(self.driver)
        self.know_your_benefits_page        = WebPortalKnowYourBenefitsPage(self.driver)
        self.claim_page                     = WebPortalClaimPage(self.driver)
        self.claim_detail_page              = SgInsuranceWebPortalSubmitClaimPage(self.driver)

    #region CDW
    def test_claim_cdw_with_document(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_option_B_expired_off.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_cdw_product()
        self.claim_page.click_on_yes_btn()

        self.claim_detail_page.cdw_option_B_input_claim_detail()
        self.claim_detail_page.cdw_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.cdw_click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_claim_cdw_without_document(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_option_A_inforce_on.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_cdw_product()
        self.claim_page.click_on_no_btn()

        self.claim_detail_page.cdw_option_A_input_claim_detail()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.cdw_click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_renew_policy(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_option_B_expired_off.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_cdw_product()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_renew_btn()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_on_pay_now_btn()

        wait_for_loading_venta(self.driver)
        assert self.know_your_benefits_page.is_renewal_successful() is True

    def test_cancel_renewal(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_option_A_inforce_on.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_cdw_product()

        wait_for_loading_venta(self.driver)
        start_date                  = self.know_your_benefits_page.get_start_date()
        policy_status               = self.know_your_benefits_page.get_policy_status()
        monthly_auto_renewal        = self.know_your_benefits_page.get_monthly_auto_renewal()
        assert start_date           == sgt_today().strftime('%d %b %Y')
        assert policy_status        == 'IN FORCE'
        assert monthly_auto_renewal == 'ON'
        assert self.know_your_benefits_page.is_cancelable() is True

        self.know_your_benefits_page.click_cancel_btn()
        self.know_your_benefits_page.click_confirm_btn()

        wait_for_loading_venta(self.driver)
        assert self.know_your_benefits_page.is_cancel_renewal_successful() is True
        self.know_your_benefits_page.click_back_to_home_button()

        wait_for_loading_venta(self.driver)
        renewal_after_cancel        = self.know_your_benefits_page.get_monthly_auto_renewal()
        assert renewal_after_cancel == 'OFF'
        assert self.know_your_benefits_page.is_renewable() is True

    def test_edit_plan_to_combined_excess(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_option_A_inforce_off.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_cdw_product()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_renew_btn()

        wait_for_loading_venta(self.driver)
        # price_before_edit
        price_before_edit = self.know_your_benefits_page.get_renew_price()

        # edit plan
        self.know_your_benefits_page.click_edit_btn()
        self.know_your_benefits_page.input_vehicle_number()
        self.know_your_benefits_page.cdw_edit_to_combined_excess()
        self.know_your_benefits_page.click_update_btn()

        wait_for_loading_venta(self.driver)
        # price after edit
        price_after_edit = self.know_your_benefits_page.get_renew_price()
        assert price_after_edit['premium']       != price_before_edit['premium']
        assert price_after_edit['gst']           != price_before_edit['gst']
        assert price_after_edit['total_premium'] != price_before_edit['total_premium']
        assert price_after_edit['charge_amount'] != price_before_edit['charge_amount']

        self.know_your_benefits_page.click_on_pay_now_btn()

        wait_for_loading_venta(self.driver)
        assert self.know_your_benefits_page.is_renewal_successful() is True

    def test_edit_plan_to_section(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_option_B_inforce_off.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_cdw_product()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_renew_btn()

        wait_for_loading_venta(self.driver)
        # price_before_edit
        price_before_edit = self.know_your_benefits_page.get_renew_price()

        # edit plan
        self.know_your_benefits_page.click_edit_btn()
        self.know_your_benefits_page.input_vehicle_number()
        self.know_your_benefits_page.cdw_edit_to_section()
        self.know_your_benefits_page.click_update_btn()

        wait_for_loading_venta(self.driver)
        # price after edit
        price_after_edit = self.know_your_benefits_page.get_renew_price()
        assert price_after_edit['premium']       != price_before_edit['premium']
        assert price_after_edit['gst']           != price_before_edit['gst']
        assert price_after_edit['total_premium'] != price_before_edit['total_premium']
        assert price_after_edit['charge_amount'] != price_before_edit['charge_amount']

        self.know_your_benefits_page.click_on_pay_now_btn()

        wait_for_loading_venta(self.driver)
        assert self.know_your_benefits_page.is_renewal_successful() is True
    #endregion CDW

    #region CDW plus
    def test_claim_cdw_plus_with_document(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_plus_option_B_expired_off.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_cdw_plus_product()
        self.claim_page.click_on_yes_btn()

        self.claim_detail_page.cdw_option_B_input_claim_detail()
        self.claim_detail_page.cdw_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.cdw_click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_claim_cdw_plus_without_document(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_plus_option_A_inforce_on.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_cdw_plus_product()
        self.claim_page.click_on_no_btn()

        self.claim_detail_page.cdw_option_A_input_claim_detail()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.cdw_click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_cdw_plus_renew_policy(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_plus_option_B_expired_off.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_cdw_plus_product()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_renew_btn()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_on_pay_now_btn()

        wait_for_loading_venta(self.driver)
        assert self.know_your_benefits_page.is_renewal_successful() is True

    def test_cdw_plus_cancel_renewal(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_plus_option_A_inforce_on.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_cdw_plus_product()

        wait_for_loading_venta(self.driver)
        start_date                  = self.know_your_benefits_page.get_start_date()
        policy_status               = self.know_your_benefits_page.get_policy_status()
        monthly_auto_renewal        = self.know_your_benefits_page.get_monthly_auto_renewal()
        assert start_date           == sgt_today().strftime('%d %b %Y')
        assert policy_status        == 'IN FORCE'
        assert monthly_auto_renewal == 'ON'
        assert self.know_your_benefits_page.is_cancelable() is True

        self.know_your_benefits_page.click_cancel_btn()
        self.know_your_benefits_page.click_confirm_btn()

        wait_for_loading_venta(self.driver)
        assert self.know_your_benefits_page.is_cancel_renewal_successful() is True
        self.know_your_benefits_page.click_back_to_home_button()

        wait_for_loading_venta(self.driver)
        renewal_after_cancel        = self.know_your_benefits_page.get_monthly_auto_renewal()
        assert renewal_after_cancel == 'OFF'
        assert self.know_your_benefits_page.is_renewable() is True

    def test_cdw_plus_edit_plan_to_combined_excess(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_plus_option_A_inforce_off.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_cdw_plus_product()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_renew_btn()

        wait_for_loading_venta(self.driver)
        # price_before_edit
        price_before_edit = self.know_your_benefits_page.get_renew_price()

        # edit plan
        self.know_your_benefits_page.click_edit_btn()
        self.know_your_benefits_page.input_vehicle_number()
        self.know_your_benefits_page.cdw_edit_to_combined_excess()
        self.know_your_benefits_page.click_update_btn()

        wait_for_loading_venta(self.driver)
        # price after edit
        price_after_edit = self.know_your_benefits_page.get_renew_price()
        assert price_after_edit['premium']       != price_before_edit['premium']
        assert price_after_edit['gst']           != price_before_edit['gst']
        assert price_after_edit['total_premium'] != price_before_edit['total_premium']
        assert price_after_edit['charge_amount'] != price_before_edit['charge_amount']

        self.know_your_benefits_page.click_on_pay_now_btn()

        wait_for_loading_venta(self.driver)
        assert self.know_your_benefits_page.is_renewal_successful() is True

    def test_cdw_plus_edit_plan_to_section(self):
        self.setUp_fixture()

        email = read_file(f'{WORKING_DIR_FIXTURE}/cdw_plus_option_B_inforce_off.txt')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_cdw_plus_product()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_renew_btn()

        wait_for_loading_venta(self.driver)
        # price_before_edit
        price_before_edit = self.know_your_benefits_page.get_renew_price()

        # edit plan
        self.know_your_benefits_page.click_edit_btn()
        self.know_your_benefits_page.input_vehicle_number()
        self.know_your_benefits_page.cdw_edit_to_section()
        self.know_your_benefits_page.click_update_btn()

        wait_for_loading_venta(self.driver)
        # price after edit
        price_after_edit = self.know_your_benefits_page.get_renew_price()
        assert price_after_edit['premium']       != price_before_edit['premium']
        assert price_after_edit['gst']           != price_before_edit['gst']
        assert price_after_edit['total_premium'] != price_before_edit['total_premium']
        assert price_after_edit['charge_amount'] != price_before_edit['charge_amount']

        self.know_your_benefits_page.click_on_pay_now_btn()

        wait_for_loading_venta(self.driver)
        assert self.know_your_benefits_page.is_renewal_successful() is True

    #endregion CDW plus