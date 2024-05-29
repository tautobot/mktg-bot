from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element, elementIsDisplayed


class FlepCheckoutPage():
    def __init__(self, driver):
        self.driver = driver
        self.success_msg         = By.XPATH,'//*[@alt="self-buy-success"]'
        self.product_name        = By.XPATH, '//*[text()="Product"]/following-sibling::div'
        self.daily_benefit       = By.XPATH, '//*[text()="Cash Benefits"]/following-sibling::div'
        self.waiting_period      = By.XPATH, '//*[text()="Waiting Period:"]/following-sibling::div'
        self.ip_benefits         = By.XPATH, '//*[text()="Inpatient Benefit Claimable"]/following-sibling::div'
        self.op_benefits         = By.XPATH, '//*[text()="Outpatient Benefit Claimable"]/following-sibling::div'
        self.renewal             = By.XPATH, '//*[text()="Renewal"]/following-sibling::div'
        self.policy_start        = By.XPATH, '//*[text()="Policy Start"]/following-sibling::div'
        self.promo_discount      = By.XPATH, '//*[text()="Promo Discount"]/following-sibling::div'
        self.credit_used         = By.XPATH, '//*[text()="Credits Used"]/following-sibling::div'
        self.total_amount        = By.XPATH, '//*[text()="Total Amount"]/following-sibling::div'
        self.total_saving        = By.XPATH, '//*[text()="Total Saving"]/following-sibling::div'
        self.gst                 = By.XPATH, '//*[text()="9% GST"]/following-sibling::div'
        self.final_amount        = By.XPATH, '//*[text()="Final Amount Due"]/following-sibling::div'
        self.refcode             = By.XPATH, '//*[@placeholder="Enter Referral Code"]'
        self.apply_btn           = By.XPATH, '//button[text()="APPLY"]'

    def apply_refcode(self, refcode):
        wait_element(self.driver, self.refcode).send_keys(refcode)
        wait_element(self.driver, self.apply_btn).click()

    def get_refcode_msg(self, refcode):
        return wait_element(self.driver,(By.XPATH, f'//*[text()="{refcode}"]/../following-sibling::div[1]')).text

    def get_data_inputted(self):
        data_inputted                                    = {}
        data_inputted['product_name']                    = wait_element(self.driver,self.product_name).text
        data_inputted['daily_benefit']                   = wait_element(self.driver,self.daily_benefit).text
        data_inputted['waiting_period']                  = wait_element(self.driver,self.waiting_period).text
        data_inputted['ip_benefits']                     = wait_element(self.driver,self.ip_benefits).text
        data_inputted['op_benefits']                     = wait_element(self.driver,self.op_benefits).text
        data_inputted['renewal']                         = wait_element(self.driver,self.renewal).text
        data_inputted['policy_start']                    = wait_element(self.driver,self.policy_start).text
        data_inputted['promo_discount']                  = wait_element(self.driver,self.promo_discount).text
        data_inputted['credit_used']                     = wait_element(self.driver,self.credit_used).text
        data_inputted['total_amount']                    = wait_element(self.driver,self.total_amount).text
        data_inputted['total_saving']                    = wait_element(self.driver,self.total_saving).text
        data_inputted['gst']                             = wait_element(self.driver,self.gst).text
        data_inputted['final_amount']                    = wait_element(self.driver,self.final_amount).text
        return data_inputted

    def is_buy_success(self):
        return elementIsDisplayed(self.driver, self.success_msg)


