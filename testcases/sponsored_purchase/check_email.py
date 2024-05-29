import sys
from selenium.webdriver.common.action_chains import ActionChains
from config_local import *

filepath = os.path.dirname(__file__)
sys.path.append(filepath)
driver = wd()
existing_policies = read_file(f'{filepath}/testfiles/email_existing_data'.split('\n'))


def check_policy_schedule_email(product):
    wait()
    if product == 'flep':
        email_title = wait_xpath(driver, '(//span[contains(text(),"Information on your Freelancer Earnings Protection Policy, sponsored by GOJEK GOALBETTER")])[last()]')
    elif product == 'flip':
        email_title = wait_xpath(driver, '(//span[contains(text(),"Information on your Freelancer Income Protection Policy, sponsored by GOJEK GOALBETTER")])[last()]')
    elif product == 'pa':
        email_title = wait_xpath(driver, '(//span[contains(text(),"Information on your Personal Accident Protection Policy, sponsored by GIS")])[last()]')
    else:
        email_title = ''
    email_title.click()

    wait()
    move = wait_xpath(driver, "//*[contains(text(), 'DAILY CASH BENEFIT')]")
    driver.execute_script("arguments[0].scrollIntoView();", move)
    ActionChains(driver).move_to_element(move)

    wait()
    actual_policy_number = driver.find_element_by_css_selector('[id$=policy_number]').text
    actual_daily_cash_benefit = driver.find_element_by_css_selector('[id$=daily_cash_benefit]').text
    actual_policy_start = driver.find_element_by_css_selector('[id$=policy_start]').text
    actual_policy_end = driver.find_element_by_css_selector('[id$=policy_end]').text
    # amount_paid = wait_xpath(driver, '//*[text()="AMOUNT PAID"]/../b[6]').text

    if (actual_policy_number == policy_number and actual_policy_start == start_date):
        if product == 'flep' and actual_daily_cash_benefit == "$80":
            print('PASS')
        elif product == 'flip' and actual_daily_cash_benefit == "$50":
            print('PASS')
        elif product == 'pa' and actual_daily_cash_benefit == "$50000":
            print('PASS')
        else:
            print(f'Product {product} is not existing')
    else:
        print('FAIL')

    file = driver.find_element_by_xpath(f'//a[contains(@href,"{policy_number}")]')
    driver.get(file.get_attribute('href'))
    sleep(5)


def check_email():
    login_gmail(options(), driver, email, password)
    search_email(driver, email_to_search)
    check_policy_schedule_email(product)
    driver.quit()


for line in existing_policies:
    data = line.split(':')[1].split(',')
    policy_number = data[0]
    product = data[1]
    nricfin = data[2]
    email_to_search = f'{email_prefix}+{nricfin.lower()}@gigacover.com'
    start_date = data[3]
    status = data[4]
    check_email()

