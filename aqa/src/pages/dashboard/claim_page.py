from random import choice

from selenium.webdriver.common.by import By

from aqa.utils.generic import generate_nricfin
from aqa.utils.webdriver_util import wait_element, findElements_xpath, elementIsDisplayed
from aqa.utils.enums import path

class ParcelClaimPage():

    def __init__(self, driver):
        self.driver                            = driver
        self.proof_non_delivery_input          = '//input[@id="proof_non_delivery"]'
        self.police_report_input               = '//input[@id="police_report"]'
        self.claim_form_input                  = '//input[@id="claim_form"]'
        self.supporting_document_input         = '//input[@id="supporting_document"]'
        self.claim_details                     = By.XPATH, '//*[text()="Claim Detail"]'
        self.claim_proof_non_delivery_picture  = By.XPATH, '//*[text()="Proof of Non-Delivery"]/../following-sibling::div//span[@class="image-title"]'
        self.claim_police_report_picture       = By.XPATH, '//*[text()="Police Report"]/../following-sibling::div//span[@class="image-title"]'
        self.claim_form_picture                = By.XPATH, '//*[text()="Claim Form"]/../following-sibling::div//span[@class="image-title"]'
        self.claim_supporting_document_picture = By.XPATH, '//*[text()="Supporting Documents"]/../following-sibling::div//span[@class="image-title"]'
        self.tracking_number                   = By.XPATH, '//*[text()="Tracking Number"]/following-sibling::div[1]'
        self.item_description                  = By.XPATH, '//*[text()="Item Description"]/following-sibling::div[1]'
        self.submit_btn                        = By.XPATH, '//*[text()="SUBMIT"]'
        self.success_msg                       = By.XPATH, '//*[@class="parcel-submit-claim"]//*[@class="subtitle"]'
        self.back_to_home_btn                  = By.XPATH, '//*[text()="BACK TO HOME"]'
        self.claim_tracking_number             = By.XPATH, '//*[text()="Tracking Number"]/following-sibling::span'
        self.claim_item_description            = By.XPATH, '//*[text()="Item Description"]/following-sibling::span'
        self.parcel_search_input               = By.XPATH, '//*[@class="searchInput"]'
        self.parcel_suggestion_text            = By.XPATH, '//*[@class="suggestionText"]'
        self.parcel_item_name                  = By.XPATH, '//*[text()="Item Name"]/following-sibling::div[1]'

    def data_autofill(self):
        autofill_data = {}
        autofill_data['tracking_number']  = wait_element(self.driver,self.tracking_number).text
        autofill_data['item_description'] = wait_element(self.driver,self.item_description).text
        return autofill_data

    def filled_claim_detail(self):
        proof_non_delivery = findElements_xpath(self.driver, self.proof_non_delivery_input)
        proof_non_delivery[0].send_keys(f'{path.fixture_dir}/1.jpg')

        police_report = findElements_xpath(self.driver, self.police_report_input)
        police_report[0].send_keys(f'{path.fixture_dir}/2.jpg')

        claim_form = findElements_xpath(self.driver, self.claim_form_input)
        claim_form[0].send_keys(f'{path.fixture_dir}/3.jpg')

        supporting_document = findElements_xpath(self.driver, self.supporting_document_input)
        supporting_document[0].send_keys(f'{path.fixture_dir}/4.jpg')

        wait_element(self.driver,self.submit_btn).click()

    def claim_success_msg(self):
        return wait_element(self.driver,self.success_msg).text

    def click_back_to_home_btn(self):
        wait_element(self.driver,self.back_to_home_btn).click()

    def past_claim_detail(self):
        past_claim_detail = {}
        past_claim_detail['isDisplayed_claim_details']                      = elementIsDisplayed(self.driver, self.claim_details)
        past_claim_detail['isDisplayed_claim_proof_non_delivery_picture']   = elementIsDisplayed(self.driver, self.claim_proof_non_delivery_picture)
        past_claim_detail['isDisplayed_claim_police_report_picture']        = elementIsDisplayed(self.driver, self.claim_police_report_picture)
        past_claim_detail['isDisplayed_claim_form_picture']                 = elementIsDisplayed(self.driver, self.claim_form_picture)
        past_claim_detail['isDisplayed_claim_supporting_document_picture']  = elementIsDisplayed(self.driver, self.claim_supporting_document_picture)
        past_claim_detail['claim_tracking_number']                          = wait_element(self.driver,self.claim_tracking_number).text
        past_claim_detail['claim_item_description']                         = wait_element(self.driver,self.claim_item_description).text
        return past_claim_detail

    def search_for_submit_claim(self):
        wait_element(self.driver,self.parcel_search_input).send_keys('Valid-00001')
        wait_element(self.driver,self.parcel_suggestion_text).click()

    def claim_autofill_data(self):
        claim_autofill_data = {}
        claim_autofill_data['parcel_item_name']  = wait_element(self.driver,self.parcel_item_name).text
        claim_autofill_data['item_description']  = wait_element(self.driver,self.item_description).text
        return claim_autofill_data


