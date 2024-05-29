from datetime import timedelta
from random import randint

from aqa.src.pages.venta.checkout_page import FlepCheckoutPage
from aqa.src.pages.venta.home_page import HomePage
from aqa.src.pages.venta.quote_page import FlepQuotePage
from aqa.src.pages.venta.stripe import StripeCheckout
from aqa.src.pages.venta.your_infomarion_page import FlepPersonalInfoPage
from aqa.src.tests.base import BaseTest
from aqa.utils.enums import url
from aqa.utils.generic import cal_year
from aqa.utils.helper import sgt_today
from aqa.utils.webdriver_util import scroll_to_bottom, wait_for_loading_venta


def cal_pricing_outdoor(occupation, transport_vehicle, transport_mode=None): # https://gigacover.atlassian.net/browse/GC-5271
    if occupation == 'Food / Logistic Delivery':
        if transport_mode == 'Motorcycle':
            total_amount = '59.07'
        else:
            if transport_vehicle == 'Motorcycle':
                total_amount = '49.23'
            else:
                total_amount = '34.00'
    else:
        if transport_vehicle == 'Motorcycle':
            total_amount = '49.23'
        else:
            total_amount = '34.00'
    return total_amount


class Test(BaseTest):

    def setUp_fixture(self):
        self.home_page          = HomePage(self.driver)
        self.quote_page         = FlepQuotePage(self.driver)
        self.personal_info_page = FlepPersonalInfoPage(self.driver)
        self.checkout_page      = FlepCheckoutPage(self.driver)
        self.stripe             = StripeCheckout(self.driver)
        self.refcode            = 'COUPON_FLEP'


    def test_flep_gojek(self):
        """This is a self-buy as gojek driver test"""
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_flep)

        self.quote_page.choose_gojek()

        wait_for_loading_venta(self.driver)
        age = randint(18, 65)
        year = cal_year(age)
        self.quote_page.input_dob(year)

        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_start_date()
        self.quote_page.click_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.input_personal_info()
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_data_inputted()
        assert actual_result['product_name']                  == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']                 == '$80 SGD / day'
        assert actual_result['waiting_period']                == '5 Days'
        assert actual_result['ip_benefits']                   == '2nd - 84th day of hospitalisation'
        assert actual_result['op_benefits']                   == '6th - 21st day of medical leave'
        assert actual_result['renewal']                       == 'Monthly'
        assert actual_result['policy_start']                  == (sgt_today() + timedelta(days=5)).strftime("%d %b %Y") # today + 5
        assert actual_result['promo_discount']                == '$0.00'
        assert actual_result['credit_used']                   == '$0.00'
        assert actual_result['total_amount']                  == '$25.00'
        assert actual_result['total_saving']                  == '$0.00'
        assert actual_result['gst']                           == '$2.00'
        assert actual_result['final_amount']                  == '$27.00'

        self.stripe.click_next_btn()
        self.stripe.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True


    def test_flep_gojek_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_flep)

        self.quote_page.choose_gojek()

        wait_for_loading_venta(self.driver)
        age = randint(17, 70)
        year = cal_year(age)
        self.quote_page.input_dob(year)

        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_start_date()
        self.quote_page.click_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.input_personal_info()
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        self.checkout_page.apply_refcode(self.refcode)

        wait_for_loading_venta(self.driver)

        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'Flep Discount 10$'

        actual_result = self.checkout_page.get_data_inputted()
        assert actual_result['product_name']                  == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']                 == '$80 SGD / day'
        assert actual_result['waiting_period']                == '5 Days'
        assert actual_result['ip_benefits']                   == '2nd - 84th day of hospitalisation'
        assert actual_result['op_benefits']                   == '6th - 21st day of medical leave'
        assert actual_result['renewal']                       == 'Monthly'
        assert actual_result['policy_start']                  == (sgt_today() + timedelta(days=5)).strftime("%d %b %Y") # today + 5
        assert actual_result['promo_discount']                == '- $10.00'
        assert actual_result['credit_used']                   == '$0.00'
        assert actual_result['total_amount']                  == '$25.00'
        assert actual_result['total_saving']                  == '$10.00'
        assert actual_result['gst']                           == '$1.20'
        assert actual_result['final_amount']                  == '$16.20'

        self.stripe.click_next_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD $16.20'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True


    def test_flep_indoor(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_flep)

        self.quote_page.choose_not_gojek()
        self.quote_page.choose_indoor_environment()
        self.quote_page.choose_motorcycle_transport()

        self.quote_page.input_dob('1980')

        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_start_date()
        self.quote_page.click_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.input_personal_info()
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        total_amount_include_gst = '49.23'

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_data_inputted()
        assert actual_result['product_name']                  == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']                 == '$80 SGD / day'
        assert actual_result['waiting_period']                == '5 Days'
        assert actual_result['ip_benefits']                   == '2nd - 84th day of hospitalisation'
        assert actual_result['op_benefits']                   == '6th - 21st day of medical leave'
        assert actual_result['renewal']                       == 'Monthly'
        assert actual_result['policy_start']                  == (sgt_today() + timedelta(days=5)).strftime("%d %b %Y") # today + 5
        assert actual_result['promo_discount']                == '$0.00'
        assert actual_result['credit_used']                   == '$0.00'
        assert actual_result['total_saving']                  == '$0.00'
        assert actual_result['final_amount']                  == f'${total_amount_include_gst}'

        self.stripe.click_next_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD ${total_amount_include_gst}'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True


    def test_flep_indoor_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_flep)

        self.quote_page.choose_not_gojek()
        self.quote_page.choose_indoor_environment()
        self.quote_page.choose_motorcycle_transport()

        self.quote_page.input_dob('1980')

        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_start_date()
        self.quote_page.click_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.input_personal_info()
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        self.checkout_page.apply_refcode(self.refcode)

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'Flep Discount 10$'

        actual_result = self.checkout_page.get_data_inputted()
        assert actual_result['product_name']                  == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']                 == '$80 SGD / day'
        assert actual_result['waiting_period']                == '5 Days'
        assert actual_result['ip_benefits']                   == '2nd - 84th day of hospitalisation'
        assert actual_result['op_benefits']                   == '6th - 21st day of medical leave'
        assert actual_result['renewal']                       == 'Monthly'
        assert actual_result['policy_start']                  == (sgt_today() + timedelta(days=5)).strftime("%d %b %Y") # today + 5
        assert actual_result['promo_discount']                == '- $10.00'
        assert actual_result['credit_used']                   == '$0.00'
        assert actual_result['total_saving']                  == '$10.00'
        assert actual_result['final_amount']                  == f'$38.43'

        self.stripe.click_next_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD $38.43'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True


    def test_flep_outdoor(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_flep)

        self.quote_page.choose_not_gojek()
        self.quote_page.choose_outdoor_environment()

        wait_for_loading_venta(self.driver)
        data = self.quote_page.choose_random_occupation()
        occupation     = data['occupation']
        transport_mode = data['transport_mode']

        wait_for_loading_venta(self.driver)
        transport_vehicle = self.quote_page.choose_random_public_transport()

        self.quote_page.input_dob('1980')

        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_start_date()
        self.quote_page.click_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.input_personal_info()
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        total_amount_include_gst = cal_pricing_outdoor(occupation, transport_vehicle, transport_mode)

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_data_inputted()
        assert actual_result['product_name']                  == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']                 == '$80 SGD / day'
        assert actual_result['waiting_period']                == '5 Days'
        assert actual_result['ip_benefits']                   == '2nd - 84th day of hospitalisation'
        assert actual_result['op_benefits']                   == '6th - 21st day of medical leave'
        assert actual_result['renewal']                       == 'Monthly'
        assert actual_result['policy_start']                  == (sgt_today() + timedelta(days=5)).strftime("%d %b %Y") # today + 5
        assert actual_result['promo_discount']                == '$0.00'
        assert actual_result['credit_used']                   == '$0.00'
        assert actual_result['total_saving']                  == '$0.00'
        assert actual_result['final_amount']                  == f'${total_amount_include_gst}'

        self.stripe.click_next_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD ${total_amount_include_gst}'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True


    def test_flep_outdoor_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_flep)

        self.quote_page.choose_not_gojek()
        self.quote_page.choose_outdoor_environment()

        wait_for_loading_venta(self.driver)
        data = self.quote_page.choose_random_occupation()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_random_public_transport()

        self.quote_page.input_dob('1980')

        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_start_date()
        self.quote_page.click_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.input_personal_info()
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        self.checkout_page.apply_refcode(self.refcode)

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'Flep Discount 10$'

        actual_result = self.checkout_page.get_data_inputted()
        assert actual_result['product_name']                  == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']                 == '$80 SGD / day'
        assert actual_result['waiting_period']                == '5 Days'
        assert actual_result['ip_benefits']                   == '2nd - 84th day of hospitalisation'
        assert actual_result['op_benefits']                   == '6th - 21st day of medical leave'
        assert actual_result['renewal']                       == 'Monthly'
        assert actual_result['policy_start']                  == (sgt_today() + timedelta(days=5)).strftime("%d %b %Y") # today + 5
        assert actual_result['promo_discount']                == '- $10.00'
        assert actual_result['credit_used']                   == '$0.00'
        assert actual_result['total_saving']                  == '$10.00'
        # assert actual_result['final_amount']                  == f'${total_amount_include_gst_after_refcode}'

        self.stripe.click_next_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f"Pay SGD {actual_result['final_amount']}"

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True


    #TODO find a way write testcase self-buy with user_balance
