import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import headless, CODE_HOME, CHROME_DRI_ENV
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

filepath = os.path.dirname(__file__)
IMPLICITLY_WAIT = 5


def options(hdl):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    if hdl == 'yes':
        chrome_options.add_argument("--headless")
    else:
        pass

    return chrome_options


def webdriver_local(type=CHROME_DRI_ENV, hdl=headless):
    """
    There is an issue that all sessions must be closed before can connect to the port.
    Considering solution that we can check if the port is in use, then use another port.
    """
    chrome_options = options(hdl)
    if type == 'local_w_profile':
        chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
        chrome_options.add_argument('--remote-debugging-pipe')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument(f'user-data-dir={CODE_HOME}/aqa/src/chrome_ud')
        chrome_options.add_argument(f'profile-directory=Profile 35')
    chrome_options.page_load_strategy = 'eager'
    # chrome_options.add_argument("--headless")  # open Browser in maximized mode
    chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    chrome_options.add_argument("--disable-infobars")  # disabling infobars
    chrome_options.add_argument("--disable-extensions")  # disabling extensions
    chrome_options.add_argument('--disable-popup-blocking')  # disabling extensions
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

    # chrome_options.binary_location = "/Applications/Chrome-debug.app/Chrome-debug"
    # No need to install chromedriver anymore since Selenium 4
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver = webdriver.Chrome(
        options=chrome_options,
        # service=ChromeService(
        #     executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        # )
    )
    driver.implicitly_wait(IMPLICITLY_WAIT)
    driver.maximize_window()
    return driver


def webdriver_docker():
    options().add_argument(webdriver.ChromeOptions)
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options()
    )
    driver.implicitly_wait(IMPLICITLY_WAIT)
    driver.maximize_window()
    return driver


def is_webdriver_alive(driver):
    print('Checking whether the driver is alive')
    try:
        assert(driver.service.process.poll() == None) #Returns an int if dead and None if alive
        driver.service.assert_process_still_running() #Throws a WebDriverException if dead
        driver.find_element_by_tag_name('html') #Throws a NoSuchElementException if dead
        print('The driver appears to be alive')
        return True
    except (NoSuchElementException, WebDriverException, AssertionError):
        print('The driver appears to be dead')
        return False
    except Exception as ex:
        print('Encountered an unexpected exception type ({}) while checking the driver status'.format(type(ex)))
        return False