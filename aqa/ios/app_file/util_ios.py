from datetime import datetime
from time import sleep
import os

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy


filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))

def wait_xpath(driver, xpath):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))

def wait_accessibility_id(driver, id):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, id)))

def wait_xpath_click(driver,xpath):
    return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))

def read_file(path):
    with open(path, "r") as file:
        return file.read()

def write_to_file(name, path):
    with open(path, "w") as file:
        file.write(name)

def isDisplayed_xpath(driver, xpath):
    try:
        wait_xpath(driver, xpath)
    except NoSuchElementException:
        return False
    return True

def isDisplayed_id(driver, id):
    try:
        wait_accessibility_id(driver, id)
    except NoSuchElementException:
        return False
    return True

def wait():
    sleep(3)

def human_wise():
    sleep(10)

def login_pouch_ios(driver, email, pwd):
    allow_btn = wait_xpath(driver, '//XCUIElementTypeButton[@name="Allow"]')
    if allow_btn.is_displayed():
        allow_btn.click()

    check = wait_xpath(driver, '//*[@name="LoginUsernameInput"]')
    while check.is_displayed():
        flag = check.is_displayed()
        if flag:
            break

    driver.scroll(wait_xpath(driver, '//*[@name="LoginUsernameInput"]'), wait_xpath(driver, '//*[@name="LoginNextButton"]'))

    email_box = wait_xpath(driver, '//*[@name="LoginUsernameInput"]')
    email_box.send_keys(email)

    next_btn = wait_accessibility_id(driver, 'Next:')
    next_btn.click()

    next_btn = wait_xpath(driver, '//*[@name="LoginNextButton"]')
    next_btn.click()

    pass_box = wait_xpath(driver, '//*[@name="LoginPasswordInput"]')
    pass_box.send_keys(pwd)

    next_btn = wait_xpath(driver, '//XCUIElementTypeOther[@name="LoginButton"]')
    next_btn.click()

def login_pocket_ios(driver, email, pwd):
    try:
        allow_btn = wait_xpath(driver, '//XCUIElementTypeButton[@name="Allow"]')
        if allow_btn.is_displayed():
            allow_btn.click()
    except: pass

    check = wait_xpath(driver, '//*[@name="LoginUsernameInput"]')
    while check.is_displayed():
        flag = check.is_displayed()
        if flag:
            break

    driver.scroll(wait_xpath(driver, '//*[@name="LoginUsernameInput"]'), wait_xpath(driver, '//*[@name="LoginNextButton"]'))

    email_box = wait_xpath(driver, '//*[@name="LoginUsernameInput"]')
    email_box.send_keys(email)

    next_btn = wait_accessibility_id(driver, 'Next:')
    next_btn.click()

    next_btn = wait_xpath(driver, '//*[@name="LoginNextButton"]')
    next_btn.click()

    pass_box = wait_xpath(driver, '//*[@name="LoginPasswordInput"]')
    pass_box.send_keys(pwd)

    next_btn = wait_xpath(driver, '//XCUIElementTypeOther[@name="LoginButton"]')
    next_btn.click()

def tutorial_welcome(driver):
    wait_accessibility_id(driver, 'WelcomeBtStart').click()
    wait_accessibility_id(driver, 'WelcomeBtNEXT').click()
    wait_accessibility_id(driver, 'WelcomeBtDONE').click()

def tutorial_essential(driver):
    wait_xpath(driver, '(//XCUIElementTypeOther[@name="SKIP"])[2]').click()
    wait_accessibility_id(driver, 'WelcomeBtDONE').click()
    wait_xpath(driver, '(//XCUIElementTypeOther[@name="GOT IT"])[2]').click()

def active_E_Card(driver, screen='clinic screen'):
    if screen == 'home screen':
        wait_accessibility_id(driver, 'ADD PAYMENT METHOD').click()
    if screen == 'clinic screen':
        medical_card = wait_accessibility_id(driver, 'Medical Card')
        medical_card.click()

        wait_accessibility_id(driver, 'ADD').click()

    card_number = wait_accessibility_id(driver, 'WelcomeInputCardNumber')
    card_number.send_keys('4242 4242 4242 4242')

    exp_date = wait_accessibility_id(driver, 'WelcomeInputCardDate')
    exp_date.send_keys('11 22')

    cvc = wait_accessibility_id(driver, 'WelcomeInputCardCVC')
    cvc.send_keys('333')

    wait_xpath(driver,'//XCUIElementTypeStaticText[@name="Your card may be charged if your bill is not covered by your sponsor."]').click()

    addcard_btn = wait_accessibility_id(driver, 'WelcomeInputCardSave')
    addcard_btn.click()

    wait_accessibility_id(driver, 'OK').click()

    if screen == 'clinic screen':
        wait_accessibility_id(driver, 'GOT IT').click()

