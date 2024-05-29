from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element


class MerVehicleDetailsPage():

    def __init__(self, driver):
        self.driver                    = driver
        self.actual_vehicle_reg        = By.XPATH, '//*[contains(@class,"text-main-green")]'
        self.actual_vehicle_type       = By.XPATH, '//*[contains(@class,"bg-indigo-50")][3]'
        self.actual_contact_email      = By.XPATH, '//*[text()="Contact Email"]/following-sibling::div'
        self.actual_contact_number     = By.XPATH, '//*[text()="Contact Number"]/following-sibling::div'
        self.actual_company_uen        = By.XPATH, '//*[text()="Company UEN"]/following-sibling::div'
        self.actual_company_name       = By.XPATH, '//*[text()="Company Name"]/following-sibling::div'
        self.actual_ss1                = By.XPATH, '//*[text()="Section 1 Excess"]/following-sibling::div'
        self.actual_ss2                = By.XPATH, '//*[text()="Section 2 Excess"]/following-sibling::div'
        self.actual_reduced_excess     = By.XPATH, '//*[text()="Reduced Excess To"]/following-sibling::div'
        self.actual_combined_excess    = By.XPATH, '//*[text()="Combined Excess"]/following-sibling::div'
        self.actual_start_date         = By.XPATH, '//*[text()="Contract Start Date"]/following-sibling::div'
        self.actual_chassis_no         = By.XPATH, '//*[text()="Vehicle Chassis No. "]/following-sibling::div'
        self.actual_upcoming_status    = By.XPATH, '//*[text()="Upcoming Status"]/following-sibling::div'
        self.actual_auto_renewal       = By.XPATH, '//*[text()="Auto-Renewal"]/following-sibling::div'


    def get_vehicle_info(self):
        data                           = {}
        data['actual_vehicle_reg']     = wait_element(self.driver, self.actual_vehicle_reg).text
        data['actual_vehicle_type']    = wait_element(self.driver, self.actual_vehicle_type).text
        data['actual_contact_email']   = wait_element(self.driver, self.actual_contact_email).text
        data['actual_contact_number']  = wait_element(self.driver, self.actual_contact_number).text
        data['actual_company_uen']     = wait_element(self.driver, self.actual_company_uen).text
        data['actual_company_name']    = wait_element(self.driver, self.actual_company_name).text
        data['actual_ss1']             = wait_element(self.driver, self.actual_ss1).text
        data['actual_ss2']             = wait_element(self.driver, self.actual_ss2).text
        data['actual_reduced_excess']  = wait_element(self.driver, self.actual_reduced_excess).text
        data['actual_combined_excess'] = wait_element(self.driver, self.actual_combined_excess).text
        data['actual_start_date']      = wait_element(self.driver, self.actual_start_date).text
        data['actual_chassis_no']      = wait_element(self.driver, self.actual_chassis_no).text
        data['actual_upcoming_status'] = wait_element(self.driver, self.actual_upcoming_status).text
        data['actual_auto_renewal']    = wait_element(self.driver, self.actual_auto_renewal).text
        return data
