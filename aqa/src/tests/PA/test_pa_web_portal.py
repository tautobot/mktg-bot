from datetime import timedelta
from random import choice

from aqa.src.pages.web_portal.claim_page import WebPortalClaimPage
from aqa.src.pages.web_portal.home_page import WebPortalHomePage
from aqa.src.pages.web_portal.know_your_benefits_page import WebPortalKnowYourBenefitsPage
from aqa.src.pages.web_portal.login_page import LoginWebPortalPage
from aqa.src.pages.web_portal.submit_claim_page import SgInsuranceWebPortalSubmitClaimPage
from aqa.src.tests.base import BaseTest
from aqa.utils.helper import set_default_password, sgt_today
from aqa.utils.webdriver_util import wait_for_loading_venta
from aqa.utils.generic import read_cell_in_excel_file
from aqa.utils.enums import path, url, account

file_name  = 'pa_template.xlsx'
excel_file = f'{path.fixture_dir}/{file_name}'

class Test(BaseTest):

    def setUp_fixture(self):
        self.login_page                 = LoginWebPortalPage(self.driver)
        self.home_page                  = WebPortalHomePage(self.driver)
        self.know_your_benefits_page    = WebPortalKnowYourBenefitsPage(self.driver)
        self.claim_page                 = WebPortalClaimPage(self.driver)
        self.claim_detail_page          = SgInsuranceWebPortalSubmitClaimPage(self.driver)

    def test_pa_claim(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H2')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.go_to_claim_page()

        wait_for_loading_venta(self.driver)
        self.claim_page.choose_pa_product()
        self.claim_page.click_on_proceed_btn()

        self.claim_detail_page.pa_input_claim_detail()
        self.claim_detail_page.pa_upload_required_doc()
        self.claim_detail_page.input_disbursement_detail()
        self.claim_detail_page.click_checkbox()
        self.claim_detail_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_detail_page.is_claim_successful() is True

    def test_verify_product_information(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H8')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_pa_product()

        wait_for_loading_venta(self.driver)
        start_date                  = self.know_your_benefits_page.get_start_date()
        policy_status               = self.know_your_benefits_page.get_policy_status()
        monthly_auto_renewal        = self.know_your_benefits_page.get_monthly_auto_renewal()
        assert start_date           == (sgt_today() - timedelta(days=1)).strftime('%d %b %Y')
        assert policy_status        == 'IN FORCE'
        assert monthly_auto_renewal == 'OFF'
        assert self.know_your_benefits_page.is_renewable() is True

        benefit_list = self.know_your_benefits_page.get_your_benefits()
        assert benefit_list[0].text.replace("\n", ' ') == '1 Accidental Death $50,000'
        assert benefit_list[1].text.replace("\n", ' ') == '2 Permanent Disablement due to Accident For full disability coverage and benefits, please refer to policy wording $50,000'
        assert benefit_list[2].text.replace("\n", ' ') == '3 Medical Expense Reimbursement Only for accident related medical claims from Hospital or Clinic is accepted $500'
        assert benefit_list[3].text.replace("\n", ' ') == '4 Daily Hospital Income $50'

    def test_renew_policy(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H3')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_pa_product()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_renew_btn()

        wait_for_loading_venta(self.driver)
        # verify price
        actual_price = self.know_your_benefits_page.get_renew_price()
        assert actual_price['premium']       == '$1.33/month'
        assert actual_price['gst']           == '$0.12'
        assert actual_price['total_premium'] == '$1.45/month'
        assert actual_price['charge_amount'] == '$1.45/month'

        self.know_your_benefits_page.add_payment_detail()
        wait_for_loading_venta(self.driver)

        self.know_your_benefits_page.click_on_pay_now_btn()
        assert self.know_your_benefits_page.is_renewal_successful() is True

    def test_renew_policy_change_level_coverage(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H4')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_pa_product()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_renew_btn()

        gst = ''
        total_amount = ''
        coverage = choice(['$20,000', '$50,000', '$100,000'])
        self.know_your_benefits_page.change_level_of_coverage(coverage)
        if coverage == '$20,000':  total_amount = '$1.45'; gst = '$0.12'
        if coverage == '$50,000':  total_amount = '$3.49'; gst = '$0.29'
        if coverage == '$100,000': total_amount = '$6.32'; gst = '$0.52'

        wait_for_loading_venta(self.driver)
        # verify price
        actual_price = self.know_your_benefits_page.get_renew_price()
        assert actual_price['gst']           == gst
        assert actual_price['total_premium'] == f'{total_amount}/month'
        assert actual_price['charge_amount'] == f'{total_amount}/month'

        self.know_your_benefits_page.add_payment_detail()
        wait_for_loading_venta(self.driver)

        self.know_your_benefits_page.click_on_pay_now_btn()
        assert self.know_your_benefits_page.is_renewal_successful() is True

    def test_cancel_renewal(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, f'H2')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_pa_product()

        wait_for_loading_venta(self.driver)
        start_date                  = self.know_your_benefits_page.get_start_date()
        policy_status               = self.know_your_benefits_page.get_policy_status()
        monthly_auto_renewal        = self.know_your_benefits_page.get_monthly_auto_renewal()
        assert start_date           == (sgt_today() - timedelta(days=32)).strftime('%d %b %Y')
        assert policy_status        == 'TERMINATED'
        assert monthly_auto_renewal == 'OFF'

        self.know_your_benefits_page.click_renew_btn()
        self.know_your_benefits_page.add_payment_detail()
        wait_for_loading_venta(self.driver)

        self.know_your_benefits_page.click_on_pay_now_btn()
        assert self.know_your_benefits_page.is_renewal_successful() is True
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

    def test_verify_user_cannot_renew_without_card(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H5')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_pa_product()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_renew_btn()

        wait_for_loading_venta(self.driver)
        # verify price
        actual_price = self.know_your_benefits_page.get_renew_price()
        assert actual_price['premium']       == '$1.33/month'
        assert actual_price['gst']           == '$0.12'
        assert actual_price['total_premium'] == '$1.45/month'
        assert actual_price['charge_amount'] == '$1.45/month'

        self.know_your_benefits_page.click_on_pay_now_btn()
        assert self.know_your_benefits_page.payment_method_required_error_msg() is True

    def test_verify_user_already_has_card_can_renew_without_card(self):
        self.setUp_fixture()

        email = read_cell_in_excel_file(excel_file, 'H6')
        pwd = account.default_pwd
        set_default_password(email)
        self.login_page.login_web_portal(email, pwd, url.url_web_portal_sg)

        wait_for_loading_venta(self.driver)
        self.home_page.active_Ecard()

        wait_for_loading_venta(self.driver)
        self.home_page.click_on_got_it_btn()
        self.home_page.click_on_pa_product()

        wait_for_loading_venta(self.driver)
        self.know_your_benefits_page.click_renew_btn()

        wait_for_loading_venta(self.driver)
        # verify price
        actual_price = self.know_your_benefits_page.get_renew_price()
        assert actual_price['premium']       == '$1.33/month'
        assert actual_price['gst']           == '$0.12'
        assert actual_price['total_premium'] == '$1.45/month'
        assert actual_price['charge_amount'] == '$1.45/month'

        assert self.know_your_benefits_page.is_already_has_card() is True

        self.know_your_benefits_page.click_on_pay_now_btn()
        assert self.know_your_benefits_page.is_renewal_successful() is True
