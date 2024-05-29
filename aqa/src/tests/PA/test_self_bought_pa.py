from random import choice
from datetime import timedelta

from aqa.src.pages.venta.checkout_page import PaCheckoutPage
from aqa.src.pages.venta.home_page import HomePage
from aqa.src.pages.venta.opn import OpnCheckout
from aqa.src.pages.venta.quote_page import PaQuotePage
from aqa.src.pages.venta.your_infomarion_page import PaPersonalInfoPage
from aqa.src.tests.base import BaseTest
from aqa.utils.enums import url
from aqa.utils.helper import sgt_today
from aqa.utils.webdriver_util import scroll_to_bottom, wait_for_loading_venta


def cal_price_for_pa(coverage):
    total_amount = ''; medical_expense_reimbursement = ''; gst = ''
    if coverage == '$20,000':  total_amount = '1.45'; medical_expense_reimbursement = '$400 per accident';   gst = '0.12'
    if coverage == '$50,000':  total_amount = '3.49'; medical_expense_reimbursement = '$1,000 per accident'; gst = '0.29'
    if coverage == '$100,000': total_amount = '6.32'; medical_expense_reimbursement = '$2,000 per accident'; gst = '0.52'
    return total_amount, medical_expense_reimbursement, gst


class Test(BaseTest):

    def setUp_fixture(self):
        self.home_page          = HomePage(self.driver)
        self.quote_page         = PaQuotePage(self.driver)
        self.personal_info_page = PaPersonalInfoPage(self.driver)
        self.checkout_page      = PaCheckoutPage(self.driver)
        self.opn                = OpnCheckout(self.driver)
        self.refcode            = 'COUPON_PA'


    def test_self_00_bought_PA(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_pa)
        wait_for_loading_venta(self.driver)

        coverage_level_list = ['$20,000', '$50,000', '$100,000']
        coverage = choice(coverage_level_list)

        self.quote_page.choose_coverage_level(coverage)
        self.quote_page.click_next_btn()

        self.quote_page.click_all_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.input_personal_info()
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        total_amount = cal_price_for_pa(coverage)[0]
        medical_expense_reimbursement = cal_price_for_pa(coverage)[1]
        gst = cal_price_for_pa(coverage)[2]

        actual_result = self.checkout_page.get_data_inputted()
        assert actual_result['product_name']                        == 'Personal Accident'
        assert actual_result['sum_insured']                         == coverage
        assert actual_result['activation_period']                   == '1 Day'
        assert actual_result['medical_expense_reimbursement']       == medical_expense_reimbursement
        assert actual_result['renewal']                             == 'Monthly'
        assert actual_result['policy_start']                        == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']                      == '$0.00'
        assert actual_result['credit_used']                         == '$0.00'
        assert actual_result['total_saving']                        == '$0.00'
        assert actual_result['gst']                                 == f'${gst}'
        assert actual_result['final_amount_due']                    == f'${total_amount}'

        self.opn.click_next_btn()
        charge_amount_stripe = self.opn.checkout()
        assert charge_amount_stripe == f'Pay {total_amount} SGD'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

    def test_self_01_bought_PA_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_pa)
        wait_for_loading_venta(self.driver)

        coverage_level_list = ['$50,000', '$100,000']
        coverage = choice(coverage_level_list)
        self.quote_page.choose_coverage_level(coverage)
        self.quote_page.click_next_btn()

        self.quote_page.click_all_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.input_personal_info()
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.checkout_page.apply_refcode(self.refcode)

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'PA Discount $2'

        medical_expense_reimbursement = cal_price_for_pa(coverage)[1]

        actual_result = self.checkout_page.get_data_inputted()
        assert actual_result['product_name']                        == 'Personal Accident'
        assert actual_result['sum_insured']                         == coverage
        assert actual_result['activation_period']                   == '1 Day'
        assert actual_result['medical_expense_reimbursement']       == medical_expense_reimbursement
        assert actual_result['renewal']                             == 'Monthly'
        assert actual_result['policy_start']                        == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']                      == '- $2.00'
        assert actual_result['credit_used']                         == '$0.00'
        assert actual_result['total_saving']                        == '$2.00'

        self.opn.click_next_btn()
        charge_amount_stripe = self.opn.checkout()
        assert charge_amount_stripe == f"Pay {actual_result['final_amount_due'].replace('$', '')} SGD"

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

    #TODO find a way write testcase self-buy with user_balance
