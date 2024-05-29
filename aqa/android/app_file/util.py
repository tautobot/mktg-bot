import json
from random import choice
from time import sleep
import os
import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.extensions.action_helpers import ActionHelpers
from config_local import *
from aqa.utils.generic import change_datetime, generate_nricfin, generate_mobile_sgd

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))

def wait_xpath(driver, xpath, time=10):
    return WebDriverWait(driver, time).until(EC.visibility_of_element_located((By.XPATH, xpath)))

def wait_id(driver, xpath, time=10):
    return WebDriverWait(driver, time).until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, xpath)))

def wait_xpath_click(driver, xpath):
    return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))

def read_file(path):
    with open(path, "r") as file:
        return file.read()

def write_to_file(name, path):
    with open(path, "w") as file:
        file.write(name)

def wait():
    sleep(10)

def login_expo(driver):
    expo = wait_id(driver, "Profile, tab, 3 of 3")
    wait()
    expo.click()

    sign_in = wait_xpath(driver, "//android.widget.TextView[@text='Sign in to your account']")
    sign_in.click()

    username = wait_xpath(driver, "//android.widget.EditText[@text='E-mail or username']")
    username.send_keys('trang.truong@gigacover.com')

    passw = wait_xpath(driver, "//android.widget.EditText[@text='Password']")
    passw.send_keys('Trang1610')

    btn = wait_xpath(driver, "(//android.widget.TextView[@text='Sign In'])[2]")
    btn.click()

    pouch_app = wait_xpath(driver, "//android.widget.TextView[@text='Gigacover']")
    wait()
    pouch_app.click()

def login_pouch(driver, email, pwd):
    sleep(45)
    check = wait_xpath(driver, '//*[@text="Region"]')
    while check.is_displayed():
        driver.scroll(wait_xpath(driver, "//*[@text='Email']"), wait_xpath(driver, "//*[@text='Region']"))
        check.is_displayed()

    if environment == 'docker':
        atlas_port = wait_xpath(driver, "//*[@text='Atlas: ip:port']")
        atlas_port.send_keys('21260')

        wait_id(driver, 'Arrow server, Arrow server').click()
        wait()

    driver.scroll(wait_xpath(driver, "//*[@text='Email']"), wait_xpath(driver, "//*[@text='NEXT']"))

    email_box = wait_xpath(driver, "//*[@text='Email']")
    email_box.send_keys(email)

    next_btn = wait_xpath(driver,"//*[@text='NEXT']")
    next_btn.click()

    pass_box = wait_xpath(driver, "//*[@text='Enter your password']")
    pass_box.send_keys(pwd)

    next_btn = wait_xpath(driver,"//*[@text='NEXT']")
    next_btn.click()

    wait()

def login_pocket(driver, mobile, pwd):
    wait_xpath(driver, "//*[@text='Login']").click()
    if environment == 'docker':
        atlas_port = wait_xpath(driver, "//*[@text='Atlas: ip:port']")
        atlas_port.send_keys('21260')

        wait_id(driver, 'Arrow server').click()
        wait()

    mobile_number = wait_xpath(driver, "//*[@text='Nomor handphone atau email']")
    mobile_number.send_keys(mobile)

    next_btn = wait_xpath(driver,"//*[@text='LANJUT']")
    next_btn.click()

    pass_box = wait_xpath(driver, "//*[@text='Masukkan kata sandi']")
    pass_box.send_keys(pwd)

    next_btn = wait_xpath(driver,"//*[@text='LANJUT']")
    next_btn.click()

    # change language
    wait_xpath(driver, "//*[@text='Profil']").click()
    wait_xpath(driver, "//*[@text='Pengaturan']").click()

    wait_id(driver, 'languageEnglish').click()
    driver.back()
    wait_xpath(driver, "//*[@text='Home']").click()

