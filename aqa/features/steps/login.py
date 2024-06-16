from time import sleep

# from behave_webdriver.steps import *
from behave import *
from aqa.utils.webdriver_util import wait_xpath, wait_id
from aqa.utils.enums import url


@given('open webportal url')
def step_impl(context):
    context.driver.get(url.url_web_portal_phl)

@when('user input {username} and {password}')
def step_impl(context, username, password):
    email = wait_id(context.driver, 'email')
    email.send_keys(username)

    pwd = wait_id(context.driver, 'password')
    pwd.send_keys(password)

@then('user click on login button')
def step_impl(context):
    login_btn = wait_xpath(context.driver, '//*[(text()="LOG IN")]')
    login_btn.click()

@then('wait10s')
def step_impl(context):
    sleep(20)