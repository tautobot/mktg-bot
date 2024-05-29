from datetime import timedelta

from aqa.src.pages.venta.checkout_page import CdwCheckoutPage
from aqa.src.pages.venta.home_page import HomePage
from aqa.src.pages.venta.opn import OpnCheckout
from aqa.src.pages.venta.quote_page import CdwQuotePage
from aqa.src.pages.venta.your_infomarion_page import CdwPersonalInfoPage
from aqa.src.tests.base import BaseTest
from aqa.utils.enums import url
from aqa.utils.generic import generate_nricfin, write_to_file
from aqa.utils.helper import sgt_today, create_fixture_for_cdw
from aqa.utils.webdriver_util import scroll_to_bottom, wait_for_loading_venta
from config_local import WORKING_DIR_FIXTURE


class Test(BaseTest):

    def setUp_fixture(self):
        self.home_page          = HomePage(self.driver)
        self.quote_page         = CdwQuotePage(self.driver)
        self.personal_info_page = CdwPersonalInfoPage(self.driver)
        self.checkout_page      = CdwCheckoutPage(self.driver)
        self.opn                = OpnCheckout(self.driver)
        self.refcode            = 'COUPON_CDW'

    #region CDW
    def test_buy_cdw_option_A(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.not_choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        section = self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        premium = self.quote_page.get_premium()
        premium = "{:.2f}".format(float((premium.split("$")[1]).split()[0])) #format premium to 2 digit

        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_data_inputted()
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']               == f'Collision Damage Waiver (CDW) - {vehicle}'
        assert actual_result['ss1_ss2']                    == f'{section["ss1"]} / {section["ss2"]}'
        assert actual_result['excess_reduced']             == reduce_excess
        assert actual_result['renewal']                    == 'Monthly'
        assert actual_result['policy_start']               == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']             == '$0.00'
        assert actual_result['credit_used']                == '$0.00'
        assert actual_result['total_saving']               == '$0.00'
        assert actual_result['final_amount_due']           == f'${premium}'

        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=sgt_today(), status='in_force', auto_renewal=True)
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdw_option_A_inforce_on.txt')

    def test_buy_cdw_option_A_overlap(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.not_choose_additional_coverage()
        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        # re-buy with the same user info to check overlap
        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.not_choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        assert self.checkout_page.is_overlap() is True

    def test_buy_cdw_option_A_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.not_choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        section = self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        self.checkout_page.apply_refcode(self.refcode)

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'CDW Discount $5'

        actual_result = self.checkout_page.get_data_inputted()
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']               == f'Collision Damage Waiver (CDW) - {vehicle}'
        assert actual_result['ss1_ss2']                    == f'{section["ss1"]} / {section["ss2"]}'
        assert actual_result['excess_reduced']             == reduce_excess
        assert actual_result['renewal']                    == 'Monthly'
        assert actual_result['policy_start']               == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']             == '- $5.00'
        assert actual_result['credit_used']                == '$0.00'
        assert actual_result['total_saving']               == '$5.00'

        self.opn.click_next_btn()
        charge_amount_opn = self.opn.checkout()
        assert charge_amount_opn == f'Pay {actual_result["final_amount_due"].replace("$","")} SGD'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=sgt_today(), status='in_force', auto_renewal=False)
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdw_option_A_inforce_off.txt')

    def test_buy_cdw_option_B(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.not_choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_option_b()
        combine_excess = self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        premium = self.quote_page.get_premium()
        premium = "{:.2f}".format(float((premium.split("$")[1]).split()[0])) #format premium to 2 digit

        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_data_inputted(optionB = True)
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']              == f'Collision Damage Waiver (CDW) - {vehicle}'
        assert actual_result['combined']                  == f'${combine_excess}'
        assert actual_result['excess_reduced']            == reduce_excess
        assert actual_result['renewal']                   == 'Monthly'
        assert actual_result['policy_start']              == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']            == '$0.00'
        assert actual_result['credit_used']               == '$0.00'
        assert actual_result['total_saving']              == '$0.00'
        assert actual_result['final_amount_due']          == f'${premium}'

        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=(sgt_today() - timedelta(days=32)), status='expired', auto_renewal=False)
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdw_option_B_expired_off.txt')

    def test_buy_cdw_option_B_overlap(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.not_choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_option_b()
        self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)

        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        #region re-buy with the same user info to check overlap
        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.not_choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_option_b()
        self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        assert self.checkout_page.is_overlap() is True
        #endregion re-buy with the same user info to check overlap

    def test_buy_cdw_option_B_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.not_choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        self.quote_page.choose_option_b()
        combine_excess = self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        self.checkout_page.apply_refcode(self.refcode)

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'CDW Discount $5'

        actual_result = self.checkout_page.get_data_inputted(optionB = True)
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']              == f'Collision Damage Waiver (CDW) - {vehicle}'
        assert actual_result['combined']                  == f'${combine_excess}'
        assert actual_result['excess_reduced']            == reduce_excess
        assert actual_result['renewal']                   == 'Monthly'
        assert actual_result['policy_start']              == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']            == '- $5.00'
        assert actual_result['credit_used']               == '$0.00'
        assert actual_result['total_saving']              == '$5.00'

        self.opn.click_next_btn()
        charge_amount_opn = self.opn.checkout()
        assert charge_amount_opn == f'Pay {actual_result["final_amount_due"].replace("$", "")} SGD'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=sgt_today(), status='in_force', auto_renewal=False)
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdw_option_B_inforce_off.txt')
    #endregion CDW

    #region CDW plus (CDWE)
    def test_buy_cdw_plus_option_A(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        section = self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        premium = self.quote_page.get_premium()
        premium = "{:.2f}".format(float((premium.split("$")[1]).split()[0])) #format premium to 2 digit

        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_data_inputted()
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']              == f'Collision Damage Waiver Extension (CDW) - {vehicle}'
        assert actual_result['ss1_ss2']                    == f'{section["ss1"]} / {section["ss2"]}'
        assert actual_result['excess_reduced']             == reduce_excess
        assert actual_result['renewal']                    == 'Monthly'
        assert actual_result['policy_start']               == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']             == '$0.00'
        assert actual_result['credit_used']                == '$0.00'
        assert actual_result['total_saving']               == '$0.00'
        assert actual_result['final_amount_due']           == f'${premium}'

        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=sgt_today(), status='in_force', auto_renewal=True, product_name='cdw_plus')
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdw_plus_option_A_inforce_on.txt')

    def test_buy_cdw_plus_option_A_overlap(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        # re-buy with the same user info to check overlap
        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        assert self.checkout_page.is_overlap() is True

    def test_buy_cdw_plus_option_A_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        section = self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        self.checkout_page.apply_refcode(self.refcode)

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'CDW Discount $5'

        actual_result = self.checkout_page.get_data_inputted()
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']              == f'Collision Damage Waiver Extension (CDW) - {vehicle}'
        assert actual_result['ss1_ss2']                    == f'{section["ss1"]} / {section["ss2"]}'
        assert actual_result['excess_reduced']             == reduce_excess
        assert actual_result['renewal']                    == 'Monthly'
        assert actual_result['policy_start']               == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']             == '- $5.00'
        assert actual_result['credit_used']                == '$0.00'
        assert actual_result['total_saving']               == '$5.00'

        self.opn.click_next_btn()
        charge_amount_opn = self.opn.checkout()
        assert charge_amount_opn == f'Pay {actual_result["final_amount_due"].replace("$", "")} SGD'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=sgt_today(), status='in_force', auto_renewal=False, product_name='cdw_plus')
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdw_plus_option_A_inforce_off.txt')

    def test_buy_cdw_plus_option_B(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_option_b()
        combine_excess = self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        premium = self.quote_page.get_premium()
        premium = "{:.2f}".format(float((premium.split("$")[1]).split()[0])) #format premium to 2 digit

        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_data_inputted(optionB = True)
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']              == f'Collision Damage Waiver Extension (CDW) - {vehicle}'
        assert actual_result['combined']                  == f'${combine_excess}'
        assert actual_result['excess_reduced']            == reduce_excess
        assert actual_result['renewal']                   == 'Monthly'
        assert actual_result['policy_start']              == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']            == '$0.00'
        assert actual_result['credit_used']               == '$0.00'
        assert actual_result['total_saving']              == '$0.00'
        assert actual_result['final_amount_due']          == f'${premium}'

        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=(sgt_today() - timedelta(days=32)), status='expired', auto_renewal=False, product_name='cdw_plus')
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdw_plus_option_B_expired_off.txt')

    def test_buy_cdw_plus_option_B_overlap(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_option_b()
        self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        scroll_to_bottom(self.driver)
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        # re-buy with the same user info to check overlap
        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_option_b()
        self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.click_all_checkbox()
        scroll_to_bottom(self.driver)
        self.personal_info_page.click_next_btn()

        assert self.checkout_page.is_overlap() is True

    def test_buy_cdw_plus_option_B_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_not_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_additional_coverage()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        self.quote_page.choose_option_b()
        combine_excess = self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        self.checkout_page.apply_refcode(self.refcode)

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'CDW Discount $5'

        actual_result = self.checkout_page.get_data_inputted(optionB = True)
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']              == f'Collision Damage Waiver Extension (CDW) - {vehicle}'
        assert actual_result['combined']                  == f'${combine_excess}'
        assert actual_result['excess_reduced']            == reduce_excess
        assert actual_result['renewal']                   == 'Monthly'
        assert actual_result['policy_start']              == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']            == '- $5.00'
        assert actual_result['credit_used']               == '$0.00'
        assert actual_result['total_saving']              == '$5.00'

        self.opn.click_next_btn()
        charge_amount_opn = self.opn.checkout()
        assert charge_amount_opn == f'Pay {actual_result["final_amount_due"].replace("$", "")} SGD'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=sgt_today(), status='in_force', auto_renewal=False, product_name='cdw_plus')
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdw_plus_option_B_inforce_off.txt')
    #endregion CDW plus (CDWE)

    #region CDWY (newdrivers.gigacover.com)
    def test_buy_newdrivers_weekly(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_yid)
        self.quote_page.click_purchase_now_btn()
        wait_for_loading_venta(self.driver)

        self.quote_page.click_on_acknowledge_btn()
        self.quote_page.choose_yid_type()
        self.quote_page.choose_yid_excess_list()
        self.quote_page.click_on_all_acknowledge_checkbox()

        self.quote_page.click_buy_now_btn()
        wait_for_loading_venta(self.driver)

        nric = generate_nricfin()
        self.quote_page.input_vehicle_reg(nric)

        self.quote_page.choose_start_date()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_weekly_package()
        wait_for_loading_venta(self.driver)

        actual_total_payable = self.quote_page.get_your_total_payable().replace('S', '')

        self.quote_page.click_next_btn()
        self.quote_page.click_continue_btn()

        self.personal_info_page.input_personal_info(nricfin=nric, is_cdwy=True)
        self.personal_info_page.cdwy_click_all_checkbox()
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        actual_result                           = self.checkout_page.cdwy_get_data_inputted()
        assert actual_result['product_name']    == 'MER - Weekly Plan'
        assert actual_result['renewal']         == 'Weekly'
        assert actual_result['policy_start']    == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['total_payable']   == actual_total_payable

        self.opn.click_pay_securely_btn()
        charge_amount_opn = self.opn.checkout()
        assert charge_amount_opn == f'Pay {actual_result["total_payable"].replace("$", "")} SGD'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

    def test_buy_newdrivers_monthly(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_yid)
        self.quote_page.click_purchase_now_btn()
        wait_for_loading_venta(self.driver)

        self.quote_page.click_on_acknowledge_btn()
        self.quote_page.choose_yid_type()
        self.quote_page.choose_yid_excess_list()
        self.quote_page.click_on_all_acknowledge_checkbox()

        self.quote_page.click_buy_now_btn()
        wait_for_loading_venta(self.driver)

        nric = generate_nricfin()
        self.quote_page.input_vehicle_reg(nric)

        self.quote_page.choose_start_date()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_monthly_package()
        wait_for_loading_venta(self.driver)

        actual_total_payable = self.quote_page.get_your_total_payable().replace('S', '')

        self.quote_page.click_next_btn()
        self.quote_page.click_continue_btn()

        self.personal_info_page.input_personal_info(nricfin=nric, is_cdwy=True)
        self.personal_info_page.cdwy_click_all_checkbox()
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        actual_result                           = self.checkout_page.cdwy_get_data_inputted()
        assert actual_result['product_name']    == 'MER - Monthly Plan'
        assert actual_result['renewal']         == 'Monthly'
        assert actual_result['policy_start']    == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['total_payable']   == actual_total_payable

        self.opn.click_pay_securely_btn()
        charge_amount_opn = self.opn.checkout()
        assert charge_amount_opn == f'Pay SGD {actual_result["total_payable"]}'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

    def test_buy_newdrivers_weekly_overlap(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_yid)
        self.quote_page.click_purchase_now_btn()
        wait_for_loading_venta(self.driver)

        self.quote_page.click_on_acknowledge_btn()
        self.quote_page.choose_yid_type()
        self.quote_page.choose_yid_excess_list()
        self.quote_page.click_on_all_acknowledge_checkbox()

        self.quote_page.click_buy_now_btn()
        wait_for_loading_venta(self.driver)

        nric = generate_nricfin()
        self.quote_page.input_vehicle_reg(nric)

        self.quote_page.choose_start_date()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_weekly_package()
        wait_for_loading_venta(self.driver)

        self.quote_page.click_next_btn()
        self.quote_page.click_continue_btn()

        self.personal_info_page.input_personal_info(nricfin=nric, is_cdwy=True)
        self.personal_info_page.cdwy_click_all_checkbox()
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.opn.click_pay_securely_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        # re-buy to check overlap (cdwy didn't clear user info after self-buy success)
        self.home_page.open_url(url.url_yid)
        self.quote_page.click_purchase_now_btn()
        wait_for_loading_venta(self.driver)

        self.quote_page.click_on_acknowledge_btn()
        self.quote_page.choose_yid_type()
        self.quote_page.choose_yid_excess_list()
        self.quote_page.click_on_all_acknowledge_checkbox()

        self.quote_page.click_buy_now_btn()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_start_date()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_weekly_package()
        wait_for_loading_venta(self.driver)

        self.quote_page.click_next_btn()
        self.quote_page.click_continue_btn()

        wait_for_loading_venta(self.driver)
        self.personal_info_page.cdwy_click_all_checkbox()
        self.personal_info_page.click_next_btn()

        assert self.checkout_page.is_overlap() is True

    def test_buy_newdrivers_monthly_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_yid)
        self.quote_page.click_purchase_now_btn()
        wait_for_loading_venta(self.driver)

        self.quote_page.click_on_acknowledge_btn()
        self.quote_page.choose_yid_type()
        self.quote_page.choose_yid_excess_list()
        self.quote_page.click_on_all_acknowledge_checkbox()

        self.quote_page.click_buy_now_btn()
        wait_for_loading_venta(self.driver)

        nric = generate_nricfin()
        self.quote_page.input_vehicle_reg(nric)

        self.quote_page.choose_start_date()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_monthly_package()
        wait_for_loading_venta(self.driver)

        self.quote_page.click_next_btn()
        self.quote_page.click_continue_btn()

        self.personal_info_page.input_personal_info(nricfin=nric, is_cdwy=True)
        self.personal_info_page.cdwy_click_all_checkbox()
        self.personal_info_page.click_next_btn()

        self.checkout_page.apply_refcode(self.refcode)
        wait_for_loading_venta(self.driver)

        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'CDW Discount $5'

        wait_for_loading_venta(self.driver)
        actual_result                               = self.checkout_page.cdwy_get_data_inputted()
        assert actual_result['product_name']        == 'MER - Monthly Plan'
        assert actual_result['renewal']             == 'Monthly'
        assert actual_result['policy_start']        == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']      == '- $5.00'
        assert actual_result['total_saving']        == '$5.00'

        self.opn.click_pay_securely_btn()
        charge_amount_opn = self.opn.checkout()
        assert charge_amount_opn == f'Pay {actual_result["total_payable"].replace("$", "")} SGD'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

    def test_verify_redirect_to_newdrivers_page(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_personal_vehicle()
        wait_for_loading_venta(self.driver)

        assert self.driver.current_url == 'https://newdrivers.gigacover.com/'
    #endregion CDWY (newdrivers.gigacover.com)

    #region CDWY (CDW x 2.85)
    def test_buy_cdwy_option_A(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_rented_vehicle()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        section = self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        premium = self.quote_page.get_premium()
        premium = "{:.2f}".format(float((premium.split("$")[1]).split()[0])) #format premium to 2 digit

        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_data_inputted()
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']               == f'Collision Damage Waiver (CDW) - {vehicle}'
        assert actual_result['ss1_ss2']                    == f'{section["ss1"]} / {section["ss2"]}'
        assert actual_result['excess_reduced']             == reduce_excess
        assert actual_result['renewal']                    == 'Monthly'
        assert actual_result['policy_start']               == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']             == '$0.00'
        assert actual_result['credit_used']                == '$0.00'
        assert actual_result['total_saving']               == '$0.00'
        assert actual_result['final_amount_due']           == f'${premium}'

        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=sgt_today(), status='in_force', auto_renewal=True, product_name='cdw_plus')
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdwy_option_A_inforce_on.txt')

    def test_buy_cdwy_option_A_overlap(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_rented_vehicle()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        # re-buy with the same user info to check overlap
        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_rented_vehicle()
        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        assert self.checkout_page.is_overlap() is True

    def test_buy_cdwy_option_A_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_rented_vehicle()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        section = self.quote_page.choose_ss1_ss2()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        self.personal_info_page.click_next_btn()

        self.checkout_page.apply_refcode(self.refcode)

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'CDW Discount $5'

        actual_result = self.checkout_page.get_data_inputted()
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']               == f'Collision Damage Waiver (CDW) - {vehicle}'
        assert actual_result['ss1_ss2']                    == f'{section["ss1"]} / {section["ss2"]}'
        assert actual_result['excess_reduced']             == reduce_excess
        assert actual_result['renewal']                    == 'Monthly'
        assert actual_result['policy_start']               == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']             == '- $5.00'
        assert actual_result['credit_used']                == '$0.00'
        assert actual_result['total_saving']               == '$5.00'

        self.opn.click_next_btn()
        charge_amount_opn = self.opn.checkout()
        assert charge_amount_opn == f'Pay {actual_result["final_amount_due"].replace("$", "")} SGD'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=sgt_today(), status='in_force', auto_renewal=False, product_name='cdw_plus')
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdwy_option_A_inforce_off.txt')

    def test_buy_cdwy_option_B(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_rented_vehicle()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_option_b()
        combine_excess = self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        premium = self.quote_page.get_premium()
        premium = "{:.2f}".format(float((premium.split("$")[1]).split()[0])) #format premium to 2 digit

        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        actual_result = self.checkout_page.get_data_inputted(optionB = True)
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']              == f'Collision Damage Waiver (CDW) - {vehicle}'
        assert actual_result['combined']                  == f'${combine_excess}'
        assert actual_result['excess_reduced']            == reduce_excess
        assert actual_result['renewal']                   == 'Monthly'
        assert actual_result['policy_start']              == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']            == '$0.00'
        assert actual_result['credit_used']               == '$0.00'
        assert actual_result['total_saving']              == '$0.00'
        assert actual_result['final_amount_due']          == f'${premium}'

        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=(sgt_today() - timedelta(days=32)), status='expired', auto_renewal=False, product_name='cdw_plus')
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdwy_option_B_expired_off.txt')

    def test_buy_cdwy_option_B_overlap(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_rented_vehicle()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_option_b()
        self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()
        scroll_to_bottom(self.driver)
        self.personal_info_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.opn.click_next_btn()
        self.opn.checkout()

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        # re-buy with the same user info to check overlap
        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_rented_vehicle()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_vehicle()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_option_b()
        self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        self.personal_info_page.click_all_checkbox()
        scroll_to_bottom(self.driver)
        self.personal_info_page.click_next_btn()

        assert self.checkout_page.is_overlap() is True

    def test_buy_cdwy_option_B_with_refcode(self):
        self.setUp_fixture()

        self.home_page.open_url(url.url_venta_cdw)

        self.quote_page.choose_individual_option()
        wait_for_loading_venta(self.driver)

        self.quote_page.is_young_and_inexperienced()
        wait_for_loading_venta(self.driver)

        self.quote_page.choose_rented_vehicle()
        wait_for_loading_venta(self.driver)

        vehicle = self.quote_page.choose_vehicle()

        self.quote_page.choose_option_b()
        combine_excess = self.quote_page.choose_combine_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        reduce_excess = self.quote_page.choose_reduce_excess()
        self.quote_page.click_next_btn()

        wait_for_loading_venta(self.driver)
        self.quote_page.click_on_quote_page_checkbox()
        self.quote_page.click_next_btn()

        #save data for testcase on webportal
        nricfin = generate_nricfin()
        self.personal_info_page.input_personal_info(nricfin)
        self.personal_info_page.click_all_checkbox()

        scroll_to_bottom(self.driver)

        self.personal_info_page.click_next_btn()

        self.checkout_page.apply_refcode(self.refcode)

        wait_for_loading_venta(self.driver)
        refcode_msg = self.checkout_page.get_refcode_msg(self.refcode)
        assert refcode_msg == 'CDW Discount $5'

        actual_result = self.checkout_page.get_data_inputted(optionB = True)
        if vehicle == 'Motorcycle': vehicle = 'Bike'
        assert actual_result['product_name']              == f'Collision Damage Waiver (CDW) - {vehicle}'
        assert actual_result['combined']                  == f'${combine_excess}'
        assert actual_result['excess_reduced']            == reduce_excess
        assert actual_result['renewal']                   == 'Monthly'
        assert actual_result['policy_start']              == (sgt_today() + timedelta(days=1)).strftime('%d %b %Y')
        assert actual_result['promo_discount']            == '- $5.00'
        assert actual_result['credit_used']               == '$0.00'
        assert actual_result['total_saving']              == '$5.00'

        self.opn.click_next_btn()
        charge_amount_opn = self.opn.checkout()
        assert charge_amount_opn == f'Pay {actual_result["final_amount_due"].replace("$", "")} SGD'

        wait_for_loading_venta(self.driver)
        assert self.checkout_page.is_buy_success() is True

        email = f'{nricfin}@gigacover.com'
        create_fixture_for_cdw(email=email, start_date=sgt_today(), status='in_force', auto_renewal=False, product_name='cdw_plus')
        write_to_file(email, f'{WORKING_DIR_FIXTURE}/cdwy_option_B_inforce_off.txt')
    #endregion CDWY (CDW x 2.85)

    #TODO find a way write testcase self-buy with user_balance
