from aqa.src.tests.base import BaseTest
from aqa.src.pages.dashboard.add_new_user_page import DashboardAddNewUserPage
from aqa.src.pages.dashboard.home_page import DashboardHomePage
from aqa.src.pages.dashboard.login_page import DashboardLoginPage

from aqa.utils.generic import cook_fixture_eb, cook_fixture_validation_eb

from aqa.utils.enums import account, path
from aqa.utils.webdriver_util import wait_loading_dashboard

onboard_file    = f'{path.fixture_dir}/eb_template.xlsx'
validation_file = f'{path.fixture_dir}/eb_validation_template.xlsx'


class Test(BaseTest):
    def setUp_fixture(self):

        self.login_page         = DashboardLoginPage(self.driver)
        self.home_page          = DashboardHomePage(self.driver)
        self.add_new_user_page  = DashboardAddNewUserPage(self.driver)

    def test_validation(self):
        self.setUp_fixture()

        cook_fixture_validation_eb()

        self.login_page.login_dashboard(account.eb_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_employee_btn()

        self.add_new_user_page.click_on_bulk_onboarding_btn()

        self.add_new_user_page.enroll_by_excel(validation_file)
        wait_loading_dashboard(self.driver)

        errors_msg = self.add_new_user_page.validation_error_msg()
        assert len(errors_msg) == 8
        assert errors_msg[0].text == 'Effective Date may not be null.'
        assert errors_msg[1].text == 'Employee Rank may not be null.'
        assert errors_msg[2].text == 'First Name may not be null.'
        assert errors_msg[3].text == 'RecordID=Unknown not found.'
        assert errors_msg[4].text == 'Start date must be greater than today.'
        assert errors_msg[5].text == 'Missing data for required fields: email.'
        assert errors_msg[6].text == 'Date of Birth may not be null.'
        assert errors_msg[7].text == 'Missing data for required fields: parent_email.'

    def test_individual_onboarding_employee(self):
        self.setUp_fixture()

        self.login_page.login_dashboard(account.eb_owner_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_employee_btn()

        self.add_new_user_page.individual_onboarding_employee()
        wait_loading_dashboard(self.driver)

        assert self.add_new_user_page.add_employee_successful_msg() == 'Onboarding Successful!'

    def test_enroll_new_employee_by_excel(self):
        self.setUp_fixture()

        cook_fixture_eb()

        self.login_page.login_dashboard(account.eb_admin_email, account.default_pwd)
        wait_loading_dashboard(self.driver)

        self.home_page.click_on_add_employee_btn()

        self.add_new_user_page.click_on_bulk_onboarding_btn()

        self.add_new_user_page.enroll_by_excel(onboard_file)
        wait_loading_dashboard(self.driver)

        self.add_new_user_page.click_next_btn()
        wait_loading_dashboard(self.driver)

        assert self.add_new_user_page.add_employee_successful_msg() == 'Onboarding Successful!'
