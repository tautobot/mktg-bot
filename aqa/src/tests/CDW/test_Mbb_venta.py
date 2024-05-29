import datetime
from random import choice
from time import sleep

import pytest
from selenium.webdriver.common.by import By

from aqa.src.tests.base import BaseTest
from aqa.utils.generic import generate_nricfin, write_to_file, generate_mobile_sgd
from aqa.utils.webdriver_util import wait_xpath, wait_name, isDisplayed_xpath, wait_id

mbb_url                 = 'https://cdg-release.gigacover.com/mbb'
mbb_claim_url           = 'https://cdg-release.gigacover.com/partners/comfort-mbb/claim'


class Test(BaseTest):


    def test_buy_mbb(self):
        self.driver.get(mbb_url)
        wait_xpath(self.driver, "//*[(text()='BUY MBB NOW')]").click()

        first_name = wait_name(self.driver, "first_name")
        first_name.send_keys('aQA')

        last_name = wait_name(self.driver, "last_name")
        last_name.send_keys('Mbb')

        nric = generate_nricfin()
        write_to_file(nric, '/tmp/aqa/mbb_nricfin')
        nricfin = wait_name(self.driver, "nricfin")
        nricfin.send_keys(nric)

        vehicle_reg = wait_name(self.driver, "vehicle_reg")
        vehicle_reg.send_keys('Some Vehicle')

        birth_day = wait_xpath(self.driver, '//*[text()="Birthday"]/..//input')
        birth_day.click()
        test = self.driver.find_elements(By.XPATH, '//*[contains(@class,"DayPickerInput-OverlayWrapper")]//*[(@class="DayPicker-Day")]')
        test[0].click()
        # self.driver.execute_script("arguments[0].setAttribute('value','01 Jan 1990')", birth_day)

        date = datetime.date.today() + datetime.timedelta(2)
        d = date.strftime("%d %b %Y")
        policy_start = wait_xpath(self.driver, '//*[text()="Policy Start"]/..//input')
        policy_start.click()
        test = self.driver.find_elements(By.XPATH, '//div[contains(@class,"DayPickerInput-OverlayWrapper")]//*[contains(@class,"DayPicker-Day--today")]')
        test[0].click()
        # self.driver.execute_script(f"arguments[0].setAttribute('value','{d}')", policy_start)

        email = wait_name(self.driver, 'email')
        email.send_keys(f'{nric}@gigacover.com')

        wait_xpath(self.driver, '//*[@name="gender"]').click()
        gender_list = ['Male', 'Female']
        a = choice(gender_list)
        gender = wait_xpath(self.driver, f'//option[text()="{a}"]')
        gender.click()

        postal_code = wait_name(self.driver, 'postalcode')
        postal_code.send_keys('123456')

        wait_xpath(self.driver, '//*[@name="taxi_company"]').click()
        company_list = ['Comfort Taxi', 'CityCab']
        c = choice(company_list)
        company = wait_xpath(self.driver, f'//option[text()="{c}"]')
        company.click()

        mobile = wait_name(self.driver, "mobile")
        mobile.send_keys(generate_mobile_sgd())

        check_box = self.driver.find_elements(By.XPATH, '//*[@type="checkbox"]')
        for i in check_box:  # click all check box
            i.click()

        checkout_btn = wait_xpath(self.driver, '//*[text()="CHECKOUT NOW"]')
        checkout_btn.click()

        Total_premium = wait_xpath(self.driver, '//*[text()="Total Annual Payable"]/../following-sibling::div').text
        assert Total_premium == '$212.93'

        pay = wait_xpath(self.driver, '//*[text()="PAY SECURELY NOW"]')
        pay.click()

        checkout(self.driver)
        sleep(15)
        assert isDisplayed_xpath(self.driver, '//*[text()="Congratulations"]') is True

    def test_claim_mbb(self):
        nric = generate_nricfin()
        p_number = buy_mbb_from_API(nric)
        if p_number == False:
            pytest.fail('Can not buy mbb form API')

        self.driver.get(mbb_claim_url)

        claimant_name_policy = wait_id(self.driver, 'claimant_name_policy')
        claimant_name_policy.send_keys('aqa mbb')

        policy_number = wait_id(self.driver, 'policy_number')
        policy_number.send_keys(p_number)

        claimant_name = wait_id(self.driver, 'claimant_name')
        claimant_name.send_keys('aqa mbb')

        nricfin = wait_id(self.driver, 'nricfin')
        nricfin.send_keys(nric)

        email = wait_id(self.driver, 'email')
        email.send_keys(f'{nric}@gigacover.com')

        mobile = wait_id(self.driver, 'mobile')
        mobile.send_keys(generate_mobile_sgd())

        vehicle_reg = wait_id(self.driver, 'vehicle_reg')
        vehicle_reg.send_keys(nric)

        rental_company = wait_id(self.driver, 'claimant_name_details')
        rental_company.send_keys('Gigacover')

        doa = wait_xpath(self.driver, '//input[@placeholder="Date of Accident"]/..')
        doa.click()
        wait_xpath(self.driver, '//*[text()="OK"]').click()

        section1excess = wait_id(self.driver, 'section1excess')
        section1excess.send_keys('2000')

        section2excess = wait_id(self.driver, 'section2excess')
        section2excess.send_keys('3000')

        list = [0, 1]
        b = choice(list)
        wait_xpath(self.driver, f'//*[@name="claimant_have_paid_excess_payable" and @value="{b}"]/..').click()

        wait_xpath(self.driver, f'//*[text()="I hereby declare that I have read and agreed to the above."]').click()

        id_photos = self.driver.find_elements_by_id('id_photos')
        id_photos[0].send_keys(f'{fixture_dir}/1.jpg')
        id_photos[0].send_keys(f'{fixture_dir}/2.jpg')

        photos = self.driver.find_elements_by_id('photos')
        photos[0].send_keys(f'{fixture_dir}/3.jpg')
        photos[0].send_keys(f'{fixture_dir}/4.jpg')

        wait_xpath(self.driver, '//*[text()="NEXT"]').click()

        bank_name = wait_id(self.driver, 'bank_name')
        bank_name.send_keys('Name of Bank')

        bank_account_holder_name = wait_id(self.driver, 'bank_account_holder_name')
        bank_account_holder_name.send_keys('Name of Bank Account holder')

        bank_account_number = wait_id(self.driver, 'bank_account_number')
        bank_account_number.send_keys('Bank Account Number')

        wait_xpath(self.driver, '//*[text()="SUBMIT"]').click()

        sleep(15)
        success_msg = isDisplayed_xpath(self.driver, '//*[@class="success-content"]')
        assert success_msg is True

