from datetime import timedelta

import pytest

from aqa.src.pages.venta.home_page import ZeekHomePage
from aqa.src.pages.venta.checkout_page import ZeekCheckoutPage
from aqa.src.pages.venta.quote_page import ZeekQuotePage
from aqa.src.pages.venta.your_infomarion_page import ZeekYourInformationPage
from aqa.src.pages.venta.stripe import StripeCheckout
from aqa.src.tests.base import BaseTest
from aqa.utils.helper import sgt_today
from aqa.utils.webdriver_util import wait, scroll_to_bottom, wait_for_loading_venta, wait_for_loading_landing_page


class Test(BaseTest):

    def setUp_fixture(self):
        self.home_page             = ZeekHomePage(self.driver)
        self.quote_page            = ZeekQuotePage(self.driver)
        self.your_information_page = ZeekYourInformationPage(self.driver)
        self.checkout_page         = ZeekCheckoutPage(self.driver)
        self.stripe                = StripeCheckout(self.driver)

    #FLEP
    def test_self_buy_zeek_flep_driver(self):
        self.setUp_fixture()

        self.home_page.open_url()

        self.home_page.click_on_buy_flep_btn()
        self.home_page.click_buy_flep_now_btn()

        self.quote_page.choose_driver_occupation()
        plan = self.quote_page.choose_flep_driver_plan()

        self.your_information_page.input_information()
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        wait_for_loading_venta(self.driver)
        premium = ''; total_amount = ''; gst = ''
        if plan == 'S$80 daily cash benefit' : premium = '27.88'; total_amount = 'S$26.06'; gst = 'S$1.82'
        if plan == 'S$100 daily cash benefit': premium = '32.53'; total_amount = 'S$30.40'; gst = 'S$2.13'

        actual_result = self.checkout_page.get_flep_data_inputted()
        assert actual_result['product_name']         == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']        == plan
        assert actual_result['waiting_period']       == '5 Days'
        assert actual_result['ip_benefits'].strip()  == '2nd - 60th day of hospitalisation'
        assert actual_result['op_benefits'].strip()  == '6th - 14th day of medical leave'
        assert actual_result['renewal']              == 'Monthly'
        assert actual_result['policy_start']         ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']             ==  f'S${premium}'
        assert actual_result['promo_discount']       ==  'S$0.00'
        assert actual_result['credit_used']          ==  'S$0.00'
        assert actual_result['total_amount']         ==  total_amount
        assert actual_result['total_saving']         ==  'S$0.00'
        assert actual_result['gst']                  ==  gst
        assert actual_result['final_amount']         ==  f'S${premium}'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD ${premium}'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_zeek_flep_driver_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url()

        self.home_page.click_on_buy_flep_btn()
        self.home_page.click_buy_flep_now_btn()

        self.quote_page.choose_driver_occupation()
        plan = self.quote_page.choose_flep_driver_plan()

        self.your_information_page.input_information()
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        self.checkout_page.apply_refcode('50FLEP')

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg()
        assert refcode_msg == 'Flep Discount 10$'

        premium = ''; total_amount = ''; gst = ''
        if plan == 'S$80 daily cash benefit' : premium = '27.88'; total_amount = 'S$26.06'; gst = 'S$1.82'
        if plan == 'S$100 daily cash benefit': premium = '32.53'; total_amount = 'S$30.40'; gst = 'S$2.13'
        total_amount_include_gst_after_refcode = "{:.2f}".format(float(premium) - 10) #recode

        actual_result = self.checkout_page.get_flep_data_inputted()
        assert actual_result['product_name']         == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']        == plan
        assert actual_result['waiting_period']       == '5 Days'
        assert actual_result['ip_benefits'].strip()  == '2nd - 60th day of hospitalisation'
        assert actual_result['op_benefits'].strip()  == '6th - 14th day of medical leave'
        assert actual_result['renewal']              == 'Monthly'
        assert actual_result['policy_start']         ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']             ==  f'S${premium}'
        assert actual_result['promo_discount']       ==  '- S$10.00'
        assert actual_result['credit_used']          ==  'S$0.00'
        assert actual_result['total_amount']         ==  total_amount
        assert actual_result['total_saving']         ==  'S$10.00'
        assert actual_result['gst']                  ==  gst
        assert actual_result['final_amount']         ==  f'S${total_amount_include_gst_after_refcode}'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD ${total_amount_include_gst_after_refcode}'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_zeek_flep_driver_with_refcode_balance(self):
        self.setUp_fixture()

        nric = setup_user_balance()

        self.home_page.open_url()

        self.home_page.click_on_buy_flep_btn()
        self.home_page.click_buy_flep_now_btn()

        self.quote_page.choose_driver_occupation()
        plan = self.quote_page.choose_flep_driver_plan()

        self.your_information_page.input_information(nric)
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        self.checkout_page.apply_refcode('50FLEP')

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg()
        assert refcode_msg == 'Flep Discount 10$'

        premium = ''; total_amount = ''; gst = ''
        if plan == 'S$80 daily cash benefit' : premium = '27.88'; total_amount = 'S$26.06'; gst = 'S$1.82'
        if plan == 'S$100 daily cash benefit': premium = '32.53'; total_amount = 'S$30.40'; gst = 'S$2.13'
        total_amount_include_gst_after_refcode_balance = "{:.2f}".format(float(premium) - 10 - 10) #recode 10 and balance 10

        actual_result = self.checkout_page.get_flep_data_inputted()
        assert actual_result['product_name']         == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']        == plan
        assert actual_result['waiting_period']       == '5 Days'
        assert actual_result['ip_benefits'].strip()  == '2nd - 60th day of hospitalisation'
        assert actual_result['op_benefits'].strip()  == '6th - 14th day of medical leave'
        assert actual_result['renewal']              == 'Monthly'
        assert actual_result['policy_start']         ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']             ==  f'S${premium}'
        assert actual_result['promo_discount']       ==  '- S$10.00'
        assert actual_result['credit_used']          ==  '- S$10.00'
        assert actual_result['total_amount']         ==  total_amount
        assert actual_result['total_saving']         ==  'S$20.00'
        assert actual_result['gst']                  ==  gst
        assert actual_result['final_amount']         ==  f'S${total_amount_include_gst_after_refcode_balance}'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD ${total_amount_include_gst_after_refcode_balance}'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_zeek_flep_moto(self):
        self.setUp_fixture()

        self.home_page.open_url()

        self.home_page.click_on_buy_flep_btn()
        self.home_page.click_buy_flep_now_btn()

        self.quote_page.choose_moto_occupation()
        plan = self.quote_page.choose_flep_moto_plan()

        self.your_information_page.input_information()
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        wait_for_loading_venta(self.driver)
        premium = ''; total_amount = ''; gst = ''
        if plan == 'S$40 daily cash benefit' : premium = '23.54'; total_amount = 'S$22.00'; gst = 'S$1.54'
        if plan == 'S$50 daily cash benefit' : premium = '29.05'; total_amount = 'S$27.15'; gst = 'S$1.90'

        actual_result = self.checkout_page.get_flep_data_inputted()
        assert actual_result['product_name']         == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']        == plan
        assert actual_result['waiting_period']       == '5 Days'
        assert actual_result['ip_benefits'].strip()  == '2nd - 60th day of hospitalisation'
        assert actual_result['op_benefits'].strip()  == '6th - 14th day of medical leave'
        assert actual_result['renewal']              == 'Monthly'
        assert actual_result['policy_start']         ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']             ==  f'S${premium}'
        assert actual_result['promo_discount']       ==  'S$0.00'
        assert actual_result['credit_used']          ==  'S$0.00'
        assert actual_result['total_amount']         ==  total_amount
        assert actual_result['total_saving']         ==  'S$0.00'
        assert actual_result['gst']                  ==  gst
        assert actual_result['final_amount']         ==  f'S${premium}'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD ${premium}'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_zeek_flep_moto_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url()

        self.home_page.click_on_buy_flep_btn()
        self.home_page.click_buy_flep_now_btn()

        self.quote_page.choose_moto_occupation()
        plan = self.quote_page.choose_flep_moto_plan()

        self.your_information_page.input_information()
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        self.checkout_page.apply_refcode('50FLEP')

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg()
        assert refcode_msg == 'Flep Discount 10$'

        wait_for_loading_venta(self.driver)
        premium = ''; total_amount = ''; gst = ''
        if plan == 'S$40 daily cash benefit' : premium = '23.54'; total_amount = 'S$22.00'; gst = 'S$1.54'
        if plan == 'S$50 daily cash benefit' : premium = '29.05'; total_amount = 'S$27.15'; gst = 'S$1.90'
        total_amount_include_gst_after_refcode = "{:.2f}".format(float(premium) - 10) #recode

        actual_result = self.checkout_page.get_flep_data_inputted()
        assert actual_result['product_name']         == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']        == plan
        assert actual_result['waiting_period']       == '5 Days'
        assert actual_result['ip_benefits'].strip()  == '2nd - 60th day of hospitalisation'
        assert actual_result['op_benefits'].strip()  == '6th - 14th day of medical leave'
        assert actual_result['renewal']              == 'Monthly'
        assert actual_result['policy_start']         ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']             ==  f'S${premium}'
        assert actual_result['promo_discount']       ==  '- S$10.00'
        assert actual_result['credit_used']          ==  'S$0.00'
        assert actual_result['total_amount']         ==  total_amount
        assert actual_result['total_saving']         ==  'S$10.00'
        assert actual_result['gst']                  ==  gst
        assert actual_result['final_amount']         ==  f'S${total_amount_include_gst_after_refcode}'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD ${total_amount_include_gst_after_refcode}'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_zeek_flep_moto_with_refcode_balance(self):
        self.setUp_fixture()

        nric = setup_user_balance()

        self.home_page.open_url()

        self.home_page.click_on_buy_flep_btn()
        self.home_page.click_buy_flep_now_btn()

        self.quote_page.choose_moto_occupation()
        plan = self.quote_page.choose_flep_moto_plan()

        self.your_information_page.input_information(nric)
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        self.checkout_page.apply_refcode('50FLEP')

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg()
        assert refcode_msg == 'Flep Discount 10$'

        wait_for_loading_venta(self.driver)
        premium = ''; total_amount = ''; gst = ''
        if plan == 'S$40 daily cash benefit' : premium = '23.54'; total_amount = 'S$22.00'; gst = 'S$1.54'
        if plan == 'S$50 daily cash benefit' : premium = '29.05'; total_amount = 'S$27.15'; gst = 'S$1.90'
        total_amount_include_gst_after_refcode_balance = "{:.2f}".format(float(premium) - 10 - 10) #recode 10 and balance 10

        actual_result = self.checkout_page.get_flep_data_inputted()
        assert actual_result['product_name']         == 'Freelance Earning Protection (FLEP)'
        assert actual_result['daily_benefit']        == plan
        assert actual_result['waiting_period']       == '5 Days'
        assert actual_result['ip_benefits'].strip()  == '2nd - 60th day of hospitalisation'
        assert actual_result['op_benefits'].strip()  == '6th - 14th day of medical leave'
        assert actual_result['renewal']              == 'Monthly'
        assert actual_result['policy_start']         ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']             ==  f'S${premium}'
        assert actual_result['promo_discount']       ==  '- S$10.00'
        assert actual_result['credit_used']          ==  '- S$10.00'
        assert actual_result['total_amount']         ==  total_amount
        assert actual_result['total_saving']         ==  'S$20.00'
        assert actual_result['gst']                  ==  gst
        assert actual_result['final_amount']         ==  f'S${total_amount_include_gst_after_refcode_balance}'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD ${total_amount_include_gst_after_refcode_balance}'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    #PA
    def test_self_buy_zeek_pa_driver(self):
        self.setUp_fixture()

        self.home_page.open_url()

        self.home_page.click_on_buy_pa_btn()
        self.home_page.click_buy_pa_now_btn()

        self.quote_page.choose_driver_occupation()
        self.quote_page.choose_pa_driver_plan()

        self.your_information_page.input_information()
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_pa_data_inputted()
        assert actual_result['product_name']                   == 'Personal Accident'
        assert actual_result['sum_insured']                    == 'S$10,000'
        assert actual_result['activation_period']              == '1 Day'
        assert actual_result['medical_expense_reimbursement']  == 'S$200 per accident'
        assert actual_result['renewal']                        == 'Monthly'
        assert actual_result['policy_start']                   ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']                       ==  'S$2.01'
        assert actual_result['promo_discount']                 ==  'S$0.00'
        assert actual_result['credit_used']                    ==  'S$0.00'
        assert actual_result['total_amount']                   ==  'S$1.88'
        assert actual_result['total_saving']                   ==  'S$0.00'
        assert actual_result['gst']                            ==  'S$0.13'
        assert actual_result['final_amount']                   ==  'S$2.01'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD $2.01'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_zeek_pa_driver_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url()

        self.home_page.click_on_buy_pa_btn()
        self.home_page.click_buy_pa_now_btn()

        self.quote_page.choose_driver_occupation()
        self.quote_page.choose_pa_driver_plan()

        self.your_information_page.input_information()
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        self.checkout_page.apply_refcode('50PA')

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg()
        assert refcode_msg == 'PA Discount $1'

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_pa_data_inputted()
        assert actual_result['product_name']                   == 'Personal Accident'
        assert actual_result['sum_insured']                    == 'S$10,000'
        assert actual_result['activation_period']              == '1 Day'
        assert actual_result['medical_expense_reimbursement']  == 'S$200 per accident'
        assert actual_result['renewal']                        == 'Monthly'
        assert actual_result['policy_start']                   ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']                       ==  'S$2.01'
        assert actual_result['promo_discount']                 ==  '- S$1.00'
        assert actual_result['credit_used']                    ==  'S$0.00'
        assert actual_result['total_amount']                   ==  'S$1.88'
        assert actual_result['total_saving']                   ==  'S$1.00'
        assert actual_result['gst']                            ==  'S$0.13'
        assert actual_result['final_amount']                   ==  'S$1.01'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD $1.01'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_zeek_pa_driver_with_refcode_balance(self):
        self.setUp_fixture()

        nric = setup_user_balance()

        self.home_page.open_url()

        self.home_page.click_on_buy_pa_btn()
        self.home_page.click_buy_pa_now_btn()

        self.quote_page.choose_driver_occupation()
        self.quote_page.choose_pa_driver_plan()

        self.your_information_page.input_information(nric)
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        self.checkout_page.apply_refcode('50PA')

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg()
        assert refcode_msg == 'PA Discount $1'

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_pa_data_inputted()
        assert actual_result['product_name']                   == 'Personal Accident'
        assert actual_result['sum_insured']                    == 'S$10,000'
        assert actual_result['activation_period']              == '1 Day'
        assert actual_result['medical_expense_reimbursement']  == 'S$200 per accident'
        assert actual_result['renewal']                        == 'Monthly'
        assert actual_result['policy_start']                   ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']                       ==  'S$2.01'
        assert actual_result['promo_discount']                 ==  '- S$1.00'
        assert actual_result['credit_used']                    ==  '- S$1.01'
        assert actual_result['total_amount']                   ==  'S$1.88'
        assert actual_result['total_saving']                   ==  'S$2.01'
        assert actual_result['gst']                            ==  'S$0.13'
        assert actual_result['final_amount']                   ==  'S$0.00'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD 0.00'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_zeek_pa_moto(self):
        self.setUp_fixture()

        self.home_page.open_url()

        self.home_page.click_on_buy_pa_btn()
        self.home_page.click_buy_pa_now_btn()

        self.quote_page.choose_moto_occupation()
        self.quote_page.choose_pa_moto_plan()

        self.your_information_page.input_information()
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_pa_data_inputted()
        assert actual_result['product_name']                   == 'Personal Accident'
        assert actual_result['sum_insured']                    == 'S$5,000'
        assert actual_result['activation_period']              == '1 Day'
        assert actual_result['medical_expense_reimbursement']  == 'S$100 per accident'
        assert actual_result['renewal']                        == 'Monthly'
        assert actual_result['policy_start']                   ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']                       ==  'S$3.78'
        assert actual_result['promo_discount']                 ==  'S$0.00'
        assert actual_result['credit_used']                    ==  'S$0.00'
        assert actual_result['total_amount']                   ==  'S$3.53'
        assert actual_result['total_saving']                   ==  'S$0.00'
        assert actual_result['gst']                            ==  'S$0.25'
        assert actual_result['final_amount']                   ==  'S$3.78'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD $3.78'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_zeek_pa_moto_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url()

        self.home_page.click_on_buy_pa_btn()
        self.home_page.click_buy_pa_now_btn()

        self.quote_page.choose_moto_occupation()
        plan = self.quote_page.choose_pa_moto_plan()

        self.your_information_page.input_information()
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        self.checkout_page.apply_refcode('50PA')

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg()
        assert refcode_msg == 'PA Discount $1'

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_pa_data_inputted()
        assert actual_result['product_name']                   == 'Personal Accident'
        assert actual_result['sum_insured']                    == 'S$5,000'
        assert actual_result['activation_period']              == '1 Day'
        assert actual_result['medical_expense_reimbursement']  == 'S$100 per accident'
        assert actual_result['renewal']                        == 'Monthly'
        assert actual_result['policy_start']                   ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']                       ==  'S$3.78'
        assert actual_result['promo_discount']                 ==  '- S$1.00'
        assert actual_result['credit_used']                    ==  'S$0.00'
        assert actual_result['total_amount']                   ==  'S$3.53'
        assert actual_result['total_saving']                   ==  'S$1.00'
        assert actual_result['gst']                            ==  'S$0.25'
        assert actual_result['final_amount']                   ==  'S$2.78'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD $2.78'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True

    def test_self_buy_zeek_pa_moto_with_refcode_balance(self):
        self.setUp_fixture()

        nric = setup_user_balance()

        self.home_page.open_url()

        self.home_page.click_on_buy_pa_btn()
        self.home_page.click_buy_pa_now_btn()

        self.quote_page.choose_moto_occupation()
        self.quote_page.choose_pa_moto_plan()

        self.your_information_page.input_information(nric)
        self.your_information_page.click_policy_checkbox()

        scroll_to_bottom(self.driver)

        self.your_information_page.click_checkout_now_btn()

        self.checkout_page.apply_refcode('50PA')

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg()
        assert refcode_msg == 'PA Discount $1'

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_pa_data_inputted()
        assert actual_result['product_name']                   == 'Personal Accident'
        assert actual_result['sum_insured']                    == 'S$5,000'
        assert actual_result['activation_period']              == '1 Day'
        assert actual_result['medical_expense_reimbursement']  == 'S$100 per accident'
        assert actual_result['renewal']                        == 'Monthly'
        assert actual_result['policy_start']                   ==  (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['subtotal']                       ==  'S$3.78'
        assert actual_result['promo_discount']                 ==  '- S$1.00'
        assert actual_result['credit_used']                    ==  '- S$2.78'
        assert actual_result['total_amount']                   ==  'S$3.53'
        assert actual_result['total_saving']                   ==  'S$3.78'
        assert actual_result['gst']                            ==  'S$0.25'
        assert actual_result['final_amount']                   ==  'S$0.00'

        self.stripe.click_pay_securely_btn()
        charge_amount_stripe = self.stripe.checkout()
        assert charge_amount_stripe == f'Pay SGD 0.00'

        wait_for_loading_landing_page(self.driver)
        assert self.checkout_page.congratulations_text() is True
