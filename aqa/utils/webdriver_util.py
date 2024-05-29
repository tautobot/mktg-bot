from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

WD_WAIT_TIMEOUT = 30

#region element utils
def wait_id(driver, id):
    return WebDriverWait(driver, WD_WAIT_TIMEOUT).until(EC.visibility_of_element_located((By.ID, id)))

def wait_xpath(driver,xpath):
    return WebDriverWait(driver, WD_WAIT_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, xpath)))

def wait_xpath_click(driver,xpath):
    return WebDriverWait(driver, WD_WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, xpath)))

def isDisplayed_xpath(driver, xpath):
    try:
        wait_xpath(driver, xpath)
    except WebDriverException:
        return False
    return True

def findElements_xpath(driver, xpath):
    return  driver.find_elements(By.XPATH, xpath)


def findElements(driver, locator):
    return  driver.find_elements(locator)

def wait_name(driver,name):
    return WebDriverWait(driver, WD_WAIT_TIMEOUT).until(EC.visibility_of_element_located((By.NAME, name)))

def isDisplayed_name(driver, name):
    try:
        wait_name(driver, name)
    except WebDriverException:
        return False
    return True

def wait_element(driver,locator):
    return WebDriverWait(driver, WD_WAIT_TIMEOUT).until(EC.visibility_of_element_located(locator))

def elementIsDisplayed(driver, locator):
    try:
        wait_element(driver, locator)
    except WebDriverException:
        return False
    return True

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#endregion element utils

#region manual wait
def wait():
    sleep(3)

def wait_for_loading():
    sleep(20)
#endregion manual wait

#region wait_loading
def wait_for_loading_venta(wd, timeout:'max seconds to wait'=60):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[contains(@style, "react-spinners-SyncLoader-sync")]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')

def wait_loading_dashboard(wd, timeout:'max seconds to wait'=90):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[contains(@style, "animation")]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')

def wait_loading_mer_dashboard(wd, timeout:'max seconds to wait'=90):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[@class="-loading -active"]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')

def wait_loading_direct_bank(wd, timeout:'max seconds to wait'=90):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[contains(@style, "react-spinners-PulseLoader-pulse")]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')

def pet_wait_loading_direct_bank(wd, timeout:'max seconds to wait'=90):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[(@src="/img/notice/purchase-pending.png")]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')

def wait_loading_credit_iframe(wd, timeout:'max seconds to wait'=90):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[@class="loader"]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')


#endregion wait_loading