def check_info_Flep(driver):
    wait()
    chose_product = wait_xpath(driver, "//*[@text='FLEP']")
    chose_product.click()

    current_cash_benefit = wait_xpath(driver, '(//android.widget.TextView[@text="DAILY CASH BENEFIT"])[1]/../android.widget.TextView[2]').text
    current_policy_period = wait_xpath(driver, '(//android.widget.TextView[@text="POLICY PERIOD"])[1]/../android.widget.TextView[4]').text
    current_policy_number = wait_xpath(driver, '(//android.widget.TextView[@text="POLICY NUMBER"])[1]/../android.widget.TextView[6]').text
    current_premium = wait_xpath(driver, '(//android.widget.TextView[@text="PREMIUM"])[1]/../android.widget.TextView[8]').text

    driver.scroll(wait_xpath(driver, '//*[@text="Self-Paid"]'), wait_xpath(driver, "(//*[@text='DAILY CASH BENEFIT'])[1]"))

    policy_start = change_datetime(read_file('/tmp/aqa/policy_start'))
    start_date = wait_xpath(driver, "//android.widget.TextView[@text='FUTURE']/../../../android.widget.TextView[1]").text

    daily_cash_benefit = read_file('/tmp/aqa/daily_benefit').split(' ')[0]
    future_cash_benefit = wait_xpath(driver, '(//android.widget.TextView[@text="DAILY CASH BENEFIT"])[1]/../android.widget.TextView[2]').text
    future_policy_period = wait_xpath(driver, '//android.widget.TextView[@text="POLICY PERIOD"]/../android.widget.TextView[4]').text
    future_policy_number = wait_xpath(driver, '//android.widget.TextView[@text="POLICY NUMBER"]/../android.widget.TextView[6]').text
    future_premium = wait_xpath(driver, '//android.widget.TextView[@text="PREMIUM"]/../android.widget.TextView[8]').text

    if (current_premium and current_cash_benefit and current_policy_period and current_policy_number == '-') and (start_date == policy_start) and (future_cash_benefit == ('$' + daily_cash_benefit)) and (future_policy_period == 'MONTHLY') and ('$' + future_premium == read_file('/tmp/aqa/amount')):
        pass
    else:
        print('FAIL')
        return