class PaCheckoutPage():
    def __init__(self, driver):
        self.driver = driver
        self.success_msg                    = By.XPATH, '//*[@alt="self-buy-success"]'
        self.product_name                   = By.XPATH, '//*[text()="Product"]/following-sibling::div'
        self.sum_insured                    = By.XPATH, '//*[text()="Sum Insured"]/following-sibling::div'
        self.activation_period              = By.XPATH, '//*[text()="Activation Period"]/following-sibling::div'
        self.medical_expense_reimbursement  = By.XPATH, '//*[text()="Medical Expense Reimbursement"]/following-sibling::div'
        self.renewal                        = By.XPATH, '//*[text()="Renewal"]/following-sibling::div'
        self.policy_start                   = By.XPATH, '//*[text()="Policy Start"]/following-sibling::div'
        self.promo_discount                 = By.XPATH, '//*[text()="Promo Discount"]/following-sibling::div'
        self.credit_used                    = By.XPATH, '//*[text()="Credits Used"]/following-sibling::div'
        self.total_amount                   = By.XPATH, '//*[text()="Total Amount"]/following-sibling::div'
        self.total_saving                   = By.XPATH, '//*[text()="Total Saving"]/following-sibling::div'
        self.gst                            = By.XPATH, '//*[text()="9% GST"]/following-sibling::div'
        self.final_amount_due               = By.XPATH, '//*[text()="Final Amount Due"]/following-sibling::div'
        self.refcode                        = By.XPATH, '//*[@placeholder="Enter Referral Code"]'
        self.apply_btn                      = By.XPATH, '//button[text()="APPLY"]'

    def apply_refcode(self, refcode):
        wait_element(self.driver,self.refcode).send_keys(refcode)
        wait_element(self.driver,self.apply_btn).click()

    def get_refcode_msg(self, refcode):
        return wait_element(self.driver,(By.XPATH, f'//*[text()="{refcode}"]/../following-sibling::div[1]')).text

    def get_data_inputted(self):
        data_inputted                                           = {}
        data_inputted['product_name']                           = wait_element(self.driver,self.product_name).text
        data_inputted['sum_insured']                            = wait_element(self.driver,self.sum_insured).text
        data_inputted['activation_period']                      = wait_element(self.driver,self.activation_period).text
        data_inputted['medical_expense_reimbursement']          = wait_element(self.driver,self.medical_expense_reimbursement).text
        data_inputted['renewal']                                = wait_element(self.driver,self.renewal).text
        data_inputted['policy_start']                           = wait_element(self.driver,self.policy_start).text
        data_inputted['promo_discount']                         = wait_element(self.driver,self.promo_discount).text
        data_inputted['credit_used']                            = wait_element(self.driver,self.credit_used).text
        data_inputted['total_amount']                           = wait_element(self.driver,self.total_amount).text
        data_inputted['total_saving']                           = wait_element(self.driver,self.total_saving).text
        data_inputted['gst']                                    = wait_element(self.driver,self.gst).text
        data_inputted['final_amount_due']                       = wait_element(self.driver,self.final_amount_due).text
        return data_inputted

    def is_buy_success(self):
        return elementIsDisplayed(self.driver, self.success_msg)


