from datetime import timedelta

from aqa.src.pages.venta.home_page import HomePage
from aqa.src.pages.venta.checkout_page import PmlCheckoutPage
from aqa.src.pages.venta.your_infomarion_page import PmlYourInformationPage
from aqa.src.pages.venta.stripe import StripeCheckout
from aqa.src.tests.base import BaseTest
from aqa.utils.enums import url
from aqa.utils.helper import sgt_today
from aqa.utils.webdriver_util import scroll_to_bottom, wait_for_loading_venta


class Test(BaseTest):

    def setUp_fixture(self):
        self.home_page             = HomePage(self.driver)
        self.your_information_page = PmlYourInformationPage(self.driver)
        self.checkout_page         = PmlCheckoutPage(self.driver)
        self.stripe                = StripeCheckout(self.driver)
        self.refcode               = 'COUPON_PML'

    def test_self_buy_pml(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_pml)

        self.home_page.click_on_buy_pml_btn()

        self.your_information_page.input_information()
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)
        self.your_information_page.click_checkout_btn()

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_data_inputted()
        assert actual_result['product_name']         == 'ComfortDelGro Taxi Prolonged Medical Leave Insurance - Individual Scheme'
        assert actual_result['cash_benefits']        == '$80 daily income benefit'
        assert actual_result['waiting_period']       == '30 Days'
        assert actual_result['ip_benefits']          == '8th day onwards, for up to 60 days'
        assert actual_result['op_benefits']          == '8th day onwards, for up to 14 days'
        assert actual_result['renewal']              == 'Yearly'
        assert actual_result['policy_start']         ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['total_amount']         ==  '$125'
        assert actual_result['discount']             ==  '-'
        assert actual_result['gst']                  ==  '$10'
        assert actual_result['total_annual_payable'] ==  '$135.00'

        self.stripe.click_pay_securely_btn()
        self.stripe.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_pml_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_pml)

        self.home_page.click_on_buy_pml_btn()

        self.your_information_page.input_information()
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)
        self.your_information_page.click_checkout_btn()

        wait_for_loading_venta(self.driver)
        self.checkout_page.apply_refcode(self.refcode)
        assert self.checkout_page.get_refcode_msg(self.refcode) == 'PML Discount 10$'

        actual_result = self.checkout_page.get_data_inputted()
        assert actual_result['product_name']         == 'ComfortDelGro Taxi Prolonged Medical Leave Insurance - Individual Scheme'
        assert actual_result['cash_benefits']        == '$80 daily income benefit'
        assert actual_result['waiting_period']       == '30 Days'
        assert actual_result['ip_benefits']          == '8th day onwards, for up to 60 days'
        assert actual_result['op_benefits']          == '8th day onwards, for up to 14 days'
        assert actual_result['renewal']              == 'Yearly'
        assert actual_result['policy_start']         ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['total_amount']         ==  '$125'
        assert actual_result['discount']             ==  '-$10'
        assert actual_result['gst']                  ==  '$9.2'
        assert actual_result['total_annual_payable'] ==  '$124.20'

        self.stripe.click_pay_securely_btn()
        self.stripe.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.congratulations_text() is True