def claim(driver):
    driver.push_file(destination_path="/sdcard/Pictures/1.jpg", source_path=f"{app_path}/fixtures/1.jpg")
    driver.push_file(destination_path="/sdcard/Pictures/2.jpg", source_path=f"{app_path}/fixtures/2.jpg")
    driver.push_file(destination_path="/sdcard/Pictures/3.jpg", source_path=f"{app_path}/fixtures/3.jpg")
    driver.push_file(destination_path="/sdcard/Pictures/4.jpg", source_path=f"{app_path}/fixtures/4.jpg")
    driver.push_file(destination_path="/sdcard/Pictures/5.jpg", source_path=f"{app_path}/fixtures/5.jpg")
    driver.push_file(destination_path="/sdcard/Pictures/6.jpg", source_path=f"{app_path}/fixtures/6.jpg")
    driver.push_file(destination_path="/sdcard/Pictures/7.jpg", source_path=f"{app_path}/fixtures/7.jpg")
    driver.push_file(destination_path="/sdcard/Pictures/8.jpg", source_path=f"{app_path}/fixtures/8.jpg")
    driver.push_file(destination_path="/sdcard/Pictures/9.jpg", source_path=f"{app_path}/fixtures/9.jpg")

    wait()
    wait_xpath(driver, '//*[@text="Claims"]').click()

    wait()
    # TouchAction(driver).tap(x=212, y=513).perform()
    ActionHelpers.tap([(100, 20), (100, 60), (100, 100)], 100)

    date = wait_xpath(driver, "//android.widget.TextView[@text='Incident date: \nDate of accident or first date \nyou saw a doctor for your illness']")
    wait()
    date.click()

    wait_xpath(driver, "//*[@text='OK']").click()

    wait_xpath(driver, "//android.widget.EditText[@text='Description:\nPlease be as detailed as possible to facilitate claims processing']").send_keys('test')

    wait_xpath(driver, "//android.widget.EditText[@text='Name of Doctor']").send_keys('test')

    wait_xpath(driver, "//android.widget.EditText[@text='Address of clinic']").send_keys('test')

    driver.scroll(wait_xpath(driver, '//*[@text="Address of clinic"]'), wait_xpath(driver, "//*[@text='Tell us about your injury / illness']"))

    wait_xpath(driver, "//android.widget.EditText[@text='Name of Doctor']").send_keys('test')

    wait_xpath(driver, "//android.widget.EditText[@text='Address of clinic']").send_keys('test')

    driver.scroll(wait_xpath(driver, "//android.widget.TextView[@text='Which doctor / clinic do you usually visit?']"), wait_xpath(driver, '//android.widget.TextView[@text="Claims"]'))

    wait_xpath(driver, "//android.widget.TextView[@text='Yes'][1]").click()

    wait_xpath(driver, "(//android.widget.TextView[@text='No'])[2]").click()

    wait_xpath(driver, "//android.widget.TextView[@text='Next']").click()

    wait_xpath(driver, "//android.widget.TextView[@text='I Understand']").click()

    wait_xpath(driver, "//android.widget.TextView[@text='Next']").click()

    try:
        wait_xpath(driver, "//*[@text='Allow']").click()
    except:
        wait_xpath(driver, "//*[@text='ALLOW']").click()

    wait()
    driver.scroll(wait_xpath(driver, '(//android.widget.ScrollView//android.widget.ImageView)[1]'), wait_xpath(driver, "//*[@text='You may submit a maximum of 2 photos']"))

    picture5 = wait_xpath(driver, "(//android.widget.ScrollView//android.widget.ImageView)[5]")
    picture5.click()

    picture6 = wait_xpath(driver, "(//android.widget.ScrollView//android.widget.ImageView)[6]")
    picture6.click()

    wait()
    wait_xpath(driver, "//android.widget.TextView[@text='Next']").click()

    wait()
    wait_xpath(driver, "//android.widget.TextView[@text='Next']").click()

    wait()
    picture1 = wait_xpath(driver, "(//android.widget.ScrollView//android.widget.ImageView)[1]")
    picture1.click()

    picture2 = wait_xpath(driver, "(//android.widget.ScrollView//android.widget.ImageView)[2]")
    picture2.click()

    picture3= wait_xpath(driver, "(//android.widget.ScrollView//android.widget.ImageView)[3]")
    picture3.click()

    wait()
    wait_xpath(driver, "//android.widget.TextView[@text='Next']").click()

    wait_xpath(driver, "//*[@text='NRIC/FIN/UEN']").send_keys('1234')

    wait_xpath(driver, "//*[@text='Name of Bank']").send_keys('some bank')

    wait_xpath(driver, "//*[@text='Name of Bank Account Holder']").send_keys('some name')

    wait_xpath(driver, "//*[@text='Bank Account Number']").send_keys('DE89370400440532013000')

    wait_xpath(driver, "//*[@text='SAVE']").click()

    wait_xpath(driver, "//*[@text='OK']").click()

    wait()
    wait_xpath(driver, "//android.widget.TextView[@text='CONFIRM']").click()

    wait_xpath(driver, "//*[@text='SUBMIT']").click()
    wait_xpath(driver, '//*[@text="Claim successfully submitted!"]').is_displayed()

    wait_xpath(driver, '//*[@text="Back To Home"]').click()


def verify_can_claim(driver, email, pwd, product_name):
    if product_name == 'FLEP': product_name = 'Freelancer\nEarnings\nProtection'

    login_pouch(driver, email, pwd)
    wait()
    wait_xpath(driver, '//*[@text="Claims"]').click()
    claim_btn = wait_xpath(driver, f'//*[@text="{product_name}"]')
    assert claim_btn.is_displayed() is True