class CdwCheckoutPage():
    def __init__(self, driver):
        self.driver = driver
        self.success_msg         = By.XPATH, '//*[@alt="self-buy-success"]'
        self.product_name        = By.XPATH, '//*[text()="Product"]/following-sibling::div'
        self.ss1_ss2             = By.XPATH, '//*[text()="Section 1 / Section 2"]/following-sibling::div'
        self.combined            = By.XPATH, '//*[text()="Combined"]/following-sibling::div'
        self.excess_reduced      = By.XPATH, '//*[text()="Excess Reduced to"]/following-sibling::div'
        self.renewal             = By.XPATH, '//*[text()="Renewal"]/following-sibling::div'
        self.policy_start        = By.XPATH, '//*[text()="Policy Start"]/following-sibling::div'
        self.daily_rate          = By.XPATH, '//*[text()="Daily Rate"]/following-sibling::div'
        self.promo_discount      = By.XPATH, '//*[text()="Promo Discount"]/following-sibling::div'
        self.credit_used         = By.XPATH, '//*[text()="Credits Used"]/following-sibling::div'
        self.total_amount        = By.XPATH, '//*[text()="Total Amount"]/following-sibling::div'
        self.total_saving        = By.XPATH, '//*[text()="Total Saving"]/following-sibling::div'
        self.gst                 = By.XPATH, '//*[text()="9% GST"]/following-sibling::div'
        self.final_amount_due    = By.XPATH, '//*[text()="Final Amount Due"]/following-sibling::div'
        self.refcode             = By.XPATH, '//*[@placeholder="Enter Referral Code"]'
        self.apply_btn           = By.XPATH, '//button[text()="APPLY"]'
        self.refcode_msg         = By.XPATH, '//*[@placeholder="Enter Referral Code"]/../following-sibling::div[1]'

        self.overlap_error_msg   = By.XPATH, '//*[contains(text(), "You already have an existing policy that covers you for that period. You can purchase another starting after")]'

        #CDWY
        self.cdwy_product_name   = By.XPATH, '//*[text()="Product"]/../following-sibling::div'
        self.cdwy_renewal        = By.XPATH, '//*[text()="Renewal"]/../following-sibling::div'
        self.cdwy_policy_start   = By.XPATH, '//*[text()="Policy Start"]/../following-sibling::div'
        self.cdwy_promo_discount = By.XPATH, '//*[text()="Promo Discount"]/../following-sibling::div'
        self.cdwy_total_saving   = By.XPATH, '//*[text()="Total Savings"]/../following-sibling::div'
        self.cdwy_total_payable  = By.XPATH, '//*[text()="Total Payable"]/../following-sibling::div'

    def apply_refcode(self, refcode):
        wait_element(self.driver,self.refcode).send_keys(refcode)
        wait_element(self.driver,self.apply_btn).click()

    def get_refcode_msg(self, refcode):
        return wait_element(self.driver,(By.XPATH,f'//*[text()="{refcode}"]/../following-sibling::div[1]')).text

    def get_data_inputted(self, optionB = False):
        data_inputted                                       = {}
        if optionB :
            data_inputted['combined']                       = wait_element(self.driver,self.combined).text
        else:
            data_inputted['ss1_ss2']                        = wait_element(self.driver,self.ss1_ss2).text

        data_inputted['product_name']                       = wait_element(self.driver,self.product_name).text
        data_inputted['excess_reduced']                     = wait_element(self.driver,self.excess_reduced).text
        data_inputted['renewal']                            = wait_element(self.driver,self.renewal).text
        data_inputted['policy_start']                       = wait_element(self.driver,self.policy_start).text
        data_inputted['promo_discount']                     = wait_element(self.driver,self.promo_discount).text
        data_inputted['credit_used']                        = wait_element(self.driver,self.credit_used).text
        data_inputted['total_amount']                       = wait_element(self.driver,self.total_amount).text
        data_inputted['total_saving']                       = wait_element(self.driver,self.total_saving).text
        data_inputted['gst']                                = wait_element(self.driver,self.gst).text
        data_inputted['final_amount_due']                   = wait_element(self.driver,self.final_amount_due).text
        return data_inputted

    def cdwy_get_data_inputted(self):
        data_inputted                                       = {}
        data_inputted['product_name']                       = wait_element(self.driver,self.cdwy_product_name).text
        data_inputted['renewal']                            = wait_element(self.driver,self.cdwy_renewal).text
        data_inputted['policy_start']                       = wait_element(self.driver,self.cdwy_policy_start).text
        data_inputted['promo_discount']                     = wait_element(self.driver,self.cdwy_promo_discount).text
        data_inputted['total_saving']                       = wait_element(self.driver,self.cdwy_total_saving).text
        data_inputted['total_payable']                      = wait_element(self.driver,self.cdwy_total_payable).text
        return data_inputted

    def is_buy_success(self):
        return elementIsDisplayed(self.driver, self.success_msg)

    def is_overlap(self):
        return elementIsDisplayed(self.driver, self.overlap_error_msg)