class MerClaimPage():

    def __init__(self, driver):
        self.driver                            = driver
        self.new_claim_btn                     = By.XPATH, '//button[text()="+ New Claim"]'
        self.yes_btn                           = By.XPATH, '//button[text()="YES"]'
        self.no_btn                            = By.XPATH, '//button[text()="NO"]'
        self.ok_btn                            = By.XPATH, '//*[text()="OK"]'
        self.vehicle_reg                       = By.NAME, 'vehicle_reg'

        self.rental_company                    = By.ID, 'rental_company'
        self.policy_holder                     = By.ID, 'policy_holder'
        self.section1excess                    = By.ID, 'section1excess'
        self.section2excess                    = By.ID, 'section2excess'
        self.paynow_nricfin                    = By.ID, 'paynow_nricfin'
        self.paynow_nickname                   = By.ID, 'paynow_nickname'

        self.date_of_accident                  = By.XPATH, '//*[text()="Date of Accident"]/following-sibling::div'

        self.id_front                          = '//input[@id="id_front"]'
        self.id_back                           = '//input[@id="id_back"]'
        self.drivers_license_front             = '//input[@id="drivers_license_front"]'
        self.drivers_license_back              = '//input[@id="drivers_license_back"]'
        self.certificate_of_motor_insurance    = '//input[@id="certificate_of_motor_insurance"]'
        self.police_report                     = '//input[@id="police_report"]'

        self.rental_contract                   = '//input[@id="rental_contract"]'
        self.gia_report                        = '//input[@id="gia_report"]'
        self.proof_of_excess_payable_or_paid   = '//input[@id="proof_of_excess_payable_or_paid"]'
        self.original_repair_invoice           = '//input[@id="original_repair_invoice"]'
        self.photos_of_vehicle_before_repair   = '//input[@id="photos_of_vehicle_before_repair"]'
        self.photos_of_vehicle_after_repair    = '//input[@id="photos_of_vehicle_after_repair"]'
        self.discharge_voucher                 = '//input[@id="discharge_voucher"]'
        self.proof_of_excess_paid              = '//input[@id="proof_of_excess_paid"]'
        self.paynow_profile_screenshot         = '//input[@id="paynow_profile_screenshot"]'

        self.have_paid                         = By.XPATH, '//*[contains(text(), "I/We have paid")]/../div[1]'
        self.have_read                         = By.XPATH, '//*[contains(text(), "I have read")]/../div[1]'
        self.we_declare                        = By.XPATH, '//*[contains(text(), "I/We declare")]/../div[1]'
        self.submit_btn                        = By.XPATH, '//*[text()="SUBMIT"]'

        self.claim_success_img                 = By.XPATH, '//*[(@alt="thankyouImage")]'

    def click_on_new_claim_btn(self):
        wait_element(self.driver, self.new_claim_btn).click()

    def choose_claim_with_documents(self):
        wait_element(self.driver, self.yes_btn).click()

    def choose_claim_with_no_documents(self):
        wait_element(self.driver, self.no_btn).click()

    def choose_vehicle_reg(self, vehicle_reg):
        wait_element(self.driver, self.vehicle_reg).send_keys(vehicle_reg)
        wait_element(self.driver, (By.XPATH, f'//*[text()="{vehicle_reg}"]/..')).click()

    def input_claim_details(self):
        wait_element(self.driver, self.rental_company).send_keys('Gigacover')
        wait_element(self.driver, self.policy_holder).send_keys('Policy Holder')
        wait_element(self.driver, self.date_of_accident).click()
        wait_element(self.driver, self.ok_btn).click()

        wait_element(self.driver, self.section1excess).send_keys('1000')
        wait_element(self.driver, self.section2excess).send_keys('2000')


    def input_disbursement_detail(self):
        nric = generate_nricfin()
        wait_element(self.driver,self.paynow_nricfin).send_keys(nric)
        wait_element(self.driver,self.paynow_nickname).send_keys('paynow nickname')

        paynow_profile_screenshot = findElements_xpath(self.driver, self.paynow_profile_screenshot)
        paynow_profile_screenshot[0].send_keys(f'{path.fixture_dir}/1.jpg')

    def upload_required_documents(self):
        id_front = findElements_xpath(self.driver, self.id_front)
        id_front[0].send_keys(f'{path.fixture_dir}/1.jpg')

        id_back = findElements_xpath(self.driver, self.id_back)
        id_back[0].send_keys(f'{path.fixture_dir}/2.jpg')

        drivers_license_front = findElements_xpath(self.driver, self.drivers_license_front)
        drivers_license_front[0].send_keys(f'{path.fixture_dir}/3.jpg')

        drivers_license_back = findElements_xpath(self.driver, self.drivers_license_back)
        drivers_license_back[0].send_keys(f'{path.fixture_dir}/4.jpg')

        certificate_of_motor_insurance = findElements_xpath(self.driver, self.certificate_of_motor_insurance)
        certificate_of_motor_insurance[0].send_keys(f'{path.fixture_dir}/5.jpg')

        rental_contract = findElements_xpath(self.driver, self.rental_contract)
        rental_contract[0].send_keys(f'{path.fixture_dir}/6.jpg')

        gia_report = findElements_xpath(self.driver, self.gia_report)
        gia_report[0].send_keys(f'{path.fixture_dir}/7.jpg')

        police_report = findElements_xpath(self.driver, self.police_report)
        police_report[0].send_keys(f'{path.fixture_dir}/8.jpg')

        proof_of_excess_payable_or_paid = findElements_xpath(self.driver, self.proof_of_excess_payable_or_paid)
        proof_of_excess_payable_or_paid[0].send_keys(f'{path.fixture_dir}/1.jpg')

        original_repair_invoice = findElements_xpath(self.driver, self.original_repair_invoice)
        original_repair_invoice[0].send_keys(f'{path.fixture_dir}/2.jpg')

        photos_of_vehicle_before_repair = findElements_xpath(self.driver, self.photos_of_vehicle_before_repair)
        photos_of_vehicle_before_repair[0].send_keys(f'{path.fixture_dir}/3.jpg')

        photos_of_vehicle_after_repair = findElements_xpath(self.driver, self.photos_of_vehicle_after_repair)
        photos_of_vehicle_after_repair[0].send_keys(f'{path.fixture_dir}/4.jpg')

        discharge_voucher = findElements_xpath(self.driver, self.discharge_voucher)
        discharge_voucher[0].send_keys(f'{path.fixture_dir}/5.jpg')

        proof_of_excess_paid = findElements_xpath(self.driver, self.proof_of_excess_paid)
        proof_of_excess_paid[0].send_keys(f'{path.fixture_dir}/6.jpg')

    def click_all_checkbox(self):
        wait_element(self.driver,self.we_declare).click()
        wait_element(self.driver,self.have_paid).click()
        wait_element(self.driver,self.have_read).click()

    def click_submit_btn(self):
        wait_element(self.driver,self.submit_btn).click()

    def is_claim_successful(self):
        return elementIsDisplayed(self.driver, self.claim_success_img)


