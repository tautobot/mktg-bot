import unittest

from testcases.lib.generic import read_cell_in_excel_file
from aQA.webdriver.appium_weddriver import *
from aQA.android.src.app_file.util import *

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = android_webdriver()

    def tearDown(self): self.driver.quit()

    def test_00_Loan_Eng(self):
        excel_file = f'{app_path}/fixtures/loan_template.xlsx'
        email = read_cell_in_excel_file(excel_file, 'F2')
        pwd = read_cell_in_excel_file(excel_file, 'E2')

        login_pouch(self.driver, email, pwd)
        wait()
        tutorial_welcome(self.driver)

        wait()
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Traditional Chinese Medicine"]'), wait_xpath(self.driver, "//*[@text='Doctor (GP)']"))
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Dental"]'), wait_xpath(self.driver, "//*[@text='Traditional Chinese Medicine']"))
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Dental"]'), wait_xpath(self.driver, "//*[@text='Traditional Chinese Medicine']"))
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Healthscreen"]'), wait_xpath(self.driver, "//*[@text='Dental']"))
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Healthscreen"]'), wait_xpath(self.driver, "//*[@text='Dental']"))

        wait_xpath(self.driver, '//*[@text="Loan"]').click()
        wait_xpath(self.driver, '//*[@text="Request A Loan Quote"]').click()
        wait_xpath(self.driver, '//*[@text="PROCEED"]').click()

        # region Personal Details
        Residency = wait_xpath(self.driver, '(//*[@text="Residency*"]/../android.view.ViewGroup)[1]') ; Residency.click()
        Singaporean = wait_xpath(self.driver, '//*[@text="Singaporean"]') ; Singaporean.click()

        Nationality = wait_xpath(self.driver, '(//*[@text="Nationality*"]/../android.view.ViewGroup)[1]') ; Nationality.click()
        Singapore = wait_xpath(self.driver, '//*[@text="Singapore"]'); Singapore.click()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Nationality*"]'), wait_xpath(self.driver, "//*[@text='Personal Details']"))

        # Telephone = wait_xpath(self.driver, '//*[@text="Telephone Number*"]/../android.widget.EditText')
        # Telephone.send_keys('84123456')
        #
        # dob = wait_xpath(self.driver, '//*[@text="Date of Birth"]') ; dob.click()
        # wait_xpath(self.driver, '//*[@text="OK"]').click()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Date of Birth*"]'), wait_xpath(self.driver, "//*[@text='Personal Details']"))
        # endregion Personal Details

        wait_xpath(self.driver, '//*[@text="Next"]').click()

        # region Additional Information
        Marital = wait_xpath(self.driver, '(//*[@text="Marital Status"]/../android.view.ViewGroup)[1]') ; Marital.click()
        Single = wait_xpath(self.driver, '//*[@text="Single"]'); Single.click()

        Education = wait_xpath(self.driver, '(//*[@text="Highest Education"]/../android.view.ViewGroup)[1]') ; Education.click()
        Professional = wait_xpath(self.driver, '//*[@text="Professional Qualification"]'); Professional.click()

        Dependents = wait_xpath(self.driver, '(//*[@text="No. of Dependents"]/../android.view.ViewGroup)[1]') ; Dependents.click()
        wait_xpath(self.driver, '//*[@text="3"]').click()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="No. of Dependents"]'), wait_xpath(self.driver, "//*[@text='Additional Information']"))

        address = wait_xpath(self.driver, '//*[@text="Block Number and Street Name"]/../android.widget.EditText')
        address.send_keys('123 street')

        Unit = wait_xpath(self.driver, '//*[@text="Unit Number"]/../android.widget.EditText')
        Unit.send_keys('unit')

        Apartment = wait_xpath(self.driver, '//*[@text="Name of Apartment (if any)"]/../android.widget.EditText')
        Apartment.send_keys('Apartment')

        Postal = wait_xpath(self.driver, '//*[@text="Postal Code*"]/../android.widget.EditText')
        Postal.send_keys('123456')

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Unit Number"]'), wait_xpath(self.driver, "//*[@text='Additional Information']"))

        Residential = wait_xpath(self.driver, '(//*[@text="Residential Type*"]/../android.view.ViewGroup)[1]') ; Residential.click()
        Public_Rental = wait_xpath(self.driver, '//*[@text="HDB Public Rental Scheme"]'); Public_Rental.click()

        Residential_Status = wait_xpath(self.driver, '(//*[@text="Residential Status*"]/../android.view.ViewGroup)[1]') ; Residential_Status.click()
        Rented = wait_xpath(self.driver, '//*[@text="Rented"]'); Rented.click()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Residential Status*"]'), wait_xpath(self.driver, "//*[@text='Additional Information']"))

        Length_of_Stay = wait_xpath(self.driver, '//*[@text="Length of Stay at Current Residence (years)"]/../android.widget.EditText')
        Length_of_Stay.send_keys('123')

        wait_xpath(self.driver, '//*[@text="Yes"]').click()
        # endregion Additional Information

        wait_xpath(self.driver, '//*[@text="Next"]').click()

        # region Employment Details
        AMI = wait_xpath(self.driver, '//*[@text="Average Monthly Income for Past 3 Months*"]/../android.widget.EditText')
        AMI.send_keys('5000')

        Primary = wait_xpath(self.driver, '(//*[@text="Current Primary Employment Status*"]/../android.view.ViewGroup)[1]') ; Primary.click()
        salary = wait_xpath(self.driver, '//*[@text="Employed-salary"]'); salary.click()

        Job_Type = wait_xpath(self.driver, '(//*[@text="Job Type"]/../android.view.ViewGroup)[1]') ; Job_Type.click()
        Director = wait_xpath(self.driver, '//*[@text="Director"]'); Director.click()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Job Type"]'), wait_xpath(self.driver, "//*[@text='Employment Details']"))

        Job_Industry = wait_xpath(self.driver, '(//*[@text="Job Industry*"]/../android.view.ViewGroup)[1]') ; Job_Industry.click()
        Healthcare = wait_xpath(self.driver, '//*[@text="Healthcare"]'); Healthcare.click()

        Company = wait_xpath(self.driver, '//*[@text="Company Name"]/../android.widget.EditText')
        Company.send_keys('Company Name')

        time_cc = wait_xpath(self.driver, '(//*[@text="Time with Current Company*"]/../android.view.ViewGroup)[1]') ; time_cc.click()
        y = wait_xpath(self.driver, '//*[@text="1 - 3 years"]'); y.click()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Company Name"]'), wait_xpath(self.driver, "//*[@text='Employment Details']"))

        Prior_Company = wait_xpath(self.driver, '//*[@text="Prior Company Name"]/../android.widget.EditText')
        Prior_Company.send_keys('Prior Company Name')

        time_pc = wait_xpath(self.driver, '(//*[@text="Time with Prior Company"]/../android.view.ViewGroup)[1]') ; time_pc.click()
        y = wait_xpath(self.driver, '//*[@text="1 - 3 years"]'); y.click()
        # endregion Employment Details

        wait_xpath(self.driver, '//*[@text="Next"]').click()

        # region Loan Details
        Loan_Amount = wait_xpath(self.driver, '//*[@text="Expected Loan Amount (SGD)*"]/../android.widget.EditText')
        Loan_Amount.send_keys('5000')

        Loan_Expected = wait_xpath(self.driver, '//*[@text="Expected Loan Tenure (Months)*"]/../android.widget.EditText')
        Loan_Expected.send_keys('5000')

        Purpose = wait_xpath(self.driver, '(//*[@text="Purpose of Loan*"]/../android.view.ViewGroup)[1]') ; Purpose.click()
        Home = wait_xpath(self.driver, '//*[@text="Home"]'); Home.click()
        # endregion Loan Details

        wait_xpath(self.driver, '//*[@text="Next"]').click()

        # region Financial Obligations
        Total_Debt = wait_xpath(self.driver, '//*[@text="Total Debt Obligations (SGD)"]/../android.widget.EditText')
        Total_Debt.send_keys('5000')

        Monthly_Repayments = wait_xpath(self.driver, '//*[@text="Monthly Repayments to Banks (SGD)*"]/../android.widget.EditText')
        Monthly_Repayments.send_keys('5000')

        Loans_no = wait_xpath(self.driver, '//*[@text="No. of Loans with Moneylenders"]/../android.widget.EditText')
        Loans_no.send_keys('5')

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="No. of Loans with Moneylenders"]'), wait_xpath(self.driver, "//*[@text='Financial Obligations']"))

        Moneylenders = wait_xpath(self.driver, '//*[@text="Monthly Repayments to Moneylenders (SGD)*"]/../android.widget.EditText')
        Moneylenders.send_keys('5000')
        # endregion Financial Obligations

        wait_xpath(self.driver, '//*[@text="Next"]').click()

        # region Document Uploads
        wait_xpath(self.driver, '//*[@text="Allow"]').click()
        wait_xpath(self.driver, "(//android.widget.ScrollView//android.widget.ImageView)[1]").click()
        wait_xpath(self.driver, "(//android.widget.ScrollView//android.widget.ImageView)[2]").click()
        wait_xpath(self.driver, "(//android.widget.ScrollView//android.widget.ImageView)[3]").click()
        # endregion Document Uploads

        wait_xpath(self.driver, '//*[@text="Next"]').click()
        wait_xpath(self.driver, '//*[@text="Submit"]').click()

        success_msg = wait_xpath(self.driver, '//*[@text="Thank you for submitting!"]').is_displayed()
        assert success_msg is True
