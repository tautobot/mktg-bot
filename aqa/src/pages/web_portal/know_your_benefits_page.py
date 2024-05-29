from random import choice

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait, wait_element, elementIsDisplayed, findElements_xpath


class WebPortalKnowYourBenefitsPage():

    def __init__(self, driver):
        self.driver                              = driver
        self.your_benefits                       = '//div[text()="Your Benefits"]/following-sibling::div'
        self.renew_policy_button                 = By.XPATH, '//button[text()="RENEW POLICY"]'
        self.cancel_policy_button                = By.XPATH, '//button[text()="Cancel policy"]'
        self.back_to_home_button                 = By.XPATH, '//button[text()="BACK TO HOME"]'
        self.update_card_successful_text         = By.XPATH, '//*[text()="Update card detail successfully"]'
        self.payment_method_required_msg         = By.XPATH, '//*[text()="Please add payment method"]'

        self.cancel_renewal_successful_text      = By.XPATH, '//*[(@alt="sorry-to-see-you-leaving")]'
                                                
        self.iframe_card_number                  = By.XPATH, '//iframe[@title="Secure card number input frame"]'
        self.iframe_expiry_date                  = By.XPATH, '//iframe[@title="Secure expiration date input frame"]'
        self.iframe_cvc                          = By.XPATH, '//iframe[@title="Secure CVC input frame"]'

        self.card_name                           = By.NAME, 'cardName'
        self.card_number                         = By.NAME, 'cardNumber'
        self.expiry_date                         = By.NAME, 'cardExpiry'
        self.cvc                                 = By.NAME, 'cardCvc'

        self.already_has_card                    = By.XPATH, '//*[contains(text(),"Debit / Credit Card -")]'
        self.active_Ecard_successful_text        = By.XPATH, '//div[text()="Payment method added"]'

        self.member_id                           = By.XPATH, '//div[text()="Member ID"]/following-sibling::div'
        self.start_date                          = By.XPATH, '//div[text()="Start Date"]/following-sibling::div'
        self.policy_status                       = By.XPATH, '//div[text()="Status"]/following-sibling::div'
        self.monthly_auto_renewal                = By.XPATH, '//div[text()="Monthly Auto Renew"]/following-sibling::div'
        self.renew_button                        = By.XPATH, '//button[text()="RENEW POLICY"]'
        self.cancel_button                       = By.XPATH, '//button[text()="Cancel policy"]'
        self.premium                             = By.XPATH, '//*[text()="Your Premium"]/following-sibling::div'
        self.gst                                 = By.XPATH, '//*[text()="9% GST"]/following-sibling::div'
        self.total_premium                       = By.XPATH, '//*[contains(text(), "Total Premium is")]/../following-sibling::div'
        self.charge_amount                       = By.XPATH, '//*[text()="You will be charged"]/following-sibling::p'
        self.edit_payment_details                = By.XPATH, '//*[text()="Payment Details"]/../following-sibling::div/img'
        self.level_of_coverage_dropdown          = By.XPATH, '//*[text()="Level of coverage"]/following-sibling::div/div'
        self.update_btn                          = By.XPATH, '//button[text()="UPDATE"]'
        self.pay_now_btn                         = By.XPATH, '//button[text()="PAY NOW"]'
        self.confirm_btn                         = By.XPATH, '//button[text()="CONFIRM"]'

        #CDW
        self.edit_btn                            = By.XPATH, '(//*[@alt="edit"])[1]'
        self.vehicle_number                      = By.XPATH, '//*[text()="Vehicle Number"]/following-sibling::div[1]/input'
        self.combined_excess_dropdown            = By.XPATH, '//*[text()="Combined Excess"]/following-sibling::div[1]'
        self.reduced_excess_dropdown             = By.XPATH, '//*[text()="Reduced Excess To"]/following-sibling::div[1]'
        self.section1_dropdown                   = By.XPATH, '//*[text()="Section 1 Excess"]/following-sibling::div[1]'
        self.section2_dropdown                   = By.XPATH, '//*[text()="Section 2 Excess"]/following-sibling::div[1]'
        self.reduced_excess_500                  = By.XPATH, '//*[text()="Reduced Excess To"]/following-sibling::div//option[@value="500"]'
        self.section1_1400                       = By.XPATH, '//*[text()="Section 1 Excess"]/following-sibling::div//option[@value="1400"]'
        self.section2_1400                       = By.XPATH, '//*[text()="Section 2 Excess"]/following-sibling::div//option[@value="1400"]'
                   
       #Essentials
        self.got_it_btn                          = By.XPATH, '//button[text()="GOT IT!"]'
        self.gp_annual_balance                   = By.XPATH, '//*[text()="GP"]/following-sibling::div[1]'
        self.gp_subsidy_cap                      = By.XPATH, '//*[text()="GP"]/following-sibling::div[2]'
        self.dental_annual_balance               = By.XPATH, '//*[text()="Dental"]/following-sibling::div[1]'
        self.dental_subsidy_cap                  = By.XPATH, '//*[text()="Dental"]/following-sibling::div[2]'
        self.tcm_annual_balance                  = By.XPATH, '//*[text()="TCM"]/following-sibling::div[1]'
        self.tcm_subsidy_cap                     = By.XPATH, '//*[text()="TCM"]/following-sibling::div[2]'
        self.active_Ecard_btn                    = By.XPATH, '//button[text()="ACTIVE E-CARD"]'
        self.activate_Ecard_btn                  = By.XPATH, '//button[text()="ACTIVATE E-CARD"]'
        self.view_Ecard_btn                      = By.XPATH, '//button[text()="VIEW E-CARD"]'
        
    def get_member_id(self):
        return wait_element(self.driver,self.member_id).text

    def get_start_date(self):
        return wait_element(self.driver,self.start_date).text

    def get_policy_status(self):
        return wait_element(self.driver,self.policy_status).text

    def get_monthly_auto_renewal(self):
        return wait_element(self.driver,self.monthly_auto_renewal).text

    def get_your_benefits(self):
        return findElements_xpath(self.driver, self.your_benefits)

    def is_renewable(self):
        return elementIsDisplayed(self.driver, self.renew_policy_button)

    def is_cancel_renewal_successful(self):
        return elementIsDisplayed(self.driver, self.cancel_renewal_successful_text)

    def is_already_has_card(self):
        return elementIsDisplayed(self.driver, self.already_has_card)

    def click_back_to_home_button(self):
        wait_element(self.driver,self.back_to_home_button).click()

    def is_cancelable(self):
        return elementIsDisplayed(self.driver, self.cancel_policy_button)

    def click_renew_btn(self):
        wait_element(self.driver,self.renew_button).click()

    def click_cancel_btn(self):
        wait_element(self.driver,self.cancel_button).click()

    def click_confirm_btn(self):
        wait_element(self.driver,self.confirm_btn).click()

    def click_edit_btn(self):
        wait_element(self.driver,self.edit_btn).click()

    def click_update_btn(self):
        wait_element(self.driver,self.update_btn).click()

    def click_got_it_btn(self):
        wait_element(self.driver,self.got_it_btn).click()

    def click_active_Ecard_btn(self):
        wait_element(self.driver,self.active_Ecard_btn).click()

    def click_view_Ecard_btn(self):
        wait_element(self.driver,self.view_Ecard_btn).click()

    def input_vehicle_number(self):
        wait_element(self.driver,self.vehicle_number).clear()
        wait_element(self.driver,self.vehicle_number).send_keys('testvehicle')

    def change_level_of_coverage(self, coverage):
        wait_element(self.driver, self.level_of_coverage_dropdown).click()
        level = wait_element(self.driver, (By.XPATH,f'//li[text()="{coverage}"]'))
        level.click()

    def get_renew_price(self):
        actual_price                  = {}
        actual_price['premium']       = wait_element(self.driver,self.premium).text
        actual_price['gst']           = wait_element(self.driver,self.gst).text
        actual_price['total_premium'] = wait_element(self.driver,self.total_premium).text
        actual_price['charge_amount'] = wait_element(self.driver,self.charge_amount).text
        return actual_price

    def add_payment_detail(self):
        wait_element(self.driver,self.edit_payment_details).click()
        wait_element(self.driver,self.card_name).send_keys('Test aqa')

        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys('4444')

        wait_element(self.driver,self.expiry_date).send_keys('1234')
        wait_element(self.driver,self.cvc).send_keys('123')
        wait_element(self.driver,self.update_btn).click()

    def active_Ecard(self):
        wait_element(self.driver,self.card_name).send_keys('Test aqa')

        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys('5555')
        wait_element(self.driver,self.card_number).send_keys(Keys.END)
        wait_element(self.driver,self.card_number).send_keys('4444')

        wait_element(self.driver,self.expiry_date).send_keys('1234')
        wait_element(self.driver,self.cvc).send_keys('123')

        wait_element(self.driver,self.activate_Ecard_btn).click()

    def is_added_payment_detail(self):
        return elementIsDisplayed(self.driver, self.update_card_successful_text)

    def payment_method_required_error_msg(self):
        return elementIsDisplayed(self.driver, self.payment_method_required_msg)

    def click_on_pay_now_btn(self):
        wait_element(self.driver,self.pay_now_btn).click()

    def is_renewal_successful(self):
        return elementIsDisplayed(self.driver, self.cancel_policy_button)

    def is_active_Ecard_successful(self):
        return elementIsDisplayed(self.driver, self.active_Ecard_successful_text)

    def cdw_edit_to_combined_excess(self):
        wait_element(self.driver,self.combined_excess_dropdown).click()
        combine_excess_list = [1500, 2000, 2500, 3000, 3500, 4000]
        combine_excess = choice(combine_excess_list)
        wait_element(self.driver,(By.XPATH, f'//*[text()="Combined Excess"]/following-sibling::div//option[@value="{combine_excess}"]')).click()
        wait_element(self.driver,self.reduced_excess_dropdown).click()
        wait_element(self.driver,self.reduced_excess_500).click()

    def cdw_edit_to_section(self):
        wait_element(self.driver,self.section1_dropdown).click()
        wait_element(self.driver,self.section1_1400).click()
        wait_element(self.driver,self.section2_dropdown).click()
        wait_element(self.driver,self.section2_1400).click()
        wait_element(self.driver,self.reduced_excess_dropdown).click()
        wait_element(self.driver,self.reduced_excess_500).click()

    def essentials_get_company_sponsorship(self):
        data                          = {}
        data['gp_annual_balance']     = wait_element(self.driver,self.gp_annual_balance).text
        data['gp_subsidy_cap']        = wait_element(self.driver,self.gp_subsidy_cap).text
        data['dental_annual_balance'] = wait_element(self.driver,self.dental_annual_balance).text
        data['dental_subsidy_cap']    = wait_element(self.driver,self.dental_subsidy_cap).text
        data['tcm_annual_balance']    = wait_element(self.driver,self.tcm_annual_balance).text
        data['tcm_subsidy_cap']       = wait_element(self.driver,self.tcm_subsidy_cap).text
        return data
