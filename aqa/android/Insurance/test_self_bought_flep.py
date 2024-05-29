import unittest
import datetime
from random import choice

from testcases.lib.generic import generate_nricfin
from aQA.venta.util import wait_xpath, input_information, wait_id, checkout, verify_success, wait, wait_name
from aQA.webdriver.selenium_webdriver import *
from config_local import *
from pathlib import Path

Path("/tmp/aqa").mkdir(parents=True, exist_ok=True)

def cal_year(age):
    now = datetime.datetime.now()
    year = now.year - age
    return year

def buying_flep_indoor(driver):
    data = {}
    url = f'http://{ip_docker}:21263/' if environment == 'docker' else 'https://app-release.gigacover.com/'

    driver.get(url)
    wait_xpath(driver, '//*[text()="Get Quote Now"]').click()
    wait_xpath(driver, '//*[text()="FLEP"]').click()

    wait()
    wait_xpath(driver, '//*[text()="No, I don’t"]').click()
    wait_xpath(driver, '//*[text()="NEXT"]').click()

    wait()
    wait_xpath(driver, '//*[text()="Indoor "]').click()
    wait_xpath(driver, '//*[text()="NEXT"]').click()

    transport_list = ['Public Transport (MRT / Bus)', 'Car / Taxi', 'Motorcycle', 'Others:']
    transport = choice(transport_list)
    wait_xpath(driver, f'//*[text()="{transport}"]').click()
    if transport == 'Others:':
        wait_name(driver, 'transport_vehicle_detail').send_keys('walk')
    wait_xpath(driver, '//*[text()="NEXT"]').click()

    wait()
    birth_day = wait_xpath(driver, '//*[text()="What is your date of birth?"]/../..//input')
    driver.execute_script("arguments[0].removeAttribute('disabled')", birth_day)
    birth_day.clear()
    birth_day.send_keys('01 Jan 1993')

    wait_xpath(driver, '//*[text()="NEXT"]').click()

    wait()
    policy_start = wait_xpath(driver, '//*[@class="date-picker-wrapper"]//button')
    policy_start.click()
    wait_xpath(driver, '//*[text()="OK"]').click()
    wait_xpath(driver, '//*[@type="checkbox"]/..').click()
    wait_xpath(driver, '//*[text()="NEXT"]').click()

    wait()
    nric = generate_nricfin()
    email = f'{nric}@gigacover.com'
    input_information(driver, 'trang', 'truong', nric, email)

    pay_btn = wait_xpath(driver, '//*[text()="PAY SECURELY NOW"]')
    pay_btn.click()

    wait()
    total_amount = wait_xpath(driver, '//*[text()="Final Amount Due:"]/following-sibling::div').text
    data['total_amount'] = total_amount

    unit = wait_xpath(driver,'//*[text()="Renewal:"]/following-sibling::span').text
    data['unit'] = unit

    daily_benefit = wait_xpath(driver,'//*[text()="Cash Benefit:"]/following-sibling::span').text
    data['daily_benefit'] = daily_benefit

    wait()
    pay_btn = wait_xpath(driver, '//*[text()="PAY SECURELY NOW"]')
    pay_btn.click()

    checkout(driver)
    verify_success(driver)
    return data


def buying_flep_outdoor(driver):
    data = {}
    url = f'http://{ip_docker}:21263/' if environment == 'docker' else 'https://app-release.gigacover.com/'

    driver.get(url)
    wait_xpath(driver, '//*[text()="Get Quote Now"]').click()
    wait_xpath(driver, '//*[text()="FLEP"]').click()

    wait()
    wait_xpath(driver, '//*[text()="No, I don’t"]').click()
    wait_xpath(driver, '//*[text()="NEXT"]').click()

    wait()
    wait_xpath(driver, '//*[text()="Outdoor "]').click()
    occupation_list = ['Private Hire Driver', 'Food / Logistic Delivery', 'Food Hawker', 'Cleaner / Handyman', 'Salesperson', 'Fitness Coach', 'Photographer / Film Professional', 'Others:']
    occupation = choice(occupation_list)
    wait_xpath(driver, f'//*[text()="{occupation}"]').click()

    if occupation == 'Others:': wait_name(driver, 'occupation_detail').send_keys('Teacher')

    if occupation == 'Food / Logistic Delivery':
        transport_list = ['Walk', 'Bicycle / PMD', 'Motorcycle', 'Car / Van', 'Others:']
        transport = choice(transport_list)
        wait_xpath(driver, f'//*[text()="{transport}"]').click()
        if transport == 'Others:':
            wait_name(driver, 'transport_mode_detail').send_keys('Grab')

    wait_xpath(driver, '//*[text()="NEXT"]').click()

    wait()
    transport_list = ['Public Transport (MRT / Bus)', 'Car / Taxi', 'Motorcycle', 'Others:']
    transport = choice(transport_list)
    wait_xpath(driver, f'//*[text()="{transport}"]').click()
    if transport == 'Others:':
        wait_name(driver, 'transport_vehicle_detail').send_keys('walk')
    wait_xpath(driver, '//*[text()="NEXT"]').click()


    birth_day = wait_xpath(driver, '//*[text()="What is your date of birth?"]/../..//input')
    driver.execute_script("arguments[0].removeAttribute('disabled')", birth_day)
    birth_day.clear()
    birth_day.send_keys('01 Jan 1993')

    wait_xpath(driver, '//*[text()="NEXT"]').click()

    wait()
    policy_start = wait_xpath(driver, '//*[@class="date-picker-wrapper"]//button')
    policy_start.click()
    wait_xpath(driver, '//*[text()="OK"]').click()
    wait_xpath(driver, '//*[@type="checkbox"]/..').click()
    wait_xpath(driver, '//*[text()="NEXT"]').click()

    wait()
    nric = generate_nricfin()
    email = f'{nric}@gigacover.com'
    input_information(driver, 'trang', 'truong', nric, email)

    pay_btn = wait_xpath(driver, '//*[text()="PAY SECURELY NOW"]')
    pay_btn.click()

    wait()
    total_amount = wait_xpath(driver, '//*[text()="Final Amount Due:"]/following-sibling::spanx').text
    data['total_amount'] = total_amount

    unit = wait_xpath(driver,'//*[text()="Renewal:"]/following-sibling::span').text
    data['unit'] = unit

    daily_benefit = wait_xpath(driver,'//*[text()="Cash Benefit:"]/following-sibling::span').text
    data['daily_benefit'] = daily_benefit

    wait()
    pay_btn = wait_xpath(driver, '//*[text()="PAY SECURELY NOW"]')
    pay_btn.click()

    checkout(driver)
    verify_success(driver)
    return data