def active_E_Card(driver, screen='clinic screen'):
    if screen == 'home screen':
        wait_xpath(driver, '//*[@text="ADD PAYMENT METHOD"]').click()
    if screen == 'clinic screen':
        medical_card = wait_xpath(driver, "//*[@text='Medical Card']")
        medical_card.click()

        wait_xpath(driver, "//android.widget.TextView[@text='ADD']").click()

    card_number = wait_xpath(driver, "//*[@text='Card number']")
    card_number.send_keys('4242 4242 4242 4242')

    exp_date = wait_xpath(driver, "//*[@text='MM/YY']")
    exp_date.send_keys('11 22')

    cvc = wait_xpath(driver, "//*[@text='CVC']")
    cvc.send_keys('333')

    addcard_btn = wait_xpath(driver, f"//*[@text='Save']")
    addcard_btn.click()

    wait_xpath(driver, f"//*[@text='OK']").click()

    if screen == 'clinic screen':
        wait_xpath(driver, f"//*[@text='GOT IT']").click()

def verify_Ecard(driver, n):
    # region check Ecard 1
    wait()
    name = wait_xpath(driver, '//android.widget.ImageView[1]/../android.widget.TextView[1]').text
    assert name == n

    id = wait_xpath(driver, '//android.widget.ImageView[1]/../android.widget.TextView[2]')
    assert id.is_displayed() is True

    gp = wait_xpath(driver, '//*[@text="GP: MHC Scheme"]')
    assert gp.is_displayed() is True

    dental = wait_xpath(driver, '//*[@text="DENTAL: Annual Limit Applies"]')
    assert dental.is_displayed() is True

    tcm = wait_xpath(driver, '//*[@text="TCM: Consultation Fee ONLY "]')
    assert tcm.is_displayed() is True

    tcm_1 = wait_xpath(driver, '//*[@text="Annual Limit Applies"]')
    assert tcm_1.is_displayed() is True

    ehs = wait_xpath(driver, '//*[@text="EHS: Annual Limit Applies"]')
    assert ehs.is_displayed() is True

    ehs_1 = wait_xpath(driver, '//*[@text="(APPLICABLE AT MHC AMARA ONLY)"]')
    assert ehs_1.is_displayed() is True

    terms_and_conditions = wait_xpath(driver, '//*[@text="Terms and Conditions"]')
    assert terms_and_conditions.is_displayed() is True

    driver.scroll(ehs, gp)

    terms_1 = wait_xpath(driver, '//*[@text="1. This card is NOT transferrable and must be returned upon termination"]')
    assert terms_1.is_displayed() is True

    terms_2 = wait_xpath(driver, '//*[@text="2. This card must be presented to clinic at the point of registration"]')
    assert terms_2.is_displayed() is True
    # endregion

    wait_xpath(driver, '(//android.widget.ImageView)[2]').click()

    # region check Ecard 2
    wait()
    name = wait_xpath(driver, '//android.widget.ImageView/../android.widget.TextView[1]').text
    assert name == n

    id = wait_xpath(driver, '//android.widget.ImageView/../android.widget.TextView[2]').is_displayed()
    assert id is True
    # endregion

