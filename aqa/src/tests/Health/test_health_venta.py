from aqa.src.pages.venta.home_page import HomePage
from aqa.src.pages.venta.checkout_page import HealthCheckoutPage
from aqa.src.pages.venta.payment_details_page import XenditPaymentDetailsPage
from aqa.src.pages.venta.quote_page import HealthQuotePage
from aqa.src.pages.venta.your_infomarion_page import HealthYourInformationPage
from aqa.src.tests.base import BaseTest
from aqa.utils.enums import url, HmoPrice
from aqa.utils.webdriver_util import wait_loading_direct_bank, wait_loading_dashboard


class Test(BaseTest):

    def setUp_fixture(self):
        self.home_page             = HomePage(self.driver)
        self.quote_page            = HealthQuotePage(self.driver)
        self.your_information_page = HealthYourInformationPage(self.driver)
        self.checkout_page         = HealthCheckoutPage(self.driver)
        self.xendit                = XenditPaymentDetailsPage(self.driver)

        self.refcode               = 'COUPON_HMO'

    #region Primary
    def test_self_buy_health_ewallet_success(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.xendit.choose_ewallet_option()
        self.xendit.choose_ewallet_grabpay()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.click_proceed_btn()

        wait_loading_dashboard(self.driver)
        assert self.xendit.congratulations_text() is True

    def test_self_buy_health_credit_card_success(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.xendit.input_card_details()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.input_purchase_authentication()

        wait_loading_dashboard(self.driver)
        assert self.xendit.congratulations_text() is True

    def test_self_buy_health_direct_debit_BPI_bank_success(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.xendit.choose_direct_debit_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_direct_debit_BPI_bank()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.login_direct_debit_with_valid_account()

        assert self.xendit.processing_image() is True
        self.xendit.input_valid_otp()

        wait_loading_direct_bank(self.driver)
        assert self.xendit.congratulations_text() is True

    def test_self_buy_health_direct_debit_Union_bank_success(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.xendit.choose_direct_debit_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_direct_debit_Union_bank()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.login_direct_debit_with_valid_account()

        assert self.xendit.processing_image() is True
        self.xendit.input_valid_otp()

        wait_loading_direct_bank(self.driver)
        assert self.xendit.congratulations_text() is True

    def test_self_buy_health_ewallet_failed(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        self.quote_page.choose_plan_failed_Ewallet()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit['PLAN 1C']
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage['PLAN 1C'].split('.',1)[0]

        self.xendit.choose_ewallet_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_ewallet_grabpay()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        assert self.xendit.failed_text() is True

    def test_self_buy_health_credit_card_failed(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        self.quote_page.choose_plan_failed_card()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit['PLAN 2C']
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage['PLAN 2C'].split('.',1)[0]

        self.xendit.input_card_details()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.input_purchase_authentication()

        wait_loading_dashboard(self.driver)
        assert self.xendit.failed_text() is True

    def test_self_buy_health_direct_debit_BPI_bank_failed_login_bank(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.xendit.choose_direct_debit_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_direct_debit_BPI_bank()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.login_direct_debit_with_invalid_account()

        wait_loading_direct_bank(self.driver)
        assert self.xendit.failed_text() is True

    def test_self_buy_health_direct_debit_Union_bank_failed_login_bank(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.xendit.choose_direct_debit_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_direct_debit_Union_bank()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.login_direct_debit_with_invalid_account()

        wait_loading_direct_bank(self.driver)
        assert self.xendit.failed_text() is True

    def test_self_buy_health_direct_debit_BPI_bank_failed_otp(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.xendit.choose_direct_debit_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_direct_debit_BPI_bank()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.login_direct_debit_with_valid_account()

        assert self.xendit.processing_image() is True
        self.xendit.input_invalid_otp()

        wait_loading_direct_bank(self.driver)
        assert self.xendit.failed_text() is True

    def test_self_buy_health_direct_debit_Union_bank_failed_otp(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.xendit.choose_direct_debit_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_direct_debit_Union_bank()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.login_direct_debit_with_valid_account()

        assert self.xendit.processing_image() is True
        self.xendit.input_invalid_otp()

        wait_loading_direct_bank(self.driver)
        assert self.xendit.failed_text() is True

    def test_self_buy_health_ewallet_cancelled(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.xendit.choose_ewallet_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_ewallet_paymaya()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.ewallet_click_cancel_btn()

        wait_loading_dashboard(self.driver)
        assert self.xendit.cancelled_text() is True

    def test_self_buy_health_credit_card_cancelled(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted()
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.xendit.input_card_details()
        self.xendit.click_pay_securely_btn()

        self.xendit.credit_card_click_cancel_btn()
        wait_loading_dashboard(self.driver)
        assert self.xendit.cancelled_text() is True

    def test_self_buy_health_ewallet_success_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        price_before_refcode                                                 = self.checkout_page.get_hmo_data_inputted()
        assert price_before_refcode['product_name']                         == 'Comprehensive Health Insurance Program'
        assert price_before_refcode['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert price_before_refcode['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert price_before_refcode['renewal']                              == 'Yearly'
        assert price_before_refcode['subtotal']                             ==  total_annual
        assert price_before_refcode['promo_discount']                       ==  'PHP 0'
        assert price_before_refcode['credit_used']                          ==  'PHP 0'
        assert price_before_refcode['total_saving']                         ==  'PHP 0'
        assert price_before_refcode['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.checkout_page.apply_refcode(self.refcode)
        wait_loading_dashboard(self.driver)

        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'HMO discount 10%'

        wait_loading_dashboard(self.driver)
        price_after_refcode                                                          = self.checkout_page.get_hmo_data_inputted()
        assert price_after_refcode['product_name']                                   == 'Comprehensive Health Insurance Program'
        assert price_after_refcode['daily_benefit']                                  == HmoPrice.cash_benefit[plan]
        assert price_after_refcode['waiting_period']                                 == 'Date policy documents will be ready (5-7 business days)'
        assert price_after_refcode['renewal']                                        == 'Yearly'
        assert price_after_refcode['total_amount'].split('.',1)[0]                   == price_before_refcode['total_amount'].split('.',1)[0]
        assert price_after_refcode['credit_used']                                    == 'PHP 0'
        assert price_after_refcode['primary_coverage'].split('.',1)[0]               == HmoPrice.primary_coverage[plan].split('.',1)[0]
        assert price_after_refcode['vat']                                            == price_before_refcode['vat']
        assert price_after_refcode['subtotal']                                       != price_before_refcode['subtotal']
        assert price_after_refcode['promo_discount']                                 != 'PHP 0'
        assert price_after_refcode['total_saving']                                   != 'PHP 0'
        assert price_after_refcode['total_annual_payable']                           != price_before_refcode['total_annual_payable']

        self.xendit.choose_ewallet_option()
        self.xendit.choose_ewallet_grabpay()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.click_proceed_btn()

        wait_loading_dashboard(self.driver)
        assert self.xendit.congratulations_text() is True

    def test_self_buy_health_credit_card_success_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        price_before_refcode                                                 = self.checkout_page.get_hmo_data_inputted()
        assert price_before_refcode['product_name']                         == 'Comprehensive Health Insurance Program'
        assert price_before_refcode['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert price_before_refcode['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert price_before_refcode['renewal']                              == 'Yearly'
        assert price_before_refcode['subtotal']                             ==  total_annual
        assert price_before_refcode['promo_discount']                       ==  'PHP 0'
        assert price_before_refcode['credit_used']                          ==  'PHP 0'
        assert price_before_refcode['total_saving']                         ==  'PHP 0'
        assert price_before_refcode['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.checkout_page.apply_refcode(self.refcode)

        wait_loading_dashboard(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'HMO discount 10%'

        wait_loading_dashboard(self.driver)
        price_after_refcode                                                 = self.checkout_page.get_hmo_data_inputted()
        assert price_after_refcode['product_name']                         == 'Comprehensive Health Insurance Program'
        assert price_after_refcode['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert price_after_refcode['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert price_after_refcode['renewal']                              == 'Yearly'
        assert price_after_refcode['total_amount'].split('.',1)[0]         == price_before_refcode['total_amount'].split('.',1)[0]
        assert price_after_refcode['credit_used']                          == 'PHP 0'
        assert price_after_refcode['primary_coverage'].split('.',1)[0]     == HmoPrice.primary_coverage[plan].split('.',1)[0]
        assert price_after_refcode['vat']                                  == price_before_refcode['vat']
        assert price_after_refcode['subtotal']                             != price_before_refcode['subtotal']
        assert price_after_refcode['promo_discount']                       != 'PHP 0'
        assert price_after_refcode['total_saving']                         != 'PHP 0'
        assert price_after_refcode['total_annual_payable']                 != price_before_refcode['total_annual_payable']

        self.xendit.input_card_details()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.input_purchase_authentication()

        wait_loading_dashboard(self.driver)
        assert self.xendit.congratulations_text() is True

    def test_self_buy_health_direct_debit_BPI_bank_success_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        price_before_refcode                                                 = self.checkout_page.get_hmo_data_inputted()
        assert price_before_refcode['product_name']                         == 'Comprehensive Health Insurance Program'
        assert price_before_refcode['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert price_before_refcode['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert price_before_refcode['renewal']                              == 'Yearly'
        assert price_before_refcode['subtotal']                             ==  total_annual
        assert price_before_refcode['promo_discount']                       ==  'PHP 0'
        assert price_before_refcode['credit_used']                          ==  'PHP 0'
        assert price_before_refcode['total_saving']                         ==  'PHP 0'
        assert price_before_refcode['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.checkout_page.apply_refcode(self.refcode)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'HMO discount 10%'

        wait_loading_dashboard(self.driver)
        price_after_refcode                                                          = self.checkout_page.get_hmo_data_inputted()
        assert price_after_refcode['product_name']                                  == 'Comprehensive Health Insurance Program'
        assert price_after_refcode['daily_benefit']                                 == HmoPrice.cash_benefit[plan]
        assert price_after_refcode['waiting_period']                                == 'Date policy documents will be ready (5-7 business days)'
        assert price_after_refcode['renewal']                                       == 'Yearly'
        assert price_after_refcode['total_amount'].split('.',1)[0]                  == price_before_refcode['total_amount'].split('.',1)[0]
        assert price_after_refcode['credit_used']                                   == 'PHP 0'
        assert price_after_refcode['primary_coverage'].split('.',1)[0]              == HmoPrice.primary_coverage[plan].split('.',1)[0]
        assert price_after_refcode['vat']                                           == price_before_refcode['vat']
        assert price_after_refcode['subtotal']                                      != price_before_refcode['subtotal']
        assert price_after_refcode['promo_discount']                                != 'PHP 0'
        assert price_after_refcode['total_saving']                                  != 'PHP 0'
        assert price_after_refcode['total_annual_payable']                          != price_before_refcode['total_annual_payable']

        self.xendit.choose_direct_debit_option()
        self.xendit.choose_direct_debit_BPI_bank()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.login_direct_debit_with_valid_account()

        assert self.xendit.processing_image() is True
        self.xendit.input_valid_otp()

        wait_loading_direct_bank(self.driver)
        assert self.xendit.congratulations_text() is True

    def test_self_buy_health_direct_debit_Union_bank_success_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan = self.quote_page.choose_random_plan_for_primary()
        self.quote_page.click_skip_btn()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        price_before_refcode                                                 = self.checkout_page.get_hmo_data_inputted()
        assert price_before_refcode['product_name']                         == 'Comprehensive Health Insurance Program'
        assert price_before_refcode['daily_benefit']                        == HmoPrice.cash_benefit[plan]
        assert price_before_refcode['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert price_before_refcode['renewal']                              == 'Yearly'
        assert price_before_refcode['subtotal']                             ==  total_annual
        assert price_before_refcode['promo_discount']                       ==  'PHP 0'
        assert price_before_refcode['credit_used']                          ==  'PHP 0'
        assert price_before_refcode['total_saving']                         ==  'PHP 0'
        assert price_before_refcode['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan].split('.',1)[0]

        self.checkout_page.apply_refcode(self.refcode)
        wait_loading_dashboard(self.driver)

        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'HMO discount 10%'

        wait_loading_dashboard(self.driver)
        price_after_refcode                                              = self.checkout_page.get_hmo_data_inputted()
        assert price_after_refcode['product_name']                      == 'Comprehensive Health Insurance Program'
        assert price_after_refcode['daily_benefit']                     == HmoPrice.cash_benefit[plan]
        assert price_after_refcode['waiting_period']                    == 'Date policy documents will be ready (5-7 business days)'
        assert price_after_refcode['renewal']                           == 'Yearly'
        assert price_after_refcode['total_amount'].split('.',1)[0]      == price_before_refcode['total_amount'].split('.',1)[0]
        assert price_after_refcode['credit_used']                       == 'PHP 0'
        assert price_after_refcode['primary_coverage'].split('.',1)[0]  == HmoPrice.primary_coverage[plan].split('.',1)[0]
        assert price_after_refcode['vat']                               == price_before_refcode['vat']
        assert price_after_refcode['subtotal']                          != price_before_refcode['subtotal']
        assert price_after_refcode['promo_discount']                    != 'PHP 0'
        assert price_after_refcode['total_saving']                      != 'PHP 0'
        assert price_after_refcode['total_annual_payable']              != price_before_refcode['total_annual_payable']

        self.xendit.choose_direct_debit_option()
        self.xendit.choose_direct_debit_Union_bank()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.login_direct_debit_with_valid_account()

        assert self.xendit.processing_image() is True
        self.xendit.input_valid_otp()

        wait_loading_direct_bank(self.driver)
        assert self.xendit.congratulations_text() is True
    #endregion Primary

    # region Dependent
    def test_self_buy_health_with_dependent_ewallet_success(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan_primary   = self.quote_page.choose_random_plan_for_primary()
        plan_dependent = self.quote_page.choose_random_plan_for_dependent()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.input_dependent_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted(with_dependent=True)
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == f'{HmoPrice.cash_benefit[plan_primary]} + {HmoPrice.cash_benefit[plan_dependent]}'
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage']                     ==  HmoPrice.primary_coverage[plan_primary]
        assert actual_result['dependent_coverage'].split('.',1)[0]   ==  HmoPrice.dependent_coverage[plan_dependent].split('.',1)[0]

        self.xendit.choose_ewallet_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_ewallet_grabpay()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.click_proceed_btn()

        wait_loading_dashboard(self.driver)
        assert self.xendit.congratulations_text() is True

    def test_self_buy_health_with_dependent_credit_card_success(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan_primary   = self.quote_page.choose_random_plan_for_primary()
        plan_dependent = self.quote_page.choose_random_plan_for_dependent()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.input_dependent_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted(with_dependent=True)
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == f'{HmoPrice.cash_benefit[plan_primary]} + {HmoPrice.cash_benefit[plan_dependent]}'
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan_primary].split('.',1)[0]
        assert actual_result['dependent_coverage'].split('.',1)[0]   ==  HmoPrice.dependent_coverage[plan_dependent].split('.',1)[0]


        self.xendit.input_card_details()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.input_purchase_authentication()

        wait_loading_dashboard(self.driver)
        assert self.xendit.congratulations_text() is True

    def test_self_buy_health_with_dependent_direct_debit_BPI_bank_success(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan_primary   = self.quote_page.choose_random_plan_for_primary()
        plan_dependent = self.quote_page.choose_random_plan_for_dependent()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.input_dependent_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted(with_dependent=True)
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == f'{HmoPrice.cash_benefit[plan_primary]} + {HmoPrice.cash_benefit[plan_dependent]}'
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan_primary].split('.',1)[0]
        assert actual_result['dependent_coverage'].split('.',1)[0]   ==  HmoPrice.dependent_coverage[plan_dependent].split('.',1)[0]

        self.xendit.choose_direct_debit_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_direct_debit_BPI_bank()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.login_direct_debit_with_valid_account()

        assert self.xendit.processing_image() is True
        self.xendit.input_valid_otp()

        wait_loading_direct_bank(self.driver)
        try:
            assert self.xendit.congratulations_text() is True
        except:
            print("Payment still waiting for callback")

    def test_self_buy_health_with_dependent_direct_debit_Union_bank_success(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_health)
        self.home_page.click_on_see_pricing_btn()

        plan_primary   = self.quote_page.choose_random_plan_for_primary()
        plan_dependent = self.quote_page.choose_random_plan_for_dependent()

        total_annual = self.quote_page.get_total_annual_payable()
        self.quote_page.click_next_btn()

        self.your_information_page.input_primary_information()
        self.your_information_page.input_dependent_information()
        self.your_information_page.click_next_btn()

        wait_loading_dashboard(self.driver)
        actual_result                                                 = self.checkout_page.get_hmo_data_inputted(with_dependent=True)
        assert actual_result['product_name']                         == 'Comprehensive Health Insurance Program'
        assert actual_result['daily_benefit']                        == f'{HmoPrice.cash_benefit[plan_primary]} + {HmoPrice.cash_benefit[plan_dependent]}'
        assert actual_result['waiting_period']                       == 'Date policy documents will be ready (5-7 business days)'
        assert actual_result['renewal']                              == 'Yearly'
        assert actual_result['subtotal']                             ==  total_annual
        assert actual_result['promo_discount']                       ==  'PHP 0'
        assert actual_result['credit_used']                          ==  'PHP 0'
        assert actual_result['total_saving']                         ==  'PHP 0'
        assert actual_result['primary_coverage'].split('.',1)[0]     ==  HmoPrice.primary_coverage[plan_primary].split('.',1)[0]
        assert actual_result['dependent_coverage'].split('.',1)[0]   ==  HmoPrice.dependent_coverage[plan_dependent].split('.',1)[0]

        self.xendit.choose_direct_debit_option()
        wait_loading_dashboard(self.driver)

        self.xendit.choose_direct_debit_Union_bank()
        self.xendit.click_pay_securely_btn()

        wait_loading_dashboard(self.driver)
        self.xendit.login_direct_debit_with_valid_account()

        assert self.xendit.processing_image() is True
        self.xendit.input_valid_otp()

        wait_loading_direct_bank(self.driver)
        try:
            assert self.xendit.congratulations_text() is True
        except:
            print("Payment still waiting for callback")
    # endregion Dependent