class PmlCheckoutPage():
    def __init__(self, driver):
        self.driver = driver
        self.success_msg            = By.XPATH, '//*[text()="Congratulations"]'
        self.product_name           = By.XPATH, '//*[text()="Product"]/../following-sibling::div'
        self.cash_benefits          = By.XPATH, '//*[text()="Cash Benefit"]/../following-sibling::div'
        self.waiting_period         = By.XPATH, '//*[text()="Waiting Period"]/../following-sibling::div'
        self.ip_benefits            = By.XPATH, '//*[text()="Inpatient Benefit Claimable"]/../following-sibling::div'
        self.op_benefits            = By.XPATH, '//*[text()="Outpatient Benefit Claimable"]/../following-sibling::div'
        self.renewal                = By.XPATH, '//*[text()="Renewal"]/../following-sibling::div'
        self.policy_start           = By.XPATH, '//*[text()="Policy Start"]/../following-sibling::div'
        self.total_amount           = By.XPATH, '//*[text()="Total Amount"]/../following-sibling::div'
        self.gst                    = By.XPATH, '//*[text()="9% GST"]/../following-sibling::div'
        self.discount               = By.XPATH, '//*[text()="Discount"]/../following-sibling::div'
        self.total_annual_payable   = By.XPATH, '//*[text()="Total Annual Payable"]/../following-sibling::div'
        self.refcode                = By.XPATH, '//*[@placeholder="Promo Code"]'
        self.apply_btn              = By.XPATH, '//button[text()="Apply"]'

    def apply_refcode(self, refcode):
        wait_element(self.driver,self.refcode).send_keys(refcode)
        wait_element(self.driver,self.apply_btn).click()

    def get_refcode_msg(self, refcode):
        return wait_element(self.driver,(By.XPATH,f'//*[text()="{refcode}"]/../following-sibling::div[1]')).text

    def get_data_inputted(self):
        data_inputted                         = {}
        data_inputted['product_name']         = wait_element(self.driver,self.product_name).text
        data_inputted['cash_benefits']        = wait_element(self.driver,self.cash_benefits).text
        data_inputted['waiting_period']       = wait_element(self.driver,self.waiting_period).text
        data_inputted['ip_benefits']          = wait_element(self.driver,self.ip_benefits).text
        data_inputted['op_benefits']          = wait_element(self.driver,self.op_benefits).text
        data_inputted['renewal']              = wait_element(self.driver,self.renewal).text
        data_inputted['policy_start']         = wait_element(self.driver,self.policy_start).text
        data_inputted['total_amount']         = wait_element(self.driver,self.total_amount).text
        data_inputted['gst']                  = wait_element(self.driver,self.gst).text
        data_inputted['discount']             = wait_element(self.driver,self.discount).text
        data_inputted['total_annual_payable'] = wait_element(self.driver,self.total_annual_payable).text
        return data_inputted

    def congratulations_text(self):
        return elementIsDisplayed(self.driver, self.success_msg)


class ZeekCheckoutPage():
    def __init__(self, driver):
        self.driver = driver

        #Flep
        self.success_msg                   = By.XPATH, '//*[text()="Congratulations"]'
        self.product_name                  = By.XPATH, '//*[text()="Product"]/../following-sibling::div'
        self.daily_benefit                 = By.XPATH, '//*[text()="Cash Benefits"]/../following-sibling::div'
        self.waiting_period                = By.XPATH, '//*[text()="Waiting Period:"]/../following-sibling::div'
        self.ip_benefits                   = By.XPATH, '//*[text()="Inpatient Benefit Claimable"]/../following-sibling::div'
        self.op_benefits                   = By.XPATH, '//*[text()="Outpatient Benefit Claimable"]/../following-sibling::div'
        self.renewal                       = By.XPATH, '//*[text()="Renewal"]/../following-sibling::div'
        self.policy_start                  = By.XPATH, '//*[text()="Policy Start"]/../following-sibling::div'
        self.promo_discount                = By.XPATH, '//*[text()="Promo Discount"]/../following-sibling::div'
        self.credit_used                   = By.XPATH, '//*[text()="Credits Used"]/../following-sibling::div'
        self.total_amount                  = By.XPATH, '//*[text()="Total Amount"]/../following-sibling::div'
        self.total_saving                  = By.XPATH, '//*[text()="Total Saving"]/../following-sibling::div'
        self.gst                           = By.XPATH, '//*[text()="9% GST"]/../following-sibling::div'
        self.final_amount                  = By.XPATH, '//*[text()="Final Amount Due"]/../following-sibling::div'
        self.refcode                       = By.XPATH, '//*[@placeholder="Promo Code"]'
        self.apply_btn                     = By.XPATH, '//button[text()="APPLY"]'
        self.refcode_msg                   = By.XPATH, '//*[@placeholder="Promo Code"]/../../following-sibling::div[1]'

        #Pa
        self.sum_insured                   = By.XPATH, '//*[text()="Sum Insured"]/../following-sibling::div'
        self.activation_period             = By.XPATH, '//*[text()="Activation Period"]/../following-sibling::div'
        self.medical_expense_reimbursement = By.XPATH, '//*[text()="Medical Expense Reimbursement"]/../following-sibling::div'

    def get_flep_data_inputted(self):
        data_inputted                                    = {}
        data_inputted['product_name']                    = wait_element(self.driver,self.product_name).text
        data_inputted['daily_benefit']                   = wait_element(self.driver,self.daily_benefit).text
        data_inputted['waiting_period']                  = wait_element(self.driver,self.waiting_period).text
        data_inputted['ip_benefits']                     = wait_element(self.driver,self.ip_benefits).text
        data_inputted['op_benefits']                     = wait_element(self.driver,self.op_benefits).text
        data_inputted['renewal']                         = wait_element(self.driver,self.renewal).text
        data_inputted['policy_start']                    = wait_element(self.driver,self.policy_start).text
        data_inputted['promo_discount']                  = wait_element(self.driver,self.promo_discount).text
        data_inputted['credit_used']                     = wait_element(self.driver,self.credit_used).text
        data_inputted['total_amount']                    = wait_element(self.driver,self.total_amount).text
        data_inputted['total_saving']                    = wait_element(self.driver,self.total_saving).text
        data_inputted['gst']                             = wait_element(self.driver,self.gst).text
        data_inputted['final_amount']                    = wait_element(self.driver,self.final_amount).text
        return data_inputted

    def get_pa_data_inputted(self):
        data_inputted                                        = {}
        data_inputted['product_name']                        = wait_element(self.driver,self.product_name).text
        data_inputted['sum_insured']                         = wait_element(self.driver,self.sum_insured).text
        data_inputted['activation_period']                   = wait_element(self.driver,self.activation_period).text
        data_inputted['medical_expense_reimbursement']       = wait_element(self.driver,self.medical_expense_reimbursement).text
        data_inputted['renewal']                             = wait_element(self.driver,self.renewal).text
        data_inputted['policy_start']                        = wait_element(self.driver,self.policy_start).text
        data_inputted['promo_discount']                      = wait_element(self.driver,self.promo_discount).text
        data_inputted['credit_used']                         = wait_element(self.driver,self.credit_used).text
        data_inputted['total_amount']                        = wait_element(self.driver,self.total_amount).text
        data_inputted['total_saving']                        = wait_element(self.driver,self.total_saving).text
        data_inputted['gst']                                 = wait_element(self.driver,self.gst).text
        data_inputted['final_amount']                        = wait_element(self.driver,self.final_amount).text
        return data_inputted

    def apply_refcode(self, refcode):
        wait_element(self.driver,self.refcode).send_keys(refcode)
        wait_element(self.driver,self.apply_btn).click()

    def get_refcode_msg(self):
        return wait_element(self.driver,self.refcode_msg).text

    def congratulations_text(self):
        return elementIsDisplayed(self.driver, self.success_msg)


