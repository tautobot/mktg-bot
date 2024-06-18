from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.action_helpers import ActionHelpers
from PIL import Image
from io import BytesIO
from config import *


filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))
WD_WAIT_TIMEOUT = 30
WD_WAIT_TIMEOUT_QUICK = 3
IMPLICIT_WAIT_TIMEOUT = 10


def wait_element(driver, locator, duration=WD_WAIT_TIMEOUT):
    return WebDriverWait(driver, duration).until(EC.visibility_of_element_located(locator))


def wait_element_clickable(driver, locator, duration=WD_WAIT_TIMEOUT):
    return WebDriverWait(driver, duration).until(EC.presence_of_element_located(locator))


def wait_elements(driver, locator, duration=WD_WAIT_TIMEOUT):
    return WebDriverWait(driver, duration).until(EC.visibility_of_any_elements_located(locator))


# region android webdriver utils
def click_on_element(driver, loc, time=IMPLICIT_WAIT_TIMEOUT):
    wait_element(
        driver=driver,
        locator=loc,
        duration=time
    ).click()


def click_on_element_location(driver, loc, timeout=IMPLICIT_WAIT_TIMEOUT, duration=1000):
    el = wait_element(
        driver=driver,
        locator=loc,
        duration=timeout
    ).location
    x = el.get('x')
    y = el.get('y')
    ActionHelpers.tap(driver, [(x, y)], duration=duration)


def get_element_text(driver, loc, time=IMPLICIT_WAIT_TIMEOUT):
    return wait_element(
        driver=driver,
        locator=loc,
        duration=time
    ).text


def send_text_into_element(driver, loc, text, time=IMPLICIT_WAIT_TIMEOUT):
    wait_element(
        driver=driver,
        locator=loc,
        duration=time
    ).send_keys(text)


def check_element_displayed(driver, loc, duration=IMPLICIT_WAIT_TIMEOUT):
    # implicitly_wait is set default in init appium webdriver. We can change implicitly_wait here
    # driver.implicitly_wait(3)
    try:
        WebDriverWait(driver, duration).until(EC.presence_of_element_located(loc))
    except NoSuchElementException as e:
        print("Element not found: {}".format(e))
        return False
    except TimeoutException as e:
        print("Timeout: {}".format(e))
        return False
    return True


def swipe_to_right_screen(driver, times=1):
    for t in range(times):
        ActionHelpers.swipe(driver, 1000, 500, 100, 500)
        wait_seconds(1)


def swipe_to_left_screen(driver, times=1):
    for t in range(times):
        ActionHelpers.swipe(driver, 100, 100, 1000, 100)
        wait_seconds(1)


def swipe_down(driver, times=1):
    for t in range(times):
        ActionHelpers.swipe(driver, 550, 500, 550, 1500)
        wait_seconds(1)


def swipe_up(driver, times=1):
    for t in range(times):
        ActionHelpers.swipe(driver, 550, 1500, 550, 500)
        wait_seconds(1)


def swipe_by_coordinates(driver, start_x, start_y, end_x, end_y, duration=1500, times=1):
    for t in range(times):
        ActionHelpers.swipe(driver, start_x, start_y, end_x, end_y, duration)
        wait_seconds(1)


def swipe_up_by_pages(driver, num_pages=1, duration=2000, times=1):
    for t in range(times):
        for p in range(num_pages):
            ActionHelpers.swipe(driver, 550, 1500, 550, 500, duration)
            wait_seconds(1)


def swipe_down_by_pages(driver, num_pages=1, duration=2000, times=1):
    for t in range(times):
        for p in range(num_pages):
            ActionHelpers.swipe(driver, 550, 500, 550, 1500, duration)
            wait_seconds(1)


def tap_on_location(driver, tuple_x_y):
    ActionHelpers.tap(driver, tuple_x_y)


def scroll_from_el1_to_el2(driver, loc1, loc2, duration=1000):
    el1 = wait_element(driver, loc1)
    el2 = wait_element(driver, loc2)
    ActionHelpers.scroll(driver, el1, el2, duration=duration)


def drag_drop_from_el1_to_el2(driver, el1, el2, pause=2):
    ActionHelpers.drag_and_drop(driver, el1, el2, pause=pause)


def drag_drop_from_loc1_to_loc2(driver, loc1, loc2, pause=2):
    el1 = wait_element(driver, loc1)
    el2 = wait_element(driver, loc2)
    ActionHelpers.drag_and_drop(driver, el1, el2, pause=pause)


def press_android_keycode(driver, keycode, time=1):
    for t in range(0, time):
        driver.press_keycode(keycode)
        wait_seconds(1)


def wait_xpath(driver, xpath, time=IMPLICIT_WAIT_TIMEOUT):
    return WebDriverWait(driver, time).until(EC.visibility_of_element_located((By.XPATH, xpath)))