def buying_flep_gojek(driver, range):
    data = {}
    url = f'http://{ip_docker}:21263/' if environment == 'docker' else 'https://app-release.gigacover.com/'

    driver.get(url)
    wait_xpath(driver, '//*[text()="Get Quote Now"]').click()
    wait_xpath(driver, '//*[text()="FLEP"]').click()

    wait()
    wait_xpath(driver, '(//*[@aria-label="company-selection"]/label/span)[1]').click()
    wait_xpath(driver, '//*[text()="NEXT"]').click()

    birth_day = wait_xpath(driver, '//*[text()="What is your date of birth?"]/../..//input')
    driver.execute_script("arguments[0].removeAttribute('disabled')", birth_day)
    birth_day.clear()
    birth_day.send_keys(range)

    wait_xpath(driver, '//*[text()="NEXT"]').click()
    wait()

    policy_start = wait_xpath(driver, '//*[@class="date-picker-wrapper"]//button')
    policy_start.click()
    wait_xpath(driver, '//*[text()="OK"]').click()
    wait_xpath(driver, '//*[@type="checkbox"]/..').click()
    wait_xpath(driver, '//*[text()="NEXT"]').click()
    wait()

    nric = generate_nricfin()
    email = f'{nric}@gigacover.com'
    input_information(driver, 'trang', 'truong', nric, email)

    pay_btn = wait_xpath(driver, '//*[text()="PAY SECURELY NOW"]')
    pay_btn.click()

    wait()
    total_amount = wait_xpath(driver, '//*[text()="Total Amount:"]/following-sibling::span').text
    data['total_amount'] = total_amount

    unit = wait_xpath(driver,'//*[text()="Renewal:"]/following-sibling::span').text
    data['unit'] = unit

    daily_benefit = wait_xpath(driver,'//*[text()="Cash Benefit:"]/following-sibling::span').text
    data['daily_benefit'] = daily_benefit

    wait()
    pay_btn = wait_xpath(driver, '//*[text()="PAY SECURELY NOW"]')
    pay_btn.click()

    checkout(driver)
    verify_success(driver)
    return data


class Test(unittest.TestCase):


    def setUp(self):
        self.driver = webdriver_local() if dri == 'local' else webdriver_docker()


    def tearDown(self):
        self.driver.quit()


    def test_flep_range1(self):
        year = cal_year(20)
        actual_output = buying_flep_gojek(self.driver, range=f'01 Jan {year}')
        assert actual_output['total_amount'] == '$19.20'

    def test_flep_range2(self):
        year = cal_year(42)
        actual_output = buying_flep_gojek(self.driver, range=f'01 Jan {year}')
        assert actual_output['total_amount'] == '$19.20'

    def test_flep_range3(self):
        year = cal_year(47)
        actual_output = buying_flep_gojek(self.driver, range=f'01 Jan {year}')
        assert actual_output['total_amount'] == '$19.20'

    def test_flep_range4(self):
        year = cal_year(52)
        actual_output = buying_flep_gojek(self.driver, range=f'01 Jan {year}')
        assert actual_output['total_amount'] == '$19.20'

    def test_flep_range5(self):
        year = cal_year(57)
        actual_output = buying_flep_gojek(self.driver, range=f'01 Jan {year}')
        assert actual_output['total_amount'] == '$19.20'

    def test_flep_range6(self):
        year = cal_year(62)
        actual_output = buying_flep_gojek(self.driver, range=f'01 Jan {year}')
        assert actual_output['total_amount'] == '$19.20'

    def test_flep_range7(self):
        year = cal_year(67)
        actual_output = buying_flep_gojek(self.driver, range=f'01 Jan {year}')
        assert actual_output['total_amount'] == '$19.20'

    def test_flep_indoor(self):
        buying_flep_indoor(self.driver)

    def test_flep_outdoor(self):
        buying_flep_outdoor(self.driver)