def claim(driver, product_name):
    if product_name == 'FLIP': product_name = 'Freelancer\nIncome\nProtection (FLIP)'
    if product_name == 'FLEP': product_name = 'Freelancer\nEarnings\nProtection (FLEP)'

    wait_xpath(driver, '//*[@name="Claims"]').click()

    wait_accessibility_id(driver, f'{product_name}').click()

    date =  wait_accessibility_id(driver, 'Incident date: \nDate of accident or first date \nyou saw a doctor for your illness')
    date.click()

    wait_accessibility_id(driver, 'Confirm').click()

    wait_xpath(driver, '//*[@name="Description:\nPlease be as detailed as possible to facilitate claims processing"]').send_keys('test')

    wait_xpath(driver, '(//*[@name=\"Name of Doctor\"])[1]').send_keys('test')

    wait_accessibility_id(driver, 'Return').click()

    wait_xpath(driver, '(//*[@name=\"Address of clinic\"])[1]').send_keys('test')

    #TODO can't click on element
    wait_accessibility_id(driver, 'Tell us about your injury / illness').click()

    driver.scroll(wait_xpath(driver, '//*[@name="Which doctor / clinic did you visit for your first consultation regarding this injury / illness?"]'), wait_xpath(driver, '//*[@name="Tell us about your injury / illness"]'))

    wait_xpath(driver, '(//*[@name=\"Name of Doctor\"])[2]').send_keys('test')

    wait_accessibility_id(driver, 'Return').click()

    wait_xpath(driver, '(//*[@name=\"Address of clinic\"])[2]').send_keys('test')

    wait_accessibility_id(driver, 'Which doctor / clinic do you usually visit?').click()

    wait_xpath(driver, '(//*[@name="Next"])[1]').click()

    wait_xpath(driver, '(//*[@name="I Understand"])[2]').click()

    wait_xpath(driver, '(//*[@name="Next"])[2]').click()

    wait_xpath(driver, '//*[@name="Allow Access to All Photos"]').click()

    picture1 = wait_xpath(driver, '//XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]')
    picture1.click()

    picture2 = wait_xpath(driver, '//XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]')
    picture2.click()

    wait_xpath(driver, '(//*[@name="Next"])[2]').click()

    wait()
    wait_xpath(driver, '(//*[@name="Next"])[2]').click()

    wait()
    picture4 = wait_xpath(driver, '//XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]')
    picture4.click()

    picture5 = wait_xpath(driver, '//XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]')
    picture5.click()

    picture6 = wait_xpath(driver, '//XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeOther[3]')
    picture6.click()

    wait_xpath(driver, '(//*[@name="Next"])[2]').click()

    wait_xpath(driver, "//*[@name='NRIC/FIN/UEN  ']").send_keys('1234')

    wait_xpath(driver, '//XCUIElementTypeOther[@name="Please add bank account to complete claim"]').click()

    wait_xpath(driver, "//*[@name='Name of Bank  ']").send_keys('some bank')

    wait_xpath(driver, '//XCUIElementTypeOther[@name="Please add bank account to complete claim"]').click()

    wait_xpath(driver, "//*[@name='Name of Bank Account Holder  ']").send_keys('some name')

    wait_xpath(driver, '//XCUIElementTypeOther[@name="Please add bank account to complete claim"]').click()

    #TODO can't sendkeys
    wait_xpath(driver, "//*[@name='Bank Account Number  ']").send_keys('DE89370400440532013000')

    wait_accessibility_id(driver, 'Next:').click()

    wait_xpath(driver, "//*[@name='SAVE']").click()

    wait_xpath(driver, "//*[@name='OK']").click()

    wait()
    wait_xpath(driver, "//*[@name='CONFIRM']").click()

    wait()
    wait_xpath(driver, '//XCUIElementTypeButton[@name="Submit"]').click()

    wait()
    wait_xpath(driver, '//*[@name="Claim successfully submitted!"]').is_displayed()

    wait_xpath(driver, '(//*[@name="Back To Home"])[2]').click()

def verify_can_claim(driver, email, pwd, product_name):
    if product_name == 'FLIP': product_name = 'Freelancer\nIncome\nProtection (FLIP)'
    if product_name == 'FLEP': product_name = 'Freelancer\nEarnings\nProtection (FLEP)'

    login_pouch_ios(driver, email, pwd)
    wait()
    wait_xpath(driver, '//*[@name="Claims"]').click()
    claim_btn = wait_accessibility_id(driver, f'{product_name}')
    assert claim_btn.is_displayed() is True

def verify_past_claim(driver, product_name):
    if product_name == 'FLIP': product_name = 'Freelancer\nIncome\nProtection (FLIP)'
    if product_name == 'FLEP': product_name = 'Freelancer\nEarnings\nProtection (FLEP)'

    wait_xpath(driver, '//*[@name="Claims"]').click()

    wait_accessibility_id(driver, f'{product_name}').click()

    wait_xpath(driver, '//*[@name="View Past Claims"]').click()

    today = datetime.today().strftime("%d %b %Y")

    assert wait_xpath(driver, f'//*[@name="#1 PROCESSING dd Pay out $0 {today}"]').is_displayed() is True

    wait_xpath(driver, '//XCUIElementTypeScrollView/XCUIElementTypeOther[1]').click()

    description = wait_xpath(driver, '//*[@name="Description test"]/XCUIElementTypeStaticText[2]').text
    name_of_doctor = wait_xpath(driver, '//*[@name="Name of Doctor test"]/XCUIElementTypeStaticText[2]').text
    address = wait_xpath(driver, '//*[@name="Address test"]/XCUIElementTypeStaticText[2]').text

    assert description == name_of_doctor == address == 'test'

    picture = wait_xpath(driver, '//XCUIElementTypeOther[@name="1 2 3 4 5"]')
    assert picture.is_displayed() is True