class EssentialsActivityPage():

    def __init__(self, driver):
        self.driver                                       = driver
        self.add_activity_btn                             = By.XPATH, '//*[text()="Add Activity"]/..'
        self.add_btn                                      = By.XPATH, '//button[text()="Add"]'
        self.name_input                                   = By.XPATH, '//*[@id="combo-box-demo-name"]'
        self.nricfin_input                                = By.XPATH, '//*[@id="combo-box-demo-nricfin"]'
        self.date_visited                                 = By.XPATH, '//*[@id="date-picker-dialog"]'
        self.clinic_type                                  = By.XPATH, '//*[@id="combo-box-demo-clinic-type"]'
        self.clinic_name                                  = By.XPATH, '//*[@id="combo-box-demo-clinics-name"]'
        self.mc_day_input                                 = By.XPATH, '(//*[@class="MuiInputBase-input MuiOutlinedInput-input"])[2]'
        self.company_spend_input                          = By.XPATH, '(//*[@class="MuiInputBase-input MuiOutlinedInput-input"])[3]'
        self.employee_spend_input                         = By.XPATH, '(//*[@class="MuiInputBase-input MuiOutlinedInput-input"])[4]'
        self.okBtn                                        = By.XPATH, '//*[text()="OK"]'

        self.record_visit_success_msg                     = By.XPATH, '//*[@id="overview-success"]//p'

    def add_activity(self, name):
        wait_element(self.driver, self.add_activity_btn).click()
        wait_element(self.driver, self.name_input).send_keys(name)
        wait_element(self.driver, (By.XPATH, f'//li[text()="{name}"]')).click()

        wait_element(self.driver, self.date_visited).click()
        wait_element(self.driver, self.okBtn).click()

        clinic_type = choice(['GP', 'TCM', 'Dental'])
        wait_element(self.driver, self.clinic_type).click()
        wait_element(self.driver, (By.XPATH, f'//li[text()="{clinic_type}"]')).click()

        wait_element(self.driver, self.clinic_name).send_keys('Test clinic')
        wait_element(self.driver, self.mc_day_input).send_keys(5)
        wait_element(self.driver, self.company_spend_input).send_keys(10)
        wait_element(self.driver, self.employee_spend_input).send_keys(5)

        wait_element(self.driver, self.add_btn).click()

    def get_record_visit_success_msg(self):
        return wait_element(self.driver, self.record_visit_success_msg).text