def appium_is_displayed_xpath(driver, xpath, time=IMPLICIT_WAIT_TIMEOUT):
    try:
        wait_element = WebDriverWait(driver, time)
        wait_element.until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath)))
    except TimeoutException:
        return False
    except WebDriverException:
        return False
    return True


def read_file(path):
    with open(path, "r") as file:
        return file.read()


def write_to_file(name, path):
    with open(path, "w") as file:
        file.write(name)


def wait_seconds(s):
    sleep(s)


def wait_id(driver, id):
    return WebDriverWait(driver, WD_WAIT_TIMEOUT).until(EC.visibility_of_element_located((By.ID, id)))

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


def wait_element_quick(driver, locator):
    return WebDriverWait(driver, WD_WAIT_TIMEOUT_QUICK).until(EC.visibility_of_element_located(locator))


def isDisplayedLocator(driver, locator, add_wait_time=0):
    try:
        wait_element(driver, locator, add_wait_time)
    except WebDriverException:
        return False
    return True


def isDisplayedLocatorQuick(driver, locator):
    try:
        wait_element_quick(driver, locator)
    except WebDriverException:
        return False
    return True


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def drag_drop(driver, f_locator, t_locator, add_wait_time=0):
    drag = WebDriverWait(driver, WD_WAIT_TIMEOUT + add_wait_time).until(EC.visibility_of_element_located(f_locator))
    drop = WebDriverWait(driver, WD_WAIT_TIMEOUT + add_wait_time).until(EC.visibility_of_element_located(t_locator))
    ActionChains(driver).drag_and_drop(drag, drop).perform()


def slide_element(driver, locator, x, y, add_wait_time=0):
    move = ActionChains(driver)
    slider = WebDriverWait(driver, WD_WAIT_TIMEOUT + add_wait_time).until(EC.visibility_of_element_located(locator))
    move.click_and_hold(slider).move_by_offset(x, y).release().perform()


def wait_xpath_clickable(driver, xpath, time=IMPLICIT_WAIT_TIMEOUT):
    return WebDriverWait(driver, time).until(EC.element_to_be_clickable((By.XPATH, xpath)))


def is_displayed_xpath(driver, xpath, time=IMPLICIT_WAIT_TIMEOUT):
    try:
        WebDriverWait(driver, time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except WebDriverException:
        return False
    return True


def appium_wait_accessibility_id(driver, accessibility_id, time=IMPLICIT_WAIT_TIMEOUT):
    return WebDriverWait(driver, time).until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, accessibility_id)))


def appium_wait_xpath(driver, xpath, time=IMPLICIT_WAIT_TIMEOUT):
    return WebDriverWait(driver, time).until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath)))


def appium_wait_uiselector_text(driver, text, time=IMPLICIT_WAIT_TIMEOUT):
    return WebDriverWait(driver, time).until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')))

# endregion android webdriver utils


#region manual wait10s
def wait():
    sleep(3)

def wait_for_loading():
    sleep(20)
#endregion manual wait10s

#region wait_loading
def wait_for_loading_venta(wd, timeout:'max seconds to wait10s'=60):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[contains(@style, "react-spinners-SyncLoader-sync")]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')

def wait_loading_dashboard(wd, timeout:'max seconds to wait10s'=90):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[contains(@style, "animation")]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')

def wait_loading_mer_dashboard(wd, timeout:'max seconds to wait10s'=90):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[@class="-loading -active"]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')

def wait_loading_direct_bank(wd, timeout:'max seconds to wait10s'=90):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[contains(@style, "react-spinners-PulseLoader-pulse")]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')


def wait_loading_credit_iframe(wd, timeout:'max seconds to wait10s'=90):
    i=0; step=0.3
    while True:
        loading_icon = wd.find_elements(By.XPATH, '//*[@class="loader"]')
        still_loading = len(loading_icon) > 0
        if not still_loading: break

        sleep(step); i += step
        if i >= timeout: raise Exception('Page loading too long')

#endregion wait_loading

def take_element_screenshot(driver, element, filename='screenshot.png'):
    # Ref https://stackoverflow.com/questions/15018372/how-to-take-partial-screenshot-with-selenium-webdriver-in-python

    location = element.location
    size = element.size
    png = driver.get_screenshot_as_png()  # saves screenshot of entire page

    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save(filename)  # saves new cropped image


def save_element_as_png(element, file_name_wo_ext):
    # open file in write and binary mode
    with open(f"{file_name_wo_ext}.png", 'wb') as file:
        # write file
        file.write(element.screenshot_as_png)


def click_element_by_location(driver, element):
    location = element.location
    size = element.size

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    ac = ActionChains(driver)
    ac.move_to_element(element).move_by_offset(top - 1, right - 1).click().perform()

