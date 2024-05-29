from random import choice

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element, elementIsDisplayed, findElements_xpath

class DashboardHomePage():

    def __init__(self, driver):
        self.driver                             = driver
        self.upload_file_input                  = '//input[@type="file"]'
        self.errors_msg                         = '//*[@class="error"]'
        self.total_user_record                  = '(//*[contains(@class,"rt-tbody")])[1]/div[contains(@class,"rt-tr-group")]'
        self.menu_user                          = By.XPATH, '//*[text()="User"]'
        self.add_new_insured_btn                = By.XPATH, '//*[text()="Add New Insured"]'
        self.add_employee_btn                   = By.XPATH, '//button[text()="+ Add Employee"]'
        self.parcel_upload_details_btn          = By.XPATH, '//*[text()="Upload Parcel Details"]'
        self.done_btn                           = By.XPATH, '//*[text()="DONE"]'
        self.total_parcel_declared              = By.XPATH, '//*[text()="Total Parcels Declared: "]/span'
        self.parcel_file_claim_btn              = By.XPATH, '//*[text()="test onboard parcel 1"]/..//span[text()="File Claim"]'
        self.parcel_claim_tab_btn               = By.XPATH, '//*[text()="Claims"]'
        self.parcel_view_claim_details_btn      = By.XPATH, '//*[text()="View Claim"]'
        self.parcel_submit_new_claim_btn        = By.XPATH, '//*[text()="Submit New Claim"]'

        #Essentials                                     
        self.total_page                         = By.XPATH, '//*[contains(@class,"-totalPages")]'
        self.search_box                         = By.XPATH, '//*[(@placeholder="Search by Name")]'
        self.user_name                          = By.XPATH, '(//*[contains(@class,"rt-td")])[2]'
        self.employee_no                        = By.XPATH, '((//*[(@class="first-table")]//*[(@class="rt-tr-group")])[1]//*[contains(@class,"rt-td")])[3]'
        self.email                              = By.XPATH, '((//*[(@class="first-table")]//*[(@class="rt-tr-group")])[1]//*[contains(@class,"rt-td")])[2]'
        self.plan_type                          = By.XPATH, '((//*[(@class="first-table")]//*[(@class="rt-tr-group")])[1]//*[contains(@class,"rt-td")])[7]'
        self.start_date                         = By.XPATH, '((//*[(@class="first-table")]//*[(@class="rt-tr-group")])[1]//*[contains(@class,"rt-td")])[4]'
        self.gp_company_subsidy                 = By.XPATH, '(//*[contains(@class,"selected")])[2]'
        self.gp_medical_subsidy_cap             = By.XPATH, '(//*[contains(@aria-labelledby,"gp-tab")]//*[contains(@class,"static-value")])[1]'
        self.gp_medical_subsidy_cap_year        = By.XPATH, '(//*[contains(@aria-labelledby,"gp-tab")]//*[contains(@class,"static-value")])[2]'
        self.dental                             = By.XPATH, '(//*[contains(@id,"dental-tab")])[1]'
        self.dental_subsidy_cap                 = By.XPATH, '(//*[contains(@id,"dental-tab")]//p)[1]'
        self.dental_subsidy_year                = By.XPATH, '(//*[contains(@id,"dental-tab")]//p)[2]'
        self.tcm                                = By.XPATH, '(//*[contains(@id,"tcm-tab")])[1]'
        self.tcm_subsidy_cap                    = By.XPATH, '(//*[contains(@aria-labelledby,"tmc-tab")]//*[contains(@class,"static-value")])[1]'
        self.tcm_subsidy_year                   = By.XPATH, '(//*[contains(@aria-labelledby,"tmc-tab")]//*[contains(@class,"static-value")])[2]'
        self.enrol_employees_btn                = By.XPATH, '//*[text()="Enrol employees"]/../a'
        self.next_btn                           = By.XPATH, '//*[text()="Next"]'
        self.activity_tab                       = By.XPATH, '//*[text()="Activity"]/..'

    def essentials_click_on_enrol_employee(self):
        wait_element(self.driver,self.enrol_employees_btn).click()
        wait_element(self.driver,self.next_btn).click()

    def essentials_click_on_activity_tab(self):
        wait_element(self.driver,self.activity_tab).click()

    def click_on_add_employee_btn(self):
        wait_element(self.driver,self.add_employee_btn).click()

    def user_existed_on_home_page(self, expected_email):
        return elementIsDisplayed(self.driver,(By.XPATH, f'//*[text()="{expected_email.lower()}"]'))

    def parcel_upload_details(self):
        wait_element(self.driver,self.parcel_upload_details_btn).click()

    def parcel_upload_file(self, file):
        findElements_xpath(self.driver, self.upload_file_input)[0].send_keys(file)
        wait_element(self.driver,self.done_btn).click()

    def error_msg(self):
        errors_msg = findElements_xpath(self.driver, self.errors_msg)
        return errors_msg

    def data_uploaded(self):
        result = {}
        result['total_parcel_declared'] = wait_element(self.driver,self.total_parcel_declared).text
        result['isDisplayed_parcel1']   = elementIsDisplayed(self.driver, '//*[text()="test onboard parcel 1"]')
        result['isDisplayed_parcel2']   = elementIsDisplayed(self.driver, '//*[text()="test onboard parcel 2"]')
        result['isDisplayed_parcel3']   = elementIsDisplayed(self.driver, '//*[text()="test onboard parcel 3"]')
        result['isDisplayed_parcel4']   = elementIsDisplayed(self.driver, '//*[text()="test onboard parcel 4"]')
        return result

    def parcel_click_file_claim_btn(self):
        wait_element(self.driver,self.parcel_file_claim_btn).click()

    def parcel_claim_tab(self):
        wait_element(self.driver,self.parcel_claim_tab_btn).click()

    def parcel_submit_new_claim(self):
        wait_element(self.driver,self.parcel_submit_new_claim_btn).click()

    def parcel_view_claim_detail(self):
        wait_element(self.driver,self.parcel_view_claim_details_btn).click()

    def essentials_total_user_record(self):
        return findElements_xpath(self.driver, self.total_user_record)

    def essentials_total_page(self):
        return wait_element(self.driver,self.total_page).text

    def essentials_search_by_name(self, name):
        wait_element(self.driver,self.search_box).send_keys(name)

    def essentials_user_info(self):
        data = {}
        data['name']                        = wait_element(self.driver,self.user_name).text
        data['employee_no']                 = wait_element(self.driver,self.employee_no).text
        data['email']                       = wait_element(self.driver,self.email).text
        data['plan_type']                   = wait_element(self.driver,self.plan_type).text
        data['start_date']                  = wait_element(self.driver,self.start_date).text
        data['gp_company_subsidy']          = wait_element(self.driver,self.gp_company_subsidy).text
        data['gp_medical_subsidy_cap']      = wait_element(self.driver,self.gp_medical_subsidy_cap).text
        data['gp_medical_subsidy_cap_year'] = wait_element(self.driver,self.gp_medical_subsidy_cap_year).text

        wait_element(self.driver,self.dental).click()

        data['dental_subsidy_cap']          = wait_element(self.driver,self.dental_subsidy_cap).text
        data['dental_subsidy_year']         = wait_element(self.driver,self.dental_subsidy_year).text

        wait_element(self.driver,self.tcm).click()

        data['tcm_subsidy_cap']             = wait_element(self.driver,self.tcm_subsidy_cap).text
        data['tcm_subsidy_year']            = wait_element(self.driver,self.tcm_subsidy_year).text
        return data

