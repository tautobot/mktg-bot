from datetime import timedelta

from aqa.src.pages.dashboard.checkout_page import DashboardCheckoutPage
from aqa.src.pages.dashboard.claim_page import MerClaimPage
from aqa.src.pages.dashboard.vehicle_details_page import MerVehicleDetailsPage
from aqa.src.tests.base import BaseTest
from aqa.src.pages.dashboard.home_page import MerDashboardHomePage
from aqa.src.pages.dashboard.login_page import DashboardLoginPage

from aqa.utils.generic import generate_nricfin, cook_fixture_mer, read_cell_in_excel_file

from aqa.utils.enums import account, path
from aqa.utils.helper import sgt_today, db_query_phoenix
from aqa.utils.webdriver_util import wait_loading_dashboard, wait_for_loading_venta, wait_loading_mer_dashboard

template_file    = f'{path.fixture_dir}/mer_template.xlsx'


class Test(BaseTest):
    def setUp_fixture(self):
        self.login_page         = DashboardLoginPage(self.driver)
        self.home_page          = MerDashboardHomePage(self.driver)
        self.vehicle_details    = MerVehicleDetailsPage(self.driver)
        self.checkout_page      = DashboardCheckoutPage(self.driver)
        self.claim_page         = MerClaimPage(self.driver)

    #region owner Mer
    def test_add_vehicle_per_excess_plan(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_one_vehicle_btn()

        vehicle_reg = generate_nricfin()
        self.home_page.input_vehicle_info(vehicle_reg)

        vehicle_type = self.home_page.choose_random_vehicle_type()
        per_excess_plan_data = self.home_page.choose_per_excess_plan()
        self.home_page.click_on_confirm_btn()

        wait_for_loading_venta(self.driver)

        actual_data                                            = self.home_page.get_review_data()
        assert actual_data['vehicle_reg'].strip()             == vehicle_reg
        assert actual_data['company_uen'].strip()             == 'company uen'
        assert actual_data['company_name'].strip()            == 'company name'
        assert actual_data['contact_num'].strip()             == 'contact number'
        assert actual_data['contact_email'].strip()           == f'{vehicle_reg}@gigacover.com'
        assert actual_data['model'].strip()                   == 'vehicle model'
        assert actual_data['make'].strip()                    == 'vehicle make'
        assert actual_data['chassis'].strip()                 == 'chassis no'
        assert actual_data['engine'].strip()                  == 'engine no'
        assert actual_data['vehicle_type'].strip()            == vehicle_type
        assert actual_data['section1excess'].strip()          == f"${per_excess_plan_data['ss1']}"
        assert actual_data['section2excess'].strip()          == per_excess_plan_data['ss2']
        assert actual_data['combined_excess'].strip()         == '$0'
        assert actual_data['reduced_excess'].strip()          == per_excess_plan_data['reduced_excess']
        assert actual_data['unit'].strip()                    == 'Monthly'
        assert actual_data['start_date'].strip()              == (sgt_today() + timedelta(days=1)).strftime('%d/%m/%Y')

        self.home_page.click_on_confirm_btn()

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_add_vehicle_combined_plan(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_one_vehicle_btn()

        vehicle_reg = generate_nricfin()
        self.home_page.input_vehicle_info(vehicle_reg)

        vehicle_type = self.home_page.choose_random_vehicle_type()
        combined_plan_data = self.home_page.choose_combined_plan()
        self.home_page.click_on_confirm_btn()

        wait_for_loading_venta(self.driver)

        actual_data                                            = self.home_page.get_review_data()
        assert actual_data['vehicle_reg'].strip()             == vehicle_reg
        assert actual_data['company_uen'].strip()             == 'company uen'
        assert actual_data['company_name'].strip()            == 'company name'
        assert actual_data['contact_num'].strip()             == 'contact number'
        assert actual_data['contact_email'].strip()           == f'{vehicle_reg}@gigacover.com'
        assert actual_data['model'].strip()                   == 'vehicle model'
        assert actual_data['make'].strip()                    == 'vehicle make'
        assert actual_data['chassis'].strip()                 == 'chassis no'
        assert actual_data['engine'].strip()                  == 'engine no'
        assert actual_data['vehicle_type'].strip()            == vehicle_type
        assert actual_data['section1excess'].strip()          == '$0'
        assert actual_data['section2excess'].strip()          == '$0'
        assert actual_data['combined_excess'].strip()         == f'${combined_plan_data["combined_excess"]}'
        assert actual_data['reduced_excess'].strip()          == f'{combined_plan_data["reduced_excess"]}'
        assert actual_data['unit'].strip()                    == 'Monthly'
        assert actual_data['start_date'].strip()              == (sgt_today() + timedelta(days=1)).strftime('%d/%m/%Y')

        self.home_page.click_on_confirm_btn()

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.choose_paynow_payment_method()
        self.checkout_page.click_on_next_btn()

        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_upload_vehicles_with_card(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')
        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_upload_vehicles_with_paynow(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.choose_paynow_payment_method()
        self.checkout_page.click_on_next_btn()

        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')
        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_validate_auto_renewal_on(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_auto_renewal']      == 'On'

    def test_validate_auto_renewal_off(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A3')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_auto_renewal']      == 'Off'

    def test_validate_vehicle_info_section_plan(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()
        self.home_page.upload_file(template_file)
        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()
        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_vehicle_reg']       == vehicle_reg
        assert actual_vehicle_info['actual_vehicle_type']      == 'Car'
        assert actual_vehicle_info['actual_contact_email']     == f'{vehicle_reg.lower()}@gigacover.com'
        assert actual_vehicle_info['actual_contact_number']    == '36003660'
        assert actual_vehicle_info['actual_company_uen']       == 'MERUEN'
        assert actual_vehicle_info['actual_company_name']      == 'Gojek'
        assert actual_vehicle_info['actual_ss1']               == '2000'
        assert actual_vehicle_info['actual_ss2']               == '2000'
        assert actual_vehicle_info['actual_reduced_excess']    == '500'
        assert actual_vehicle_info['actual_combined_excess']   == '0'
        assert actual_vehicle_info['actual_start_date']        == (sgt_today() + timedelta(days=1)).strftime("%d/%m/%Y")
        assert actual_vehicle_info['actual_chassis_no']        == 'ChassisNo'
        assert actual_vehicle_info['actual_upcoming_status']   == 'Paid'
        assert actual_vehicle_info['actual_auto_renewal']      == 'On'

    def test_validate_vehicle_info_combined_plan(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()
        self.home_page.upload_file(template_file)
        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()
        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A3')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_vehicle_reg']       == vehicle_reg
        assert actual_vehicle_info['actual_vehicle_type']      == 'Car'
        assert actual_vehicle_info['actual_contact_email']     == f'{vehicle_reg.lower()}@gigacover.com'
        assert actual_vehicle_info['actual_contact_number']    == '36003660'
        assert actual_vehicle_info['actual_company_uen']       == 'MERUEN'
        assert actual_vehicle_info['actual_company_name']      == 'Gojek'
        assert actual_vehicle_info['actual_ss1']               == '0'
        assert actual_vehicle_info['actual_ss2']               == '0'
        assert actual_vehicle_info['actual_reduced_excess']    == '1000'
        assert actual_vehicle_info['actual_combined_excess']   == '2500'
        assert actual_vehicle_info['actual_start_date']        == (sgt_today() + timedelta(days=1)).strftime("%d/%m/%Y")
        assert actual_vehicle_info['actual_chassis_no']        == 'ChassisNo'
        assert actual_vehicle_info['actual_upcoming_status']   == 'Paid'
        assert actual_vehicle_info['actual_auto_renewal']      == 'Off'

    def test_change_auto_renewal(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)
        wait_loading_mer_dashboard(self.driver)

        vehicle_reg = db_query_phoenix("select vehicle_reg from order_details od join orders o on o.id = od.order_id  where od.sale_type = 'mer' and next_prepare_date is not null and od.status != 'pending' and o.source_group_id = 80 order by vehicle_reg desc limit 1", 'vehicle_reg_change_auto_renewal')
        self.home_page.search_vehicle(vehicle_reg.strip())
        wait_loading_mer_dashboard(self.driver)

        auto_renewal_before = self.home_page.get_auto_renewal_status()
        assert auto_renewal_before == 'On'

        self.home_page.turn_off_auto_renewal()
        wait_loading_mer_dashboard(self.driver)
        auto_renewal_after = self.home_page.get_auto_renewal_status()
        assert auto_renewal_after == 'Off'

    def test_claim_with_documents(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)
        wait_loading_mer_dashboard(self.driver)

        self.home_page.go_to_claim_page()
        wait_loading_mer_dashboard(self.driver)

        self.claim_page.click_on_new_claim_btn()
        self.claim_page.choose_claim_with_documents()

        vehicle_reg = db_query_phoenix("select vehicle_reg from order_details od join orders o on o.id = od.order_id  where od.sale_type = 'mer' and next_prepare_date is not null and od.status = 'in_force' and o.source_group_id = 80 order by vehicle_reg desc limit 1", 'vehicle_reg_claim_with_documents')
        self.claim_page.choose_vehicle_reg(vehicle_reg.strip())

        self.claim_page.input_claim_details()
        self.claim_page.input_disbursement_detail()
        self.claim_page.upload_required_documents()

        self.claim_page.click_all_checkbox()
        self.claim_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_page.is_claim_successful() is True

    def test_claim_with_no_documents(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)
        wait_loading_mer_dashboard(self.driver)

        self.home_page.go_to_claim_page()
        wait_loading_mer_dashboard(self.driver)

        self.claim_page.click_on_new_claim_btn()
        self.claim_page.choose_claim_with_no_documents()

        vehicle_reg = db_query_phoenix("select vehicle_reg from order_details od join orders o on o.id = od.order_id  where od.sale_type = 'mer' and next_prepare_date is not null and od.status = 'in_force' and o.source_group_id = 80 order by vehicle_reg desc limit 1", 'vehicle_reg_claim_with_no_documents')
        self.claim_page.choose_vehicle_reg(vehicle_reg.strip())

        self.claim_page.input_claim_details()
        self.claim_page.input_disbursement_detail()

        self.claim_page.click_all_checkbox()
        self.claim_page.click_submit_btn()

        wait_for_loading_venta(self.driver)
        assert self.claim_page.is_claim_successful() is True

    def test_change_start_date(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)
        wait_loading_mer_dashboard(self.driver)

        today = sgt_today()
        vehicle_reg = db_query_phoenix(f"select vehicle_reg from order_details od join orders o on o.id = od.order_id  where od.sale_type = 'mer' and next_prepare_date is not null and od.status = 'pending' and od.start_date >= '{today}' and o.source_group_id = 80 limit 1", 'vehicle_reg_change_start_date')

        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_mer_dashboard(self.driver)

        start_date_before = self.home_page.get_upcoming_start_date()
        next_start_date = self.home_page.change_upcoming_start_date()

        wait_loading_mer_dashboard(self.driver)

        start_date_after          = self.home_page.get_upcoming_start_date()
        assert start_date_before != start_date_after
        assert next_start_date   == start_date_after
    #endregion owner Mer

    #region admin Mer
    def test_confirm_payment(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_admin_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)
        wait_loading_mer_dashboard(self.driver)

        today = sgt_today()
        vehicle_reg = db_query_phoenix(f"select vehicle_reg from order_details od join orders o on o.id = od.order_id  where od.sale_type = 'mer' and next_prepare_date is not null and od.status = 'pending' and od.start_date >= '{today}' limit 1", 'vehicle_reg_confirm_payment')
        self.home_page.search_vehicle(vehicle_reg.strip())
        wait_loading_mer_dashboard(self.driver)

        before_upcoming_status = self.home_page.get_upcoming_status()
        assert before_upcoming_status in ['Prepared', 'Pending']

        self.home_page.confirm_paynow_payment()

        wait_loading_mer_dashboard(self.driver)
        after_upcoming_status = self.home_page.get_upcoming_status()
        assert after_upcoming_status == 'Paid'
    #endregion admin Mer

    #region only have paynow
    def test_paynow_add_vehicle_per_excess_plan(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_paynow, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_one_vehicle_btn()

        vehicle_reg = generate_nricfin()
        self.home_page.input_vehicle_info(vehicle_reg)

        vehicle_type = self.home_page.choose_random_vehicle_type()
        per_excess_plan_data = self.home_page.choose_per_excess_plan()
        self.home_page.click_on_confirm_btn()

        wait_for_loading_venta(self.driver)

        actual_data                                            = self.home_page.get_review_data()
        assert actual_data['vehicle_reg'].strip()             == vehicle_reg
        assert actual_data['company_uen'].strip()             == 'company uen'
        assert actual_data['company_name'].strip()            == 'company name'
        assert actual_data['contact_num'].strip()             == 'contact number'
        assert actual_data['contact_email'].strip()           == f'{vehicle_reg}@gigacover.com'
        assert actual_data['model'].strip()                   == 'vehicle model'
        assert actual_data['make'].strip()                    == 'vehicle make'
        assert actual_data['chassis'].strip()                 == 'chassis no'
        assert actual_data['engine'].strip()                  == 'engine no'
        assert actual_data['vehicle_type'].strip()            == vehicle_type
        assert actual_data['section1excess'].strip()          == f"${per_excess_plan_data['ss1']}"
        assert actual_data['section2excess'].strip()          == per_excess_plan_data['ss2']
        assert actual_data['combined_excess'].strip()         == '$0'
        assert actual_data['reduced_excess'].strip()          == per_excess_plan_data['reduced_excess']
        assert actual_data['unit'].strip()                    == 'Monthly'
        assert actual_data['start_date'].strip()              == (sgt_today() + timedelta(days=1)).strftime('%d/%m/%Y')

        self.home_page.click_on_confirm_btn()

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.choose_paynow_payment_method()

        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_paynow_add_vehicle_combined_plan(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_paynow, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_one_vehicle_btn()

        vehicle_reg = generate_nricfin()
        self.home_page.input_vehicle_info(vehicle_reg)

        vehicle_type = self.home_page.choose_random_vehicle_type()
        combined_plan_data = self.home_page.choose_combined_plan()
        self.home_page.click_on_confirm_btn()

        wait_for_loading_venta(self.driver)

        actual_data                                            = self.home_page.get_review_data()
        assert actual_data['vehicle_reg'].strip()             == vehicle_reg
        assert actual_data['company_uen'].strip()             == 'company uen'
        assert actual_data['company_name'].strip()            == 'company name'
        assert actual_data['contact_num'].strip()             == 'contact number'
        assert actual_data['contact_email'].strip()           == f'{vehicle_reg}@gigacover.com'
        assert actual_data['model'].strip()                   == 'vehicle model'
        assert actual_data['make'].strip()                    == 'vehicle make'
        assert actual_data['chassis'].strip()                 == 'chassis no'
        assert actual_data['engine'].strip()                  == 'engine no'
        assert actual_data['vehicle_type'].strip()            == vehicle_type
        assert actual_data['section1excess'].strip()          == '$0'
        assert actual_data['section2excess'].strip()          == '$0'
        assert actual_data['combined_excess'].strip()         == f'${combined_plan_data["combined_excess"]}'
        assert actual_data['reduced_excess'].strip()          == f'{combined_plan_data["reduced_excess"]}'
        assert actual_data['unit'].strip()                    == 'Monthly'
        assert actual_data['start_date'].strip()              == (sgt_today() + timedelta(days=1)).strftime('%d/%m/%Y')

        self.home_page.click_on_confirm_btn()

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.choose_paynow_payment_method()
        self.checkout_page.click_on_next_btn()

        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_paynow_upload_vehicles_with_card(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paynow, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.choose_paynow_payment_method()

        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')
        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_paynow_upload_vehicles_with_paynow(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paynow, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.choose_paynow_payment_method()
        self.checkout_page.click_on_next_btn()

        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')
        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_paynow_validate_auto_renewal_on(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paynow, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.choose_paynow_payment_method()

        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_auto_renewal']      == 'On'

    def test_paynow_validate_auto_renewal_off(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paynow, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.choose_paynow_payment_method()

        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A3')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_auto_renewal']      == 'Off'

    def test_paynow_validate_vehicle_info_section_plan(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paynow, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()
        self.home_page.upload_file(template_file)
        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.choose_paynow_payment_method()

        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_vehicle_reg']       == vehicle_reg
        assert actual_vehicle_info['actual_vehicle_type']      == 'Car'
        assert actual_vehicle_info['actual_contact_email']     == f'{vehicle_reg.lower()}@gigacover.com'
        assert actual_vehicle_info['actual_contact_number']    == '36003660'
        assert actual_vehicle_info['actual_company_uen']       == 'MERUEN'
        assert actual_vehicle_info['actual_company_name']      == 'Gojek'
        assert actual_vehicle_info['actual_ss1']               == '2000'
        assert actual_vehicle_info['actual_ss2']               == '2000'
        assert actual_vehicle_info['actual_reduced_excess']    == '500'
        assert actual_vehicle_info['actual_combined_excess']   == '0'
        assert actual_vehicle_info['actual_start_date']        == (sgt_today() + timedelta(days=1)).strftime("%d/%m/%Y")
        assert actual_vehicle_info['actual_chassis_no']        == 'ChassisNo'
        assert actual_vehicle_info['actual_upcoming_status']   == 'Pending'
        assert actual_vehicle_info['actual_auto_renewal']      == 'On'

    def test_paynow_validate_vehicle_info_combined_plan(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paynow, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()
        self.home_page.upload_file(template_file)
        wait_loading_dashboard(self.driver)

        self.checkout_page.click_on_checkout_btn()

        self.checkout_page.choose_paynow_payment_method()

        self.checkout_page.click_on_next_btn()
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A3')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_vehicle_reg']       == vehicle_reg
        assert actual_vehicle_info['actual_vehicle_type']      == 'Car'
        assert actual_vehicle_info['actual_contact_email']     == f'{vehicle_reg.lower()}@gigacover.com'
        assert actual_vehicle_info['actual_contact_number']    == '36003660'
        assert actual_vehicle_info['actual_company_uen']       == 'MERUEN'
        assert actual_vehicle_info['actual_company_name']      == 'Gojek'
        assert actual_vehicle_info['actual_ss1']               == '0'
        assert actual_vehicle_info['actual_ss2']               == '0'
        assert actual_vehicle_info['actual_reduced_excess']    == '1000'
        assert actual_vehicle_info['actual_combined_excess']   == '2500'
        assert actual_vehicle_info['actual_start_date']        == (sgt_today() + timedelta(days=1)).strftime("%d/%m/%Y")
        assert actual_vehicle_info['actual_chassis_no']        == 'ChassisNo'
        assert actual_vehicle_info['actual_upcoming_status']   == 'Pending'
        assert actual_vehicle_info['actual_auto_renewal']      == 'Off'

    def test_paynow_change_auto_renewal(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_paynow, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)
        wait_loading_mer_dashboard(self.driver)

        vehicle_reg = db_query_phoenix("select vehicle_reg from order_details od join orders o on o.id = od.order_id  where od.sale_type = 'mer' and next_prepare_date is not null and od.status != 'pending' and o.source_group_id = 77 order by vehicle_reg desc limit 1", 'vehicle_reg_change_auto_renewal')
        self.home_page.search_vehicle(vehicle_reg.strip())
        wait_loading_mer_dashboard(self.driver)

        auto_renewal_before = self.home_page.get_auto_renewal_status()
        assert auto_renewal_before == 'On'

        self.home_page.turn_off_auto_renewal()
        wait_loading_mer_dashboard(self.driver)
        auto_renewal_after = self.home_page.get_auto_renewal_status()
        assert auto_renewal_after == 'Off'
    #endregion only have paynow

    #region only have paylater
    def test_paylater_add_vehicle_per_excess_plan(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_paylater, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_one_vehicle_btn()

        vehicle_reg = generate_nricfin()
        self.home_page.input_vehicle_info(vehicle_reg)

        vehicle_type = self.home_page.choose_random_vehicle_type()
        per_excess_plan_data = self.home_page.choose_per_excess_plan()
        self.home_page.click_on_confirm_btn()

        wait_for_loading_venta(self.driver)

        actual_data                                            = self.home_page.get_review_data()
        assert actual_data['vehicle_reg'].strip()             == vehicle_reg
        assert actual_data['company_uen'].strip()             == 'company uen'
        assert actual_data['company_name'].strip()            == 'company name'
        assert actual_data['contact_num'].strip()             == 'contact number'
        assert actual_data['contact_email'].strip()           == f'{vehicle_reg}@gigacover.com'
        assert actual_data['model'].strip()                   == 'vehicle model'
        assert actual_data['make'].strip()                    == 'vehicle make'
        assert actual_data['chassis'].strip()                 == 'chassis no'
        assert actual_data['engine'].strip()                  == 'engine no'
        assert actual_data['vehicle_type'].strip()            == vehicle_type
        assert actual_data['section1excess'].strip()          == f"${per_excess_plan_data['ss1']}"
        assert actual_data['section2excess'].strip()          == per_excess_plan_data['ss2']
        assert actual_data['combined_excess'].strip()         == '$0'
        assert actual_data['reduced_excess'].strip()          == per_excess_plan_data['reduced_excess']
        assert actual_data['unit'].strip()                    == 'Monthly'
        assert actual_data['start_date'].strip()              == (sgt_today() + timedelta(days=1)).strftime('%d/%m/%Y')

        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_paylater_add_vehicle_combined_plan(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_paylater, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_one_vehicle_btn()

        vehicle_reg = generate_nricfin()
        self.home_page.input_vehicle_info(vehicle_reg)

        vehicle_type = self.home_page.choose_random_vehicle_type()
        combined_plan_data = self.home_page.choose_combined_plan()
        self.home_page.click_on_confirm_btn()

        wait_for_loading_venta(self.driver)

        actual_data                                            = self.home_page.get_review_data()
        assert actual_data['vehicle_reg'].strip()             == vehicle_reg
        assert actual_data['company_uen'].strip()             == 'company uen'
        assert actual_data['company_name'].strip()            == 'company name'
        assert actual_data['contact_num'].strip()             == 'contact number'
        assert actual_data['contact_email'].strip()           == f'{vehicle_reg}@gigacover.com'
        assert actual_data['model'].strip()                   == 'vehicle model'
        assert actual_data['make'].strip()                    == 'vehicle make'
        assert actual_data['chassis'].strip()                 == 'chassis no'
        assert actual_data['engine'].strip()                  == 'engine no'
        assert actual_data['vehicle_type'].strip()            == vehicle_type
        assert actual_data['section1excess'].strip()          == '$0'
        assert actual_data['section2excess'].strip()          == '$0'
        assert actual_data['combined_excess'].strip()         == f'${combined_plan_data["combined_excess"]}'
        assert actual_data['reduced_excess'].strip()          == f'{combined_plan_data["reduced_excess"]}'
        assert actual_data['unit'].strip()                    == 'Monthly'
        assert actual_data['start_date'].strip()              == (sgt_today() + timedelta(days=1)).strftime('%d/%m/%Y')

        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_paylater_upload_vehicles_with_card(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paylater, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')
        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_paylater_upload_vehicles_with_paynow(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paylater, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        #verify vehicle is added success
        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')
        self.home_page.search_vehicle(vehicle_reg)
        wait_loading_dashboard(self.driver)

        assert self.home_page.vehicle_is_displayed(vehicle_reg) is True

    def test_paylater_validate_auto_renewal_on(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paylater, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_auto_renewal']      == 'On'

    def test_paylater_validate_auto_renewal_off(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paylater, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()

        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A3')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_auto_renewal']      == 'Off'

    def test_paylater_validate_vehicle_info_section_plan(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paylater, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()
        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A2')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_vehicle_reg']       == vehicle_reg
        assert actual_vehicle_info['actual_vehicle_type']      == 'Car'
        assert actual_vehicle_info['actual_contact_email']     == f'{vehicle_reg.lower()}@gigacover.com'
        assert actual_vehicle_info['actual_contact_number']    == '36003660'
        assert actual_vehicle_info['actual_company_uen']       == 'MERUEN'
        assert actual_vehicle_info['actual_company_name']      == 'Gojek'
        assert actual_vehicle_info['actual_ss1']               == '2000'
        assert actual_vehicle_info['actual_ss2']               == '2000'
        assert actual_vehicle_info['actual_reduced_excess']    == '500'
        assert actual_vehicle_info['actual_combined_excess']   == '0'
        assert actual_vehicle_info['actual_start_date']        == (sgt_today() + timedelta(days=1)).strftime("%d/%m/%Y")
        assert actual_vehicle_info['actual_chassis_no']        == 'ChassisNo'
        assert actual_vehicle_info['actual_upcoming_status']   == 'Paid'
        assert actual_vehicle_info['actual_auto_renewal']      == 'On'

    def test_paylater_validate_vehicle_info_combined_plan(self):
        self.setUp_fixture()

        cook_fixture_mer()

        self.login_page.login_dashboard(account.mer_owner_paylater, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_vehicles_btn()
        self.home_page.upload_file(template_file)

        wait_loading_dashboard(self.driver)
        self.home_page.click_on_confirm_btn()

        wait_loading_dashboard(self.driver)
        assert self.checkout_page.is_purchase_successful() is True

        self.checkout_page.click_on_back_to_overview_btn()
        wait_loading_dashboard(self.driver)

        vehicle_reg = read_cell_in_excel_file(template_file, 'A3')

        self.home_page.search_vehicle(vehicle_reg)
        self.home_page.click_on_vehicle_reg(vehicle_reg)

        wait_loading_dashboard(self.driver)

        actual_vehicle_info                                     = self.vehicle_details.get_vehicle_info()
        assert actual_vehicle_info['actual_vehicle_reg']       == vehicle_reg
        assert actual_vehicle_info['actual_vehicle_type']      == 'Car'
        assert actual_vehicle_info['actual_contact_email']     == f'{vehicle_reg.lower()}@gigacover.com'
        assert actual_vehicle_info['actual_contact_number']    == '36003660'
        assert actual_vehicle_info['actual_company_uen']       == 'MERUEN'
        assert actual_vehicle_info['actual_company_name']      == 'Gojek'
        assert actual_vehicle_info['actual_ss1']               == '0'
        assert actual_vehicle_info['actual_ss2']               == '0'
        assert actual_vehicle_info['actual_reduced_excess']    == '1000'
        assert actual_vehicle_info['actual_combined_excess']   == '2500'
        assert actual_vehicle_info['actual_start_date']        == (sgt_today() + timedelta(days=1)).strftime("%d/%m/%Y")
        assert actual_vehicle_info['actual_chassis_no']        == 'ChassisNo'
        assert actual_vehicle_info['actual_upcoming_status']   == 'Paid'
        assert actual_vehicle_info['actual_auto_renewal']      == 'Off'

    def test_paylater_change_auto_renewal(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.mer_owner_paylater, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.driver.refresh()
        wait_loading_dashboard(self.driver)
        wait_loading_mer_dashboard(self.driver)

        vehicle_reg = db_query_phoenix("select vehicle_reg from order_details od join orders o on o.id = od.order_id  where od.sale_type = 'mer' and next_prepare_date is not null and od.status != 'pending' and o.source_group_id = 77 order by vehicle_reg desc limit 1", 'vehicle_reg_change_auto_renewal')
        self.home_page.search_vehicle(vehicle_reg.strip())
        wait_loading_mer_dashboard(self.driver)

        auto_renewal_before = self.home_page.get_auto_renewal_status()
        assert auto_renewal_before == 'On'

        self.home_page.turn_off_auto_renewal()
        wait_loading_mer_dashboard(self.driver)
        auto_renewal_after = self.home_page.get_auto_renewal_status()
        assert auto_renewal_after == 'Off'
    #endregion only have paylater
