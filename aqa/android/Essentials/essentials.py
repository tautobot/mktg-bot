import unittest

from testcases.lib.generic import read_cell_in_excel_file
from aQA.venta.util import *
from aQA.webdriver.selenium_webdriver import *
from config_local import *

def setUpModule():    pass  # nothing here for now
def tearDownModule(): pass  # nothing here for now

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))
excel_file = f'{app_path}/fixtures/benefits_template_no_nricfin.xlsx'

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver_local() if dri == 'local' else webdriver_docker()
        login_dashboard(self.driver)
        wait()

    def tearDown(self): self.driver.quit()

    def test_01_total_users(self):
        wait()
        users = self.driver.find_elements_by_xpath('(//*[contains(@class,"rt-tbody")])[1]/div[contains(@class,"rt-tr-group")]')
        assert len(users) == 5

        pages = wait_xpath(self.driver, '//*[contains(@class,"-totalPages")]').text
        assert pages == '1'

    def test_user1(self):
        full_name = read_cell_in_excel_file(excel_file, 'D2')

        wait_xpath(self.driver, "//*[(@placeholder='Search by Name')]").send_keys(full_name)

        #region user information
        wait()
        name = wait_xpath(self.driver, "(//*[contains(@class,'rt-td')])[2]").text
        assert name == full_name

        employee_no = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[3]").text
        assert employee_no == read_cell_in_excel_file(excel_file, 'H2')

        email = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[2]").text
        assert email == read_cell_in_excel_file(excel_file, 'F2')

        plan_type = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[7]").text
        assert plan_type == read_cell_in_excel_file(excel_file, 'C2')

        start_date = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[4]").text
        assert start_date == read_cell_in_excel_file(excel_file, 'N2').strftime('%d %b %Y')
        #endregion

        #region GP
        GP_Company_subsidy = wait_xpath(self.driver, '(//*[contains(@class,"selected")])[2]').text
        assert GP_Company_subsidy == 'Full Subsidy'

        GP_medical_subsidy_cap = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'gp-tab')]//*[contains(@class,'static-value')])[1]").text
        assert GP_medical_subsidy_cap == '____'

        GP_medical_subsidy_cap_year = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'gp-tab')]//*[contains(@class,'static-value')])[2]").text
        assert GP_medical_subsidy_cap_year == 'S$200.00'
        #endregion

        #region Dental
        dental = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")])[1]')
        dental.click()

        dental_subsidy_cap = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")]//p)[1]').text
        assert dental_subsidy_cap == 'S$10.00'

        dental_subsidy_year = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")]//p)[2]').text
        assert dental_subsidy_year == 'S$100.00'
        #endregion

        #region TCM
        TCM = wait_xpath(self.driver, '(//*[contains(@id,"tcm-tab")])[1]')
        TCM.click()

        tcm_subsidy_cap = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'tmc-tab')]//*[contains(@class,'static-value')])[1]").text
        assert tcm_subsidy_cap == 'S$10.00'

        tcm_subsidy_year = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'tmc-tab')]//*[contains(@class,'static-value')])[2]").text
        assert tcm_subsidy_year == 'S$100.00'
        #endregion


    def test_user2(self):
        full_name = read_cell_in_excel_file(excel_file, 'D3')

        wait_xpath(self.driver, "//*[(@placeholder='Search by Name')]").send_keys(full_name)

        #region user information
        wait()
        name = wait_xpath(self.driver, "(//*[contains(@class,'rt-td')])[2]").text
        assert name == full_name

        employee_no = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[3]").text
        assert employee_no == read_cell_in_excel_file(excel_file, 'H3')

        email = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[2]").text
        assert email == read_cell_in_excel_file(excel_file, 'F3')

        plan_type = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[7]").text
        assert plan_type == read_cell_in_excel_file(excel_file, 'C3')

        start_date = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[4]").text
        assert start_date == read_cell_in_excel_file(excel_file, 'N3').strftime('%d %b %Y')
        #endregion

        #region GP
        GP_Company_subsidy = wait_xpath(self.driver, '(//*[contains(@class,"selected")])[2]').text
        assert GP_Company_subsidy == 'NIL'

        GP_medical_subsidy_cap = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'gp-tab')]//*[contains(@class,'static-value')])[1]").text
        assert GP_medical_subsidy_cap == 'S$20.00'

        GP_medical_subsidy_cap_year = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'gp-tab')]//*[contains(@class,'static-value')])[2]").text
        assert GP_medical_subsidy_cap_year == 'S$200.00'
        #endregion

        #region Dental
        dental = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")])[1]')
        dental.click()

        dental_subsidy_cap = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")]//p)[1]').text
        assert dental_subsidy_cap == 'S$20.00'

        dental_subsidy_year = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")]//p)[2]').text
        assert dental_subsidy_year == 'S$100.00'
        #endregion

        #region TCM
        TCM = wait_xpath(self.driver, '(//*[contains(@id,"tcm-tab")])[1]')
        TCM.click()

        tcm_subsidy_cap = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'tmc-tab')]//*[contains(@class,'static-value')])[1]").text
        assert tcm_subsidy_cap == 'S$0'

        tcm_subsidy_year = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'tmc-tab')]//*[contains(@class,'static-value')])[2]").text
        assert tcm_subsidy_year == 'S$100.00'
        #endregion

    def test_user3(self):
        full_name = read_cell_in_excel_file(excel_file, 'D4')

        wait_xpath(self.driver, "//*[(@placeholder='Search by Name')]").send_keys(full_name)

        #region user information
        wait()
        name = wait_xpath(self.driver, "(//*[contains(@class,'rt-td')])[2]").text
        assert name == full_name

        employee_no = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[3]").text
        assert employee_no == read_cell_in_excel_file(excel_file, 'H4')

        email = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[2]").text
        assert email == read_cell_in_excel_file(excel_file, 'F4')

        plan_type = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[7]").text
        assert plan_type == read_cell_in_excel_file(excel_file, 'C4')

        start_date = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[4]").text
        assert start_date == read_cell_in_excel_file(excel_file, 'N4').strftime('%d %b %Y')
        #endregion

        #region GP
        GP_Company_subsidy = wait_xpath(self.driver, '(//*[contains(@class,"selected")])[2]').text
        assert GP_Company_subsidy == 'Cover Consult Only'

        GP_medical_subsidy_cap = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'gp-tab')]//*[contains(@class,'static-value')])[1]").text
        assert GP_medical_subsidy_cap == 'S$30.00'

        GP_medical_subsidy_cap_year = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'gp-tab')]//*[contains(@class,'static-value')])[2]").text
        assert GP_medical_subsidy_cap_year == 'S$200.00'
        # endregion

        #region Dental
        dental = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")])[1]')
        dental.click()

        dental_subsidy_cap = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")]//p)[1]').text
        assert dental_subsidy_cap == 'S$30.00'

        dental_subsidy_year = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")]//p)[2]').text
        assert dental_subsidy_year == 'S$100.00'
        #endregion

        #region TCM
        TCM = wait_xpath(self.driver, '(//*[contains(@id,"tcm-tab")])[1]')
        TCM.click()

        tcm_subsidy_cap = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'tmc-tab')]//*[contains(@class,'static-value')])[1]").text
        assert tcm_subsidy_cap == 'S$30.00'

        tcm_subsidy_year = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'tmc-tab')]//*[contains(@class,'static-value')])[2]").text
        assert tcm_subsidy_year == 'S$100.00'
        #endregion

    def test_user4(self):
        full_name = read_cell_in_excel_file(excel_file, 'D5')

        wait_xpath(self.driver, "//*[(@placeholder='Search by Name')]").send_keys(full_name)

        #region user information
        wait()
        name = wait_xpath(self.driver, "(//*[contains(@class,'rt-td')])[2]").text
        assert name == full_name

        employee_no = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[3]").text
        assert employee_no == read_cell_in_excel_file(excel_file, 'H5')

        email = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[2]").text
        assert email == read_cell_in_excel_file(excel_file, 'F5')

        plan_type = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[7]").text
        assert plan_type == read_cell_in_excel_file(excel_file, 'C5')

        start_date = wait_xpath(self.driver, "((//*[(@class='first-table')]//*[(@class='rt-tr-group')])[1]//*[contains(@class,'rt-td')])[4]").text
        assert start_date == read_cell_in_excel_file(excel_file, 'N5').strftime('%d %b %Y')
        #endregion

        #region GP
        GP_Company_subsidy = wait_xpath(self.driver, '(//*[contains(@class,"selected")])[2]').text
        assert GP_Company_subsidy == 'Cover Non-Consult Only'

        GP_medical_subsidy_cap = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'gp-tab')]//*[contains(@class,'static-value')])[1]").text
        assert GP_medical_subsidy_cap == '____'

        GP_medical_subsidy_cap_year = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'gp-tab')]//*[contains(@class,'static-value')])[2]").text
        assert GP_medical_subsidy_cap_year == 'S$200.00'
        # endregion

        #region Dental
        dental = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")])[1]')
        dental.click()

        dental_subsidy_cap = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")]//p)[1]').text
        assert dental_subsidy_cap == 'S$40.00'

        dental_subsidy_year = wait_xpath(self.driver, '(//*[contains(@id,"dental-tab")]//p)[2]').text
        assert dental_subsidy_year == 'S$100.00'
        #endregion

        #region TCM
        TCM = wait_xpath(self.driver, '(//*[contains(@id,"tcm-tab")])[1]')
        TCM.click()

        tcm_subsidy_cap = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'tmc-tab')]//*[contains(@class,'static-value')])[1]").text
        assert tcm_subsidy_cap == 'S$0'

        tcm_subsidy_year = wait_xpath(self.driver, "(//*[contains(@aria-labelledby,'tmc-tab')]//*[contains(@class,'static-value')])[2]").text
        assert tcm_subsidy_year == 'S$100.00'
        #endregion
