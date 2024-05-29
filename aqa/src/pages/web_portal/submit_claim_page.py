from random import choice

from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element, scroll_to_bottom, findElements_xpath, elementIsDisplayed
from aqa.utils.generic import generate_mobile_phl, generate_nricfin
from aqa.utils.enums import path

csv_file = f'{path.fixture_dir}/eb_employee_template.csv'

class EbWebPortalSubmitClaimPage():
    def __init__(self, driver):
        self.driver                         = driver
        self.inpatient_form_input           = '//input[@id="inpatient_form"]'
        self.outpatient_form_input          = '//input[@id="outpatient_form"]'
        self.hospital_statement_input       = '//input[@id="hospital_statement"]'
        self.medical_certificates_input     = '//input[@id="medical_certificate"]'
        self.hospital_medical_bills_input   = '//input[@id="hospital_medical_bill"]'
        self.lab_requests_input             = '//input[@id="lab_requests"]'
        self.date_of_accident               = By.XPATH, '//*[text()="Date of Accident"]/following-sibling::div[1]'
        self.choose_user_dropdown           = By.XPATH, '//*[text()="Please verify your information"]/following-sibling::div'
        self.ok_btn                         = By.XPATH, '//*[text()="OK"]'
        self.choose_payment_method_dropdown = By.XPATH, '//*[text()="Bank/ E-Wallet Name"]/following-sibling::div[1]'
        self.GCash_option                   = By.XPATH, '//li[text()="GCash"]'
        self.checkbox                       = By.XPATH, '//*[contains(@class, "mt-7")]/div[1]'
        self.submit_btn                     = By.XPATH, '//*[text()="SUBMIT"]'
        self.mobile_input                   = By.ID,    'mobile'

        self.claim_success_img              = By.XPATH, '//*[(@alt="thankyouImage")]'


    def choose_date_of_accident(self):
        wait_element(self.driver,self.date_of_accident).click()
        wait_element(self.driver,self.ok_btn).click()

    def input_eb_inpatient_required_document(self):
        inpatient_form = findElements_xpath(self.driver, self.inpatient_form_input)
        inpatient_form[0].send_keys(f'{path.fixture_dir}/1.jpg')

        hospital_statement = findElements_xpath(self.driver, self.hospital_statement_input)
        hospital_statement[0].send_keys(f'{path.fixture_dir}/2.jpg')

        hospital_medical_bills = findElements_xpath(self.driver, self.hospital_medical_bills_input)
        hospital_medical_bills[0].send_keys(f'{path.fixture_dir}/3.jpg')

        lab_requests = findElements_xpath(self.driver, self.lab_requests_input)
        lab_requests[0].send_keys(f'{path.fixture_dir}/4.jpg')

    def input_eb_outpatient_required_document(self):
        outpatient_form = findElements_xpath(self.driver, self.outpatient_form_input)
        outpatient_form[0].send_keys(f'{path.fixture_dir}/1.jpg')

        medical_certificates = findElements_xpath(self.driver, self.medical_certificates_input)
        medical_certificates[0].send_keys(f'{path.fixture_dir}/2.jpg')

        hospital_medical_bills = findElements_xpath(self.driver, self.hospital_medical_bills_input)
        hospital_medical_bills[0].send_keys(f'{path.fixture_dir}/3.jpg')

        lab_requests = findElements_xpath(self.driver, self.lab_requests_input)
        lab_requests[0].send_keys(f'{path.fixture_dir}/4.jpg')

    def input_disbursement_details(self):
        scroll_to_bottom(self.driver)

        wait_element(self.driver,self.choose_payment_method_dropdown).click()
        wait_element(self.driver,self.GCash_option).click()

        mobile = generate_mobile_phl()
        wait_element(self.driver,self.mobile_input).send_keys(mobile)

        wait_element(self.driver,self.checkbox).click()

    def click_submit_btn(self):
        wait_element(self.driver,self.submit_btn).click()

    def is_claim_successful(self):
        return elementIsDisplayed(self.driver, self.claim_success_img)


