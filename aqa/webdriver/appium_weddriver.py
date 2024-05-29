import os

import pytest
from appium import webdriver
from config_local import *


filepath = os.path.dirname(__file__)
app_path = os.path.dirname(filepath)


def android_webdriver(app_name='pouch'):
    path = f'/root/{app_name}.apk' if environment == 'docker' else f"{app_path}/android/app_file/{app_name}.apk"
    appium_options = webdriver.webdriver.AppiumOptions()
    desired_cap = {
        "deviceName"                       : "emulator-5554",
        "platformName"                     : "Android",
        "app"                              : path,
        "automationName"                   : "UiAutomator2",
        "unicodeKeyboard"                  : True,
        "resetKeyboard"                    : True,
        "adbExecTimeout"                   : 300000,
        "androidInstallTimeout"            : 500000,
        "uiautomator2ServerInstallTimeout" : 300000,
        "uiautomator2ServerLaunchTimeout"  : 300000,
    }
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=appium_options.load_capabilities(desired_cap))
    driver.implicitly_wait(100)
    return driver


def ios_webdriver(app_name='pouch'):
    path = f"{app_path}/ios/app_file/{app_name}.app"
    appium_options = webdriver.webdriver.AppiumOptions()
    desired_cap = {
        "platformName"                     : "iOS",
        "platformVersion"                  : "16.0",
        "deviceName"                       : "iPhone 14 Pro Max",
        "automationName"                   : "xcuitest",
        "app"                              : path,
        "udid"                             : UDID,
        "unicodeKeyboard"                  : True,
        "connectHardwareKeyboard"          : False,
        "sendKeyStrategy"                  : "setValue",
        "includeNonModalElements"          : True,
        "shouldUseTestManagerForVisibilityDetection": True,
        "simpleIsVisibleCheck"             : True,
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=appium_options.load_capabilities(desired_cap))
    driver.implicitly_wait(100)
    return driver


@pytest.fixture()
def real_ios_webdriver(app_name='pouch'):
    path = f"{app_path}/ios/app_file/{app_name}.app"
    appium_options = webdriver.webdriver.AppiumOptions()
    desired_cap = {
        "platformName"                     : "iOS",
        "platformVersion"                  : "17.2.1",
        "deviceName"                       : "iPhone XS Pro Max",
        "automationName"                   : "xcuitest",
        # "app"                              : path,
        "udid"                             : "00008020-0019314A0190003A",
        "bundleId"                         : "com.mktg.wda.runner",
        "xcodeOrgId"                       : "",
        "xcodeSigningId"                   : "Mktg",
        "updatedWDABundleId"               : ""
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=appium_options.load_capabilities(desired_cap))
    driver.open_notifications()
    driver.implicitly_wait(300)
    return driver