class HealthCheckoutPage():
    def __init__(self, driver):
        self.driver                            = driver
        self.product_name                      = By.XPATH, '//*[text()="Product"]/../following-sibling::div'
        self.daily_benefit                     = By.XPATH, '//*[text()="Cash Benefit"]/../following-sibling::div'
        self.waiting_period                    = By.XPATH, '//*[text()="Waiting Period:"]/../following-sibling::div'
        self.renewal                           = By.XPATH, '//*[text()="Renewal"]/../following-sibling::div'
        self.policy_start                      = By.XPATH, '//*[text()="Policy Start"]/../following-sibling::div'
        self.subtotal                          = By.XPATH, '//*[text()="Subtotal"]/../following-sibling::div'
        self.promo_discount                    = By.XPATH, '//*[text()="Promo Discount"]/../following-sibling::div'
        self.credit_used                       = By.XPATH, '//*[text()="Credits Used"]/../following-sibling::div'
        self.total_amount                      = By.XPATH, '//*[text()="Total Amount"]/../following-sibling::div'
        self.total_saving                      = By.XPATH, '//*[text()="Total Saving"]/../following-sibling::div'
        self.primary_coverage                  = By.XPATH, '//*[text()="Primary Coverage"]/../following-sibling::div'
        self.dependent_coverage                = By.XPATH, '//*[text()="Dependent Coverage"]/../following-sibling::div'
        self.vat                               = By.XPATH, '//*[text()="12% VAT"]/../following-sibling::div'
        self.processing_fee                    = By.XPATH, '//*[text()="Bank Processing Fee"]/../following-sibling::div'
        self.total_annual_payable              = By.XPATH, '//*[text()="Total Annual Payable"]/../following-sibling::div'
        self.refcode                           = By.XPATH, '//*[@placeholder="Enter Referral Code"]'
        self.apply_btn                         = By.XPATH, '//button[text()="APPLY"]'

    def get_hmo_data_inputted(self, with_dependent=False):
        data_inputted                                    = {}
        data_inputted['product_name']                    = wait_element(self.driver,self.product_name).text
        data_inputted['daily_benefit']                   = wait_element(self.driver,self.daily_benefit).text
        data_inputted['waiting_period']                  = wait_element(self.driver,self.waiting_period).text
        data_inputted['renewal']                         = wait_element(self.driver,self.renewal).text
        data_inputted['subtotal']                        = wait_element(self.driver,self.subtotal).text
        data_inputted['promo_discount']                  = wait_element(self.driver,self.promo_discount).text
        data_inputted['credit_used']                     = wait_element(self.driver,self.credit_used).text
        data_inputted['total_amount']                    = wait_element(self.driver,self.total_amount).text
        data_inputted['total_saving']                    = wait_element(self.driver,self.total_saving).text
        data_inputted['primary_coverage']                = wait_element(self.driver,self.primary_coverage).text
        if with_dependent:
            data_inputted['dependent_coverage']          = wait_element(self.driver,self.dependent_coverage).text
        data_inputted['vat']                             = wait_element(self.driver,self.vat).text
        data_inputted['processing_fee']                  = wait_element(self.driver,self.processing_fee).text
        data_inputted['total_annual_payable']            = wait_element(self.driver,self.total_annual_payable).text
        return data_inputted

    def apply_refcode(self, refcode):
        wait_element(self.driver,self.refcode).send_keys(refcode)
        wait_element(self.driver,self.apply_btn).click()

    def get_refcode_msg(self, refcode):
        return wait_element(self.driver,(By.XPATH, f'//*[text()="{refcode}"]/../following-sibling::div')).text