class PhlInsuranceWebPortalSubmitClaimPage():
    def __init__(self, driver):
        self.driver                            = driver
        #insurance (flep/pa)
        self.date_injury                       = By.XPATH, '//*[text()="Date of Accident"]/following-sibling::div[1]'
        self.date_accident                     = By.XPATH, '//*[text()="Date & Time of Accident"]/following-sibling::div[1]'
        self.date_incident                     = By.XPATH, '//*[text()="Incident date"]/following-sibling::div[1]'
        self.ok_btn                            = By.XPATH, '//*[text()="OK"]'
        self.description_injury                = By.ID, 'description'
        self.what_doing_accident               = By.ID, 'what_doing_accident'
        self.how_did_the_accident_happen       = By.ID, 'how_did_the_accident_happen'

        #termlife
        self.due_to_other_causes               = By.XPATH, '//*[text()="What is the cause of death?"]/following-sibling::div//div[text()="Death from other causes"]'

        #disbursement_details
        self.choose_payment_method_dropdown    = By.XPATH, '//*[text()="Bank/ E-Wallet Name"]/following-sibling::div[1]'
        self.GCash_option                      = By.XPATH, '//li[text()="GCash"]'
        self.checkbox                          = By.XPATH, '//*[contains(@class, "mt-7")]/div[1]'
        self.submit_btn                        = By.XPATH, '//*[text()="SUBMIT"]'
        self.mobile_input                      = By.ID, 'mobile'

        #insurance required document (flep/pa)
        self.id_front                          = '//input[@id="id_front"]'
        self.id_back                           = '//input[@id="id_back"]'
        self.apf_form                          = '//input[@id="apf_form"]'
        self.medical_certificate               = '//input[@id="medical_certificate"]'
        self.hospital_medical_bill             = '//input[@id="hospital_medical_bill"]'
        self.medical_report                    = '//input[@id="medical_report"]'
        self.police_report                     = '//input[@id="police_report"]'
        self.referral_letter                   = '//input[@id="referral_letter"]'

        #TermLife required document
        self.claimant_statement                = '//input[@id="claimant_statement"]'
        self.aps_form                          = '//input[@id="aps_form"]'
        self.id_of_deceased                    = '//input[@id="id_of_deceased"]'
        self.policy_contract                   = '//input[@id="policy_contract"]'
        self.death_certificate                 = '//input[@id="death_certificate"]'
        self.birth_certificate                 = '//input[@id="birth_certificate"]'
        self.marriage_contract                 = '//input[@id="marriage_contract"]'
        self.letter_of_guardianship            = '//input[@id="letter_of_guardianship"]'
        self.affidavit_of_guardianship         = '//input[@id="affidavit_of_guardianship"]'
        self.police_investigation_report       = '//input[@id="police_investigation_report"]'
        self.autopsy_report                    = '//input[@id="autopsy_report"]'

        #submited successful pop-up
        self.claim_success_img                 = By.XPATH, '//*[(@alt="thankyouImage")]'

    def input_claim_details(self):
        wait_element(self.driver,self.date_injury).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.description_injury).send_keys('Description of Illness/ Injury')

    def input_accident_claim(self):
        wait_element(self.driver,self.date_accident).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.what_doing_accident).send_keys('What were you doing when the accident happened?')
        wait_element(self.driver,self.how_did_the_accident_happen).send_keys('How did the accident happen?')

        yes_no_option = ['Yes', 'No']
        option = choice(yes_no_option)
        related_to_your_work = wait_element(self.driver,(By.XPATH,f'//*[text()="Was your injury/illness caused by or related to your work?"]/following-sibling::div[1]//div[text()="{option}"]'))
        related_to_your_work.click()

        filled_under_ECC = wait_element(self.driver,(By.XPATH,f'//*[text()="Has your claim been filed under the Employee Compensation Commission?"]/following-sibling::div[1]//div[text()="{option}"]'))
        filled_under_ECC.click()

    def upload_insurance_required_document(self):
        id_front = findElements_xpath(self.driver, self.id_front)
        id_front[0].send_keys(f'{path.fixture_dir}/1.jpg')

        id_back = findElements_xpath(self.driver, self.id_back)
        id_back[0].send_keys(f'{path.fixture_dir}/2.jpg')

        apf_form = findElements_xpath(self.driver, self.apf_form)
        apf_form[0].send_keys(f'{path.fixture_dir}/3.jpg')

        medical_certificate = findElements_xpath(self.driver, self.medical_certificate)
        medical_certificate[0].send_keys(f'{path.fixture_dir}/4.jpg')

        hospital_medical_bill = findElements_xpath(self.driver, self.hospital_medical_bill)
        hospital_medical_bill[0].send_keys(f'{path.fixture_dir}/5.jpg')

        medical_report = findElements_xpath(self.driver, self.medical_report)
        medical_report[0].send_keys(f'{path.fixture_dir}/6.jpg')

        police_report = findElements_xpath(self.driver, self.police_report)
        police_report[0].send_keys(f'{path.fixture_dir}/7.jpg')

        referral_letter = findElements_xpath(self.driver, self.referral_letter)
        referral_letter[0].send_keys(f'{path.fixture_dir}/8.jpg')

    def input_disbursement_details(self):
        scroll_to_bottom(self.driver)

        wait_element(self.driver,self.choose_payment_method_dropdown).click()
        wait_element(self.driver,self.GCash_option).click()

        mobile = generate_mobile_phl()
        wait_element(self.driver,self.mobile_input).send_keys(mobile)

        wait_element(self.driver,self.checkbox).click()

    def choose_due_to_other_causes(self):
        wait_element(self.driver,self.due_to_other_causes).click()

    def choose_date_incident(self):
        wait_element(self.driver,self.date_incident).click()
        wait_element(self.driver,self.ok_btn).click()

    def upload_termlife_required_document(self):
        claimant_statement = findElements_xpath(self.driver, self.claimant_statement)
        claimant_statement[0].send_keys(f'{path.fixture_dir}/1.jpg')

        aps_form = findElements_xpath(self.driver, self.aps_form)
        aps_form[0].send_keys(f'{path.fixture_dir}/2.jpg')

        id_of_deceased = findElements_xpath(self.driver, self.id_of_deceased)
        id_of_deceased[0].send_keys(f'{path.fixture_dir}/3.jpg')

        policy_contract = findElements_xpath(self.driver, self.policy_contract)
        policy_contract[0].send_keys(f'{path.fixture_dir}/4.jpg')

        death_certificate = findElements_xpath(self.driver, self.death_certificate)
        death_certificate[0].send_keys(f'{path.fixture_dir}/5.jpg')

        birth_certificate = findElements_xpath(self.driver, self.birth_certificate)
        birth_certificate[0].send_keys(f'{path.fixture_dir}/6.jpg')

        marriage_contract = findElements_xpath(self.driver, self.marriage_contract)
        marriage_contract[0].send_keys(f'{path.fixture_dir}/7.jpg')

        letter_of_guardianship = findElements_xpath(self.driver, self.letter_of_guardianship)
        letter_of_guardianship[0].send_keys(f'{path.fixture_dir}/8.jpg')

        affidavit_of_guardianship = findElements_xpath(self.driver, self.affidavit_of_guardianship)
        affidavit_of_guardianship[0].send_keys(f'{path.fixture_dir}/1.jpg')

        police_investigation_report = findElements_xpath(self.driver, self.police_investigation_report)
        police_investigation_report[0].send_keys(f'{path.fixture_dir}/2.jpg')

        autopsy_report = findElements_xpath(self.driver, self.autopsy_report)
        autopsy_report[0].send_keys(f'{path.fixture_dir}/3.jpg')

    def click_submit_btn(self):
        wait_element(self.driver,self.submit_btn).click()

    def is_claim_successful(self):
        return elementIsDisplayed(self.driver, self.claim_success_img)


