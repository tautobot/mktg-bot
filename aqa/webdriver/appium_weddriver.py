from appium import webdriver
from config import *


filepath = os.path.dirname(__file__)
app_path = os.path.dirname(filepath)

device_name = ANDROID_DEVICE_NAME  # emulator emulator-5554


def android_webdriver(app_name='pouch'):
    path = f'/root/{app_name}.apk' if environment == 'docker' else f"{app_path}/android/app_file/{app_name}.apk"
    appium_options = webdriver.webdriver.AppiumOptions()
    desired_cap = {
        "deviceName"                       : device_name,
        "platformName"                     : "Android",
        "bundleId"                         : "com.ss.android.ugc.trill",
        # "app"                              : path,
        "automationName"                   : "uiautomator2",
        "hideKeyboard"                     : True,
        "resetKeyboard"                    : True,
        "adbExecTimeout"                   : 300000,
        "androidInstallTimeout"            : 500000,
        "uiautomator2ServerInstallTimeout" : 300000,
        "uiautomator2ServerLaunchTimeout"  : 300000,
        "disableIdLocatorAutocompletion": True,  # The requested id selector does not have a package name prefix. This Appium session has package name autocompletion enabled, which may be the reason why no elements were found. To disable this behavior, relaunch this session with the capability 'appium:disableIdLocatorAutocompletion' set to 'true'.
    }
    driver = webdriver.Remote('http://localhost:4723', options=appium_options.load_capabilities(desired_cap))
    # driver.implicitly_wait(5)
    return driver


# @pytest.fixture()
def ios_webdriver(app_name='pouch'):
    path = f"{app_path}/ios/app_file/{app_name}.app"
    appium_options = webdriver.webdriver.AppiumOptions()
    desired_cap = {
        "platformName"                     : "iOS",
        "platformVersion"                  : "17.5",
        "deviceName"                       : "iPhone 15 Pro Max",
        "automationName"                   : "XCUITest",
        # "app"                              : path,
        "udid"                             : UDID,
        "unicodeKeyboard"                  : True,
        "connectHardwareKeyboard"          : False,
        "sendKeyStrategy"                  : "setValue",
        "includeNonModalElements"          : True,
        "shouldUseTestManagerForVisibilityDetection": True,
        "simpleIsVisibleCheck"             : True,
        'bundleId'                         : 'com.apple.mobilesafari',
        'usePreinstalledWDA'               : True,
        'xcodeOrgId'                       : '522GKSR677',
        'updatedWDABundleId'               : 'com.tktdev.WebDriverAgentRunner',
        'nativeWebTap'                     : True,
        'safariIgnoreFraudWarning'         : True,
        'webviewConnectTimeout'            : 100000

    }
    driver = webdriver.Remote("http://127.0.0.1:4723", options=appium_options.load_capabilities(desired_cap))
    driver.implicitly_wait(100)
    return driver


# @pytest.fixture()
def real_ios_webdriver(app_name='pouch'):
    path = f"{app_path}/ios/app_file/{app_name}.app"
    appium_options = webdriver.webdriver.AppiumOptions()
    desired_cap = {
        "platformName"                     : "iOS",
        "platformVersion"                  : "17.2.1",
        "deviceName"                       : "iPhone XS Pro Max",
        "automationName"                   : "XCUITest",
        # "app"                              : path,
        "udid"                             : UDID,
        "bundleId"                         : "com.mktg.rios.IntegrationApp",
        "xcodeOrgId"                       : "",
        "xcodeSigningId"                   : "Mktg",
        "updatedWDABundleId"               : ""
    }
    driver = webdriver.Remote("http://localhost:4723", options=appium_options.load_capabilities(desired_cap))
    # driver.open_notifications()
    # driver.implicitly_wait(300)
    return driver