class PetCheckoutPage():
    def __init__(self, driver):
        self.driver               = driver
        self.product_name         = By.XPATH, '//*[text()="Product"]/../following-sibling::div'
        self.waiting_period       = By.XPATH, '//*[text()="Waiting Period"]/../following-sibling::div'
        self.renewal              = By.XPATH, '//*[text()="Renewal"]/../following-sibling::div'
        self.primary_coverage     = By.XPATH, '//*[text()="Primary Coverage"]/../following-sibling::div'
        self.promo_discount       = By.XPATH, '//*[text()="Promo Discount"]/../following-sibling::div'
        self.credit_used          = By.XPATH, '//*[text()="Credits Used"]/../following-sibling::div'
        self.total_amount         = By.XPATH, '//*[text()="Total Amount"]/../following-sibling::div'
        self.total_saving         = By.XPATH, '//*[text()="Total Savings"]/../following-sibling::div'
        self.vat                  = By.XPATH, '//*[text()="VAT (12%)"]/../following-sibling::div'
        self.processing_fee       = By.XPATH, '//*[text()="Bank Processing Fee"]/../following-sibling::div'
        self.total_annual_payable = By.XPATH, '//*[text()="Total Annual Payable"]/../following-sibling::div'
        self.refcode              = By.XPATH, '//*[@placeholder="Enter Referral Code"]'
        self.apply_btn            = By.XPATH, '//button[text()="APPLY"]'


    def get_pet_data_inputted(self):
        data_inputted                                    = {}
        data_inputted['product_name']                    = wait_element(self.driver,self.product_name).text
        data_inputted['waiting_period']                   = wait_element(self.driver,self.waiting_period).text
        data_inputted['renewal']                         = wait_element(self.driver,self.renewal).text
        data_inputted['promo_discount']                  = wait_element(self.driver,self.promo_discount).text
        data_inputted['credit_used']                     = wait_element(self.driver,self.credit_used).text
        data_inputted['total_amount']                    = wait_element(self.driver,self.total_amount).text
        data_inputted['total_saving']                    = wait_element(self.driver,self.total_saving).text
        data_inputted['primary_coverage']                = wait_element(self.driver,self.primary_coverage).text
        data_inputted['vat']                             = wait_element(self.driver,self.vat).text
        data_inputted['processing_fee']                  = wait_element(self.driver,self.processing_fee).text
        data_inputted['total_annual_payable']            = wait_element(self.driver,self.total_annual_payable).text
        return data_inputted

    def apply_refcode(self, refcode):
        wait_element(self.driver,self.refcode).send_keys(refcode)
        wait_element(self.driver,self.apply_btn).click()

    def get_refcode_msg(self, refcode):
        return wait_element(self.driver,(By.XPATH, f'//*[text()="{refcode}"]/../following-sibling::div')).text