class SgInsuranceWebPortalSubmitClaimPage():
    def __init__(self, driver):
        self.driver                           = driver
        #insurance (flep/pa)
        self.start_date_of_mc                 = By.XPATH, '//*[text()="Start Date of MC"]/following-sibling::div[1]'
        self.end_date_of_mc                   = By.XPATH, '//*[text()="End Date of MC"]/following-sibling::div[1]'
        self.accident_type                    = By.XPATH, '//*[text()="Incident Type"]/following-sibling::div//button/div[text()="Accident"]'
        self.illness_type                     = By.XPATH, '//*[text()="Incident Type"]/following-sibling::div//button/div[text()="Illness"]'
        self.date_of_accident                 = By.XPATH, '//*[text()="Date of Accident"]/following-sibling::div[1]'
        self.date_of_illness                  = By.XPATH, '//*[text()="Start of Illness"]/following-sibling::div[1]'
        self.date_of_covid                    = By.XPATH, '//*[text()="Select date and time for COVID 19 Test"]/following-sibling::div[1]'
        self.medical_expense_claim            = By.NAME,  'medical_expense_claim'
        self.incident_description             = By.NAME,  'incident_description'
        self.incident_how                     = By.NAME,  'incident_how'
        self.incident_where                   = By.NAME,  'incident_where'
        self.paynow_nricfin                   = By.NAME,  'paynow_nricfin'
        self.paynow_nickname                  = By.NAME,  'paynow_nickname'
        self.check_box                        = By.XPATH, '//*[contains(@class, "mt-7")]/div[1]'
        self.submit_btn                       = By.XPATH, '//*[text()="SUBMIT"]'
        self.ok_btn                           = By.XPATH, '//*[text()="OK"]'

        # CDW
        self.rental_company                   = By.NAME,  'rental_company'
        self.section1excess                   = By.NAME,  'section1excess'
        self.section2excess                   = By.NAME,  'section2excess'
        self.combined_excess                  = By.NAME,  'combined_excess'
        self.have_paid                        = By.XPATH, '//*[contains(text(), "I/We have paid")]/../div[1]'
        self.have_not_paid                    = By.XPATH, '//*[contains(text(), "I/We have not paid")]/../div[1]'
        self.have_read                        = By.XPATH, '//*[contains(text(), "I have read")]/../div[1]'

        # PA/FLEP
        self.id_front                          = '//input[@id="id_front"]'
        self.id_back                           = '//input[@id="id_back"]'
        self.medical_certificate               = '//input[@id="medical_certificate"]'
        self.medical_report                    = '//input[@id="medical_report"]'
        self.police_report                     = '//input[@id="police_report"]'
        self.referral_letter                   = '//input[@id="referral_letter"]'
        self.inpatient_discharge_sum           = '//input[@id="inpatient_discharge_sum"]'
        self.operation_record                  = '//input[@id="operation_record"]'
        self.hospital_medical_bill             = '//input[@id="hospital_medical_bill"]'

        # CDW
        self.drivers_license_front             = '//input[@id="drivers_license_front"]'
        self.drivers_license_back              = '//input[@id="drivers_license_back"]'
        self.certificate_of_motor_insurance    = '//input[@id="certificate_of_motor_insurance"]'
        self.rental_contract                   = '//input[@id="rental_contract"]'
        self.gia_report                        = '//input[@id="gia_report"]'
        self.proof_of_excess_payable_or_paid   = '//input[@id="proof_of_excess_payable_or_paid"]'
        self.original_repair_invoice           = '//input[@id="original_repair_invoice"]'
        self.photos_of_vehicle_before_repair   = '//input[@id="photos_of_vehicle_before_repair"]'
        self.photos_of_vehicle_after_repair    = '//input[@id="photos_of_vehicle_after_repair"]'
        self.discharge_voucher                 = '//input[@id="discharge_voucher"]'
        self.proof_of_excess_paid              = '//input[@id="proof_of_excess_paid"]'
        self.pcr_art_test                      = '//input[@id="pcr_art_test"]'
        self.paynow_profile_screenshot         = '//input[@id="paynow_profile_screenshot"]'

        self.claim_success_img                 = By.XPATH, '//*[(@alt="thankyouImage")]'


    def flep_input_accident_claim_detail(self):
        wait_element(self.driver,self.start_date_of_mc).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.end_date_of_mc).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.accident_type).click()
        wait_element(self.driver,self.date_of_accident).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.incident_description).send_keys('Description')
        wait_element(self.driver,self.incident_how).send_keys('How did the Accident happen')
        wait_element(self.driver,self.incident_where).send_keys('Where did the accident happen')

    def flep_input_illness_claim_detail(self):
        wait_element(self.driver,self.start_date_of_mc).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.end_date_of_mc).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.illness_type).click()
        wait_element(self.driver,self.date_of_illness).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.incident_description).send_keys('Description')

    def flep_covid_select_date(self):
        wait_element(self.driver,self.date_of_covid).click()
        wait_element(self.driver,self.ok_btn).click()

    def flep_covid_input_required_doc(self):
        id_front = findElements_xpath(self.driver, self.id_front)
        id_front[0].send_keys(f'{path.fixture_dir}/1.jpg')

        id_back = findElements_xpath(self.driver, self.id_back)
        id_back[0].send_keys(f'{path.fixture_dir}/2.jpg')

        pcr_art_test = findElements_xpath(self.driver, self.pcr_art_test)
        pcr_art_test[0].send_keys(f'{path.fixture_dir}/3.jpg')

        medical_certificate = findElements_xpath(self.driver, self.medical_certificate)
        medical_certificate[0].send_keys(f'{path.fixture_dir}/4.jpg')

    def flep_hospital_upload_required_doc(self):
        id_front = findElements_xpath(self.driver, self.id_front)
        id_front[0].send_keys(f'{path.fixture_dir}/1.jpg')

        id_back = findElements_xpath(self.driver, self.id_back)
        id_back[0].send_keys(f'{path.fixture_dir}/2.jpg')

        medical_certificate = findElements_xpath(self.driver, self.medical_certificate)
        medical_certificate[0].send_keys(f'{path.fixture_dir}/3.jpg')

        medical_report = findElements_xpath(self.driver, self.medical_report)
        medical_report[0].send_keys(f'{path.fixture_dir}/4.jpg')

        police_report = findElements_xpath(self.driver, self.police_report)
        police_report[0].send_keys(f'{path.fixture_dir}/5.jpg')

        referral_letter = findElements_xpath(self.driver, self.referral_letter)
        referral_letter[0].send_keys(f'{path.fixture_dir}/6.jpg')

        inpatient_discharge_sum = findElements_xpath(self.driver, self.inpatient_discharge_sum)
        inpatient_discharge_sum[0].send_keys(f'{path.fixture_dir}/7.jpg')

        operation_record = findElements_xpath(self.driver, self.operation_record)
        operation_record[0].send_keys(f'{path.fixture_dir}/8.jpg')

        hospital_medical_bill = findElements_xpath(self.driver, self.hospital_medical_bill)
        hospital_medical_bill[0].send_keys(f'{path.fixture_dir}/1.jpg')

    def flep_medical_upload_required_doc(self):
        id_front = findElements_xpath(self.driver, self.id_front)
        id_front[0].send_keys(f'{path.fixture_dir}/1.jpg')

        id_back = findElements_xpath(self.driver, self.id_back)
        id_back[0].send_keys(f'{path.fixture_dir}/2.jpg')

        medical_certificate = findElements_xpath(self.driver, self.medical_certificate)
        medical_certificate[0].send_keys(f'{path.fixture_dir}/3.jpg')

        medical_report = findElements_xpath(self.driver, self.medical_report)
        medical_report[0].send_keys(f'{path.fixture_dir}/4.jpg')

        police_report = findElements_xpath(self.driver, self.police_report)
        police_report[0].send_keys(f'{path.fixture_dir}/5.jpg')

        referral_letter = findElements_xpath(self.driver, self.referral_letter)
        referral_letter[0].send_keys(f'{path.fixture_dir}/6.jpg')

    def pa_input_claim_detail(self):
        wait_element(self.driver,self.date_of_accident).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.medical_expense_claim).send_keys('50000')
        wait_element(self.driver,self.incident_description).send_keys('Description')
        wait_element(self.driver,self.incident_how).send_keys('How did the Accident happen')
        wait_element(self.driver,self.incident_where).send_keys('Where did the accident happen')

    def pa_upload_required_doc(self):
        id_front = findElements_xpath(self.driver, self.id_front)
        id_front[0].send_keys(f'{path.fixture_dir}/1.jpg')

        id_back = findElements_xpath(self.driver, self.id_back)
        id_back[0].send_keys(f'{path.fixture_dir}/2.jpg')

        inpatient_discharge_sum = findElements_xpath(self.driver, self.inpatient_discharge_sum)
        inpatient_discharge_sum[0].send_keys(f'{path.fixture_dir}/3.jpg')

        medical_report = findElements_xpath(self.driver, self.medical_report)
        medical_report[0].send_keys(f'{path.fixture_dir}/4.jpg')

        hospital_medical_bill = findElements_xpath(self.driver, self.hospital_medical_bill)
        hospital_medical_bill[0].send_keys(f'{path.fixture_dir}/5.jpg')

        police_report = findElements_xpath(self.driver, self.police_report)
        police_report[0].send_keys(f'{path.fixture_dir}/6.jpg')

        referral_letter = findElements_xpath(self.driver, self.referral_letter)
        referral_letter[0].send_keys(f'{path.fixture_dir}/7.jpg')

    def cdw_option_B_input_claim_detail(self):
        wait_element(self.driver,self.rental_company).send_keys('Gigacover')
        wait_element(self.driver,self.date_of_accident).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.combined_excess).send_keys('1000')

    def cdw_option_A_input_claim_detail(self):
        wait_element(self.driver,self.rental_company).send_keys('Gigacover')
        wait_element(self.driver,self.date_of_accident).click()
        wait_element(self.driver,self.ok_btn).click()
        wait_element(self.driver,self.section1excess).send_keys('1000')
        wait_element(self.driver,self.section2excess).send_keys('1500')

    def cdw_upload_required_doc(self):
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

    def cdw_click_checkbox(self):
        wait_element(self.driver,self.check_box).click()
        wait_element(self.driver,self.have_paid).click()
        wait_element(self.driver,self.have_read).click()

    def input_disbursement_detail(self):
        scroll_to_bottom(self.driver)
        nric = generate_nricfin()
        wait_element(self.driver,self.paynow_nricfin).send_keys(nric)
        wait_element(self.driver,self.paynow_nickname).send_keys('paynow nickname')

        paynow_profile_screenshot = findElements_xpath(self.driver, self.paynow_profile_screenshot)
        paynow_profile_screenshot[0].send_keys(f'{path.fixture_dir}/1.jpg')

    def click_checkbox(self):
        wait_element(self.driver,self.check_box).click()

    def click_submit_btn(self):
        scroll_to_bottom(self.driver)
        wait_element(self.driver,self.submit_btn).click()

    def is_claim_successful(self):
        return elementIsDisplayed(self.driver, self.claim_success_img)
