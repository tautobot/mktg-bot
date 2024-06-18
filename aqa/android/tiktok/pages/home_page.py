from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from aqa.utils.webdriver_util import (
    click_on_element,
    send_text_into_element,
    check_element_displayed,
    wait_seconds,
    swipe_to_right_screen,
    swipe_to_left_screen,
    tap_on_location,
    press_android_keycode
)


class AndroidTikTokHomePage:
    def __init__(self, driver):
        self.driver      = driver
        self.chrome_app  = AppiumBy.ACCESSIBILITY_ID, 'Chrome'
        # self.tiktok_app  = AppiumBy.ACCESSIBILITY_ID, 'TikTok'
        self.tiktok_app = AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("TikTok")'

        self.ads_pop            = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Coupon bundle"]'
        self.campaign_popup     = AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]//com.lynx.tasm.ui.image.FlattenUIImage'
        self.campaign_close_btn = AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]//com.lynx.tasm.ui.image.FlattenUIImage/following-sibling::com.lynx.tasm.behavior.ui.LynxFlattenUI[last()]'
        self.friends_top        = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/text1" and @text="Friends"]'
        self.following_top      = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/text1" and @text="Following"]'
        self.for_you_top        = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/text1" and @text="For You"]'
        self.live_now           = AppiumBy.XPATH, '//android.widget.TextView[@text="LIVE now"]'

        self.home_btn    = AppiumBy.ACCESSIBILITY_ID, 'Home'
        self.shop_btn    = AppiumBy.ACCESSIBILITY_ID, 'Shop'
        self.friends_btn = AppiumBy.ACCESSIBILITY_ID, 'Friends'
        self.inbox_btn   = AppiumBy.ACCESSIBILITY_ID, 'Inbox'
        self.profile_btn = AppiumBy.ACCESSIBILITY_ID, 'Profile'
        self.create_btn  = AppiumBy.ACCESSIBILITY_ID, 'Create'

        self.phone_email_username_btn = AppiumBy.ACCESSIBILITY_ID, 'Use phone / email / username'
        self.email_username_tab       = AppiumBy.ACCESSIBILITY_ID, 'Email / Username'
        self.username_txt             = AppiumBy.XPATH, '//android.widget.EditText[@text="Email or username"]'
        self.continue_btn             = AppiumBy.XPATH, '//android.widget.TextView[@text="Continue"]'
        self.verify_code_txt          = AppiumBy.XPATH, '//android.widget.Button[@text="Resend code"]/preceding-sibling::android.widget.EditText'
        self.resend_code_btn          = AppiumBy.XPATH, '//android.widget.Button[@text="Resend code"]'
        self.login_w_password_btn     = AppiumBy.XPATH, '//android.widget.Button[@text="Log in with password"]'
        self.password_text            = AppiumBy.XPATH, '//android.widget.TextView[@text="Enter password"]/../..//android.widget.EditText'
        self.login_btn                = AppiumBy.XPATH, '//android.widget.TextView[@text="Log in"]'

    def open_app(self, app='TikTok'):
        press_android_keycode(self.driver, AndroidKey.HOME)
        wait_seconds(3)
        if app == 'TikTok':
            click_on_element(self.driver, self.tiktok_app)
        wait_seconds(3)
        # if check_element_displayed(self.driver, self.campaign_popup) or check_element_displayed(self.driver, self.ads_pop):
        #     tap_on_location(self.driver, [(550, 450)])  # Tap outside popup to close it
        press_android_keycode(self.driver, AndroidKey.BACK, 2)

    def login_w_username(self, username, password, logged):
        if check_element_displayed(self.driver, self.for_you_top):
            tap_on_location(self.driver, [(550, 230)])  # Tap on center of screen
        wait_seconds(2)
        if str(logged).upper() != "Y":
            click_on_element(self.driver, self.profile_btn)
            click_on_element(self.driver, self.phone_email_username_btn)
            click_on_element(self.driver, self.email_username_tab)
            send_text_into_element(self.driver, self.username_txt, username)
            click_on_element(self.driver, self.continue_btn)
            click_on_element(self.driver, self.login_w_password_btn)
            send_text_into_element(self.driver, self.password_text, password)
            click_on_element(self.driver, self.login_btn)
            if check_element_displayed(self.driver, self.verify_code_txt):
                code = input("Verify Code: ")
                send_text_into_element(self.driver, self.verify_code_txt, code)
            wait_seconds(1)

    def demo(self):
        if check_element_displayed(self.driver, self.tiktok_app):
            click_on_element(self.driver, self.tiktok_app)
        else:
            print('tiktok_app is not displayed')

