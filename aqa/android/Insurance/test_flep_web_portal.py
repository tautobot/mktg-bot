import unittest
import os
from time import sleep

from aQA.venta.util import login_web_portal, wait_xpath, isDisplayed_xpath, wait, wait_id
from aQA.webdriver.selenium_webdriver import webdriver_local, webdriver_docker
from config_local import dri
from testcases.lib.generic import read_cell_in_excel_file, generate_mobile_sgd

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))
excel_file = f'{app_path}/fixtures/flep_template.xlsx'


def verify_can_claim(dri, email, pwd):
    login_web_portal(dri, email, pwd)

    gg_protect = wait_xpath(dri, '//*[(text()="GigaProtect")]/..')
    gg_protect.click()

    flep = wait_xpath(dri, '//*[(text()="FLEP")]/..')
    flep.click()

    submit_claim = wait_xpath(dri, '//*[(text()="Submit Claims")]/..')
    submit_claim.click()

    assert isDisplayed_xpath(dri, '//*[(@class="flep-claim-page")]') is True


def flep_claim(dri):
    wait()

    gg_protect = wait_xpath(dri, '//*[(text()="GigaProtect")]/..')
    gg_protect.click()

    flep = wait_xpath(dri, '//*[(text()="FLEP")]/..')
    flep.click()

    submit_claim = wait_xpath(dri, '//*[(text()="Submit Claims")]/..')
    submit_claim.click()

    wait()
    assert isDisplayed_xpath(dri, '//*[(@class="flep-claim-page")]') is True

    wait_xpath(dri, '//*[(text()="NEXT")]').click()

    wait()
    wait_xpath(dri, '//*[(text()="NEXT")]').click()

    start_date = wait_xpath(dri, '//*[(@name="start_date")]/following-sibling::div/button')
    start_date.click()
    wait_xpath(dri, '//*[(text()="OK")]').click()

    end_date = wait_xpath(dri, '//*[(@name="end_date")]/following-sibling::div/button')
    end_date.click()
    wait_xpath(dri, '//*[(text()="OK")]').click()

    incident_date = wait_xpath(dri, '//*[(@name="incident_date")]/following-sibling::div/button')
    incident_date.click()
    wait_xpath(dri, '//*[(text()="OK")]').click()

    des = wait_xpath(dri, '//*[(text()="Description")]/following-sibling::div')
    des.send_keys('Description')

    accident_happen = wait_xpath(dri, '//*[(text()="How did the Accident happen?")]/following-sibling::div')
    accident_happen.send_keys('How did the Accident happen?')

    where_happen = wait_xpath(dri, '//*[(text()="Where did the accident happen?")]/following-sibling::div')
    where_happen.send_keys('Where did the accident happen?')

    m = generate_mobile_sgd()
    mobile = wait_id(dri, 'paynow_mobile')
    mobile.send_keys(m)

    nickname = wait_id(dri, 'paynow_nickname')
    nickname.send_keys('Nickname')

    wait_xpath(dri, '//*[(text()="NEXT")]').click()

    wait()
    id_front = dri.find_elements_by_xpath('//input[@id="id_front"]')
    id_front[0].send_keys(f'{app_path}/fixtures/1.jpg')

    id_back = dri.find_elements_by_xpath('//input[@id="id_back"]')
    id_back[0].send_keys(f'{app_path}/fixtures/2.jpg')

    medical_certificate = dri.find_elements_by_xpath('//input[@id="medical_certificate"]')
    medical_certificate[0].send_keys(f'{app_path}/fixtures/3.jpg')
    medical_certificate[0].send_keys(f'{app_path}/fixtures/4.jpg')
    medical_certificate[0].send_keys(f'{app_path}/fixtures/5.jpg')
    medical_certificate[0].send_keys(f'{app_path}/fixtures/6.jpg')
    medical_certificate[0].send_keys(f'{app_path}/fixtures/7.jpg')

    medical_report = dri.find_elements_by_xpath('//input[@id="medical_report"]')
    medical_report[0].send_keys(f'{app_path}/fixtures/3.jpg')
    medical_report[0].send_keys(f'{app_path}/fixtures/4.jpg')
    medical_report[0].send_keys(f'{app_path}/fixtures/5.jpg')
    medical_report[0].send_keys(f'{app_path}/fixtures/6.jpg')
    medical_report[0].send_keys(f'{app_path}/fixtures/7.jpg')

    police_report = dri.find_elements_by_xpath('//input[@id="police_report"]')
    police_report[0].send_keys(f'{app_path}/fixtures/3.jpg')
    police_report[0].send_keys(f'{app_path}/fixtures/4.jpg')
    police_report[0].send_keys(f'{app_path}/fixtures/5.jpg')
    police_report[0].send_keys(f'{app_path}/fixtures/6.jpg')

    referral_letter = dri.find_elements_by_xpath('//input[@id="referral_letter"]')
    referral_letter[0].send_keys(f'{app_path}/fixtures/3.jpg')
    referral_letter[0].send_keys(f'{app_path}/fixtures/4.jpg')
    referral_letter[0].send_keys(f'{app_path}/fixtures/5.jpg')

    inpatient_discharge_sum = dri.find_elements_by_xpath('//input[@id="inpatient_discharge_sum"]')
    inpatient_discharge_sum[0].send_keys(f'{app_path}/fixtures/3.jpg')
    inpatient_discharge_sum[0].send_keys(f'{app_path}/fixtures/4.jpg')
    inpatient_discharge_sum[0].send_keys(f'{app_path}/fixtures/5.jpg')
    inpatient_discharge_sum[0].send_keys(f'{app_path}/fixtures/6.jpg')
    inpatient_discharge_sum[0].send_keys(f'{app_path}/fixtures/7.jpg')

    operation_record = dri.find_elements_by_xpath('//input[@id="operation_record"]')
    operation_record[0].send_keys(f'{app_path}/fixtures/3.jpg')
    operation_record[0].send_keys(f'{app_path}/fixtures/4.jpg')
    operation_record[0].send_keys(f'{app_path}/fixtures/5.jpg')
    operation_record[0].send_keys(f'{app_path}/fixtures/6.jpg')
    operation_record[0].send_keys(f'{app_path}/fixtures/7.jpg')

    hospital_medical_bill = dri.find_elements_by_xpath('//input[@id="hospital_medical_bill"]')
    hospital_medical_bill[0].send_keys(f'{app_path}/fixtures/3.jpg')
    hospital_medical_bill[0].send_keys(f'{app_path}/fixtures/4.jpg')

    wait_xpath(dri, '//*[(text()="NEXT")]').click()

    checkbox = wait_xpath(dri, '//input[@name="declaration"]/..')
    checkbox.click()

    wait_xpath(dri, '//*[(text()="NEXT")]').click()

    sleep(10)

    assert isDisplayed_xpath(dri, '//*[text()="Thank you!"]') is True


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver_local() if dri == 'local' else webdriver_docker()


    def tearDown(self):
        self.driver.quit()


    def test_flep_claim(self):
        email = read_cell_in_excel_file(excel_file, 'E2')
        pwd = read_cell_in_excel_file(excel_file, 'D2')
        login_web_portal(self.driver, email, pwd)
        flep_claim(self.driver)

    def test_flep_verify_policy_in_force(self):
        email = read_cell_in_excel_file(excel_file, f'E3')
        pwd = read_cell_in_excel_file(excel_file, f'D3')
        verify_can_claim(self.driver, email, pwd)


    def test_flep_verify_policy_expired_inforce(self):
        email = read_cell_in_excel_file(excel_file, f'E4')
        pwd = read_cell_in_excel_file(excel_file, f'D4')
        verify_can_claim(self.driver, email, pwd)


    def test_flep_verify_policy_expired_paid(self):
        email = read_cell_in_excel_file(excel_file, f'E6')
        pwd = read_cell_in_excel_file(excel_file, f'D6')
        verify_can_claim(self.driver, email, pwd)


    def test_flep_verify_policy_expired_inforce_paid(self):
        email = read_cell_in_excel_file(excel_file, f'E8')
        pwd = read_cell_in_excel_file(excel_file, f'D8')
        verify_can_claim(self.driver, email, pwd)


    def test_flep_verify_policy_inforce_paid(self):
        email = read_cell_in_excel_file(excel_file, f'E11')
        pwd = read_cell_in_excel_file(excel_file, f'D11')
        verify_can_claim(self.driver, email, pwd)