def input_salary_advance_indo_language(driver):
    wait()
    salary = wait_xpath(driver, '//android.widget.TextView[1]').text
    assert salary == 'Gaji'

    msg = wait_xpath(driver, '//android.widget.TextView[2]').text
    msg = msg.replace('\n', ' ')
    assert msg == 'Silakan masukkan gaji pokok per bulan Anda:'

    cancel_btn = wait_xpath(driver, '(//android.widget.TextView)[3]')
    assert cancel_btn.text == 'BATAL'

    confirm_btn = wait_xpath(driver, '(//android.widget.TextView)[4]')
    assert confirm_btn.text == 'KONFIRMASI'

    wait_xpath(driver, '//android.widget.EditText[1]').send_keys('10000000')

    confirm_btn.click()

    wait()
    confirm_msg = wait_xpath(driver, '//android.widget.TextView[2]').text
    confirm_msg = confirm_msg.replace('\n', ' ')
    assert confirm_msg == 'Silakan dicatat bahwa Anda dapat menghubungi hai@gigacover.com untuk mengubah ini jika Anda memasukkan gaji pokok per bulan yang tidak sesuai'

    wait_xpath(driver, '(//*[@text="Konfirmasi"])[2]').click()


def add_dependent(driver):
    wait()
    add_dependent_btn = wait_id(driver, 'dependentSectionButton, dependentSectionButton')
    add_dependent_btn.click()

    relation = wait_xpath(driver, '//*[@text="Relationship (optional)"]')
    relation.click()
    relation_list = ['Spouse', 'Parent', 'Children', 'Sibling', 'Others']
    a = choice(relation_list)
    wait_xpath(driver, f'//*[@text="{a}"]').click()

    full_name = wait_xpath(driver, '//*[@text="Full name"]')
    full_name.send_keys(f'Test dependent')

    gender = wait_xpath(driver, '//*[@text="Gender"]')
    gender.click()
    gender_list = ['Male', 'Female', 'Others']
    b = choice(gender_list)
    wait_xpath(driver, f'//*[@text="{b}"]').click()

    nric = generate_nricfin()

    email = wait_xpath(driver, '//*[@text="Email (optional)"]')
    email.send_keys(nric + '@gigacover.com')

    driver.scroll(wait_xpath(driver, '//*[@text="NRIC"]'), wait_xpath(driver, "//*[@text='Add a dependent']"))

    mobile = wait_xpath(driver, '//*[@text="Mobile Number (optional)"]')
    mobile.send_keys(generate_mobile_sgd())

    dob = wait_xpath(driver, '//*[@text="Date of Birth"]')
    dob.click()
    wait_xpath(driver, '//*[@text="OK"]').click()

    nricfin = wait_xpath(driver, '//*[@text="NRIC"]')
    nricfin.send_keys(nric)

    save = wait_xpath(driver, '//*[@text="Save"]')
    save.click()

def verify_past_claim(driver):
    wait()
    TouchAction(driver).tap(x=212, y=513).perform()

    wait_xpath(driver, '//*[@text="View Past Claims"]').click()

    assert wait_xpath(driver, '//*[@text="PROCESSING"]').is_displayed() is True

    wait_xpath(driver, '//*[@text="#1"]').click()

    # date = wait_xpath(driver, '(//*[@text="Date"]/../android.widget.TextView)[2]').text
    # today = datetime.today().strftime("%d %b %Y")

    #TODO check why date of calendar on sevrer different
    #assert date == today

    description = wait_xpath(driver, '(//*[@text="Description"]/../android.widget.TextView)[4]').text
    name_of_doctor = wait_xpath(driver, '(//*[@text="Name of Doctor"]/../android.widget.TextView)[6]').text
    address = wait_xpath(driver, '(//*[@text="Address"]/../android.widget.TextView)[8]').text

    assert description == name_of_doctor == address == 'test'

    picture = driver.find_elements_by_xpath('//android.widget.ImageView')
    assert len (picture) > 0

def tutorial_welcome(driver):
    wait_xpath(driver, '//*[@text="START"]').click()
    wait()
    wait_xpath(driver, '//*[@text="NEXT"]').click()
    wait()
    wait_xpath(driver, '//*[@text="DONE"]').click()

def tutorial_essential(driver):
    wait_xpath(driver, '//*[@text="SKIP"]').click()
    wait()
    wait_xpath(driver, '//*[@text="DONE"]').click()
    wait()
    wait_xpath(driver, '//*[@text="GOT IT"]').click()