class MerDashboardHomePage():

    def __init__(self, driver):
        self.driver                             = driver
        self.upload_file_input                  = '//input[@type="file"]'
        self.errors_msg                         = '//*[@class="error"]'
        self.review_data                        = '//*[text()="Preview"]/following-sibling::div//div[contains(@class,"text-main-green")]'

        self.next_btn                           = By.XPATH, '//*[text()="Next"]'
        self.edit_btn                           = By.XPATH, '//*[text()=" Edit"]'
        self.edit_reference_number_btn          = By.XPATH, '//*[@alt="edit"]/..'
        self.add_vehicles_btn                   = By.XPATH, '//button[text()="+ Add Vehicles"]'
        self.add_one_vehicle_btn                = By.XPATH, '//*[(text()="Add one vehicle")]/../button'
        self.section_reduced_excess             = By.XPATH,  '//*[text()="Per Excess"]/..//*[@name="reduced_excess"]'
        self.per_excess_option                  = By.XPATH, '//*[(text()="Per Excess")]/../../button'
        self.combined_excess_option             = By.XPATH, '//*[(text()="Combined Excess")]/../../button'
        self.combined_reduced_excess            = By.XPATH, '//*[text()="Combined Excess"]/..//*[@name="reduced_excess"]'
        self.confirm_btn                        = By.XPATH, '//button[text()="Confirm"]'
        self.search_box                         = By.XPATH, '//*[@placeholder="Search this list"]'
        self.auto_renewal_button                = By.XPATH, '//*[contains(@id, "headlessui-switch")]'
        self.actual_upcoming_policy             = By.XPATH, '//*[@class="react-datepicker-wrapper"]'
        self.upcoming_status                    = By.XPATH, '//*[@class="rt-tr-group"][1]//*[@role="gridcell"and position() = (last()-1)]'
        self.current_start_date                 = By.XPATH, '//*[contains(@class,"react-datepicker__day--selected")]'
        self.next_start_date                    = By.XPATH, '//*[contains(@class,"react-datepicker__day--selected")]/../following-sibling::div[1]/div[1]'
        self.next_upcoming_start_date           = By.XPATH, '//*[text()="Are you sure you want to change date to"]//following-sibling::span'
        self.claim_icon                         = By.XPATH, '//*[@href="/dashboard/mer/claim-tracker"]'

        self.vehicle_type                       = By.NAME,  'vehicle_type'
        self.section1excess                     = By.NAME,  'section1excess'
        self.section2excess                     = By.NAME,  'section2excess'
        self.combined_excess_dropdown           = By.NAME,  'combined_excess'
        self.unit_id                            = By.NAME,  'unit_id'

        self.vehicle_reg                        = By.ID,    'vehicle_reg'
        self.company_uen                        = By.ID,    'company_uen'
        self.company_name                       = By.ID,    'company_name'
        self.contact_num                        = By.ID,    'contact_num'
        self.contact_email                      = By.ID,    'contact_email'
        self.model                              = By.ID,    'model'
        self.make                               = By.ID,    'make'
        self.chassis                            = By.ID,    'chassis'
        self.engine                             = By.ID,    'engine'
        self.reference_number_input             = By.ID,    'reference_number'

    def click_on_add_one_vehicle_btn(self):
        wait_element(self.driver, self.add_one_vehicle_btn).click()

    def click_on_add_vehicles_btn(self):
        wait_element(self.driver, self.add_vehicles_btn).click()

    def go_to_claim_page(self):
        wait_element(self.driver, self.claim_icon).click()

    def input_vehicle_info(self, vehicle_reg):
        wait_element(self.driver, self.vehicle_reg).send_keys(vehicle_reg)
        wait_element(self.driver, self.company_uen).send_keys('company uen')
        wait_element(self.driver, self.company_name).send_keys('company name')
        wait_element(self.driver, self.contact_num).send_keys('contact number')
        wait_element(self.driver, self.contact_email).send_keys(f'{vehicle_reg}@gigacover.com')
        wait_element(self.driver, self.model).send_keys('vehicle model')
        wait_element(self.driver, self.make).send_keys('vehicle make')
        wait_element(self.driver, self.chassis).send_keys('chassis no')
        wait_element(self.driver, self.engine).send_keys('engine no')

    def choose_random_vehicle_type(self):
        wait_element(self.driver, self.vehicle_type).click()

        vehicle_type_list = ['Motorcycle', 'Car', 'Van']
        vehicle_type = choice(vehicle_type_list)
        wait_element(self.driver, (By.XPATH, f'//option[text()="{vehicle_type}"]')).click()
        return vehicle_type

    def choose_per_excess_plan(self):
        per_excess_plan_data = {}
        wait_element(self.driver, self.per_excess_option).click()

        wait_element(self.driver, self.section1excess).click()
        ss1_list = [0, 1000, 1400, 1500, 1800, 2000, 2500, 3000, 3500, 4000]
        per_excess_plan_data['ss1'] = choice(ss1_list)
        wait_element(self.driver,(By.XPATH, f'//*[@name="section1excess"]/option[text()="${per_excess_plan_data["ss1"]}"]')).click()

        wait_element(self.driver, self.section2excess).click()
        per_excess_plan_data['ss2']= wait_element(self.driver,(By.XPATH, '//*[@name="section2excess"]/option[2]')).text
        wait_element(self.driver,(By.XPATH, '//*[@name="section2excess"]/option[2]')).click()

        wait_element(self.driver, self.section_reduced_excess).click()
        per_excess_plan_data['reduced_excess'] =  wait_element(self.driver,(By.XPATH, '//*[text()="Per Excess"]/..//*[@name="reduced_excess"]/option[2]')).text
        wait_element(self.driver,(By.XPATH, '//*[text()="Per Excess"]/..//*[@name="reduced_excess"]/option[2]')).click()

        return per_excess_plan_data

    def choose_combined_plan(self):
        combined_plan_data = {}
        wait_element(self.driver, self.combined_excess_option).click()

        wait_element(self.driver, self.combined_excess_dropdown).click()
        combined_list = [1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
        combined_plan_data['combined_excess'] = choice(combined_list)

        wait_element(self.driver,(By.XPATH, f'//*[@name="combined_excess"]/option[text()="${combined_plan_data["combined_excess"]}"]')).click()
        combined_plan_data['reduced_excess'] = wait_element(self.driver,(By.XPATH, '//*[text()="Combined Excess"]/..//*[@name="reduced_excess"]/option[2]')).text

        wait_element(self.driver, self.combined_reduced_excess).click()
        wait_element(self.driver,(By.XPATH, '//*[text()="Combined Excess"]/..//*[@name="reduced_excess"]/option[2]')).click()
        return combined_plan_data

    def get_review_data(self):
        review_data = {}

        review_data_list               = findElements_xpath(self.driver, self.review_data)
        review_data['vehicle_reg']     = review_data_list[0].text
        review_data['company_uen']     = review_data_list[1].text
        review_data['company_name']    = review_data_list[2].text
        review_data['contact_num']     = review_data_list[3].text
        review_data['contact_email']   = review_data_list[4].text
        review_data['model']           = review_data_list[5].text
        review_data['make']            = review_data_list[6].text
        review_data['chassis']         = review_data_list[7].text
        review_data['engine']          = review_data_list[8].text
        review_data['vehicle_type']    = review_data_list[9].text
        review_data['section1excess']  = review_data_list[10].text
        review_data['section2excess']  = review_data_list[11].text
        review_data['combined_excess'] = review_data_list[12].text
        review_data['reduced_excess']  = review_data_list[13].text
        review_data['unit']            = review_data_list[14].text
        review_data['start_date']      = review_data_list[15].text
        return review_data

    def click_on_confirm_btn(self):
        wait_element(self.driver, self.confirm_btn).click()

    def upload_file(self, file):
        findElements_xpath(self.driver, self.upload_file_input)[0].send_keys(file)
        wait_element(self.driver,self.next_btn).click()

    def search_vehicle(self, vehicle_reg):
        wait_element(self.driver, self.search_box).send_keys(vehicle_reg)
        wait_element(self.driver, self.search_box).send_keys(Keys.ENTER)

    def click_on_vehicle_reg(self, vehicle_reg):
        wait_element(self.driver, (By.XPATH, f'//*[text()="{vehicle_reg}"]')).click()

    def get_upcoming_start_date(self):
        return wait_element(self.driver, self.actual_upcoming_policy).text

    def get_upcoming_status(self):
        return wait_element(self.driver, self.upcoming_status).text

    def get_auto_renewal_status(self):
        return wait_element(self.driver, self.auto_renewal_button).text

    def change_upcoming_start_date(self):
        wait_element(self.driver, self.actual_upcoming_policy).click()

        next_start_date = wait_element(self.driver, self.next_start_date)
        next_start_date.click()

        start_date_after_change = wait_element(self.driver, self.next_upcoming_start_date).text
        wait_element(self.driver, self.confirm_btn).click()
        return start_date_after_change

    def turn_off_auto_renewal(self):
        wait_element(self.driver, self.auto_renewal_button).click()
        wait_element(self.driver, self.confirm_btn).click()

    def confirm_paynow_payment(self):
        wait_element(self.driver, self.edit_reference_number_btn).click()
        try:
            wait_element(self.driver, self.reference_number_input).send_keys('ReferenceNumber')
        except: pass
        wait_element(self.driver, self.confirm_btn).click()

    def vehicle_is_displayed(self, vehicle_reg):
        return elementIsDisplayed(self.driver, (By.XPATH, f'//*[text()="{vehicle_reg}"]'))
