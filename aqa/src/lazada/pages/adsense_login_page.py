import time
from selenium.webdriver.common.by import By
from aqa.utils.enums import URL, Languages, LoginTypes
from aqa.utils.webdriver_util import wait_element, wait_element_quick, isDisplayedLocator, isDisplayedLocatorQuick, take_element_screenshot, slide_element, wait_for_loading
from config import LAZ_ACC, LAZ_PASS


class LazadaAdsensePage():
    def __init__(self, driver):
        self.driver                        = driver
        self.change_lang_btn               = By.ID, 'topActionSwitchLang'
        self.lang_vi_btn                   = By.XPATH, '//*[@id="topActionSwitchLang"]//div[@data-lang="vi"]'
        self.lang_en_btn                   = By.XPATH, '//*[@id="topActionSwitchLang"]//div[@data-lang="en"]'
        self.login_w_account_btn           = By.XPATH, '//*[@class="loginWrap"]//*[@class="loginWithQrWrap-qrCode-Container-rightContent-qrImg"]'
        self.login_w_qr_btn                = By.XPATH, '//*[@class="loginWrap"]//*[@class="loginWrap-rightContent-qrImg"]'
        self.qr_lbl                        = By.XPATH, '//*[@class="loginWithQrWrap-qrCode-Container-title"]'
        self.qr_elm                        = By.XPATH, '//*[@class="loginWithQrWrap-qrCode-img-list-scan-area-qrCode"]'
        self.expired_qr_txt                = By.XPATH, '//*[@class="loginWithQrWrap-qrCode-img-list-scan-area-expired-wrapper-notice"]'
        self.refresh_expired_qr_btn        = By.XPATH, '//*[@class="loginWithQrWrap-qrCode-img-list-scan-area-expired-wrapper-btn"]'

        self.user_name_txt                 = By.XPATH, '//*[@class[contains(.,"loginName")]]/input'
        self.password_txt                  = By.XPATH, '//*[@class[contains(.,"input-password")]]/input'
        self.login_btn                     = By.XPATH, '//*[@class="mod-login-btn"]/button'
        self.slide_btn                     = By.XPATH, '//*[@class="pc-slider"]//*[@class[contains(.,"btn_slide")]]'
        self.slide_to_unlock               = By.XPATH, '//*[@class="pc-slider"]//*[@class[contains(.,"slidetounlock")]]'

        self.affiliate_link_converter      = By.XPATH, '//*[@class="link_convertor_header_title_box"]'
        self.affiliate_release_update_close_btn = By.XPATH, '//*[@role="dialog"][*[text()="Release Updates"]]/a[@role="button" and @aria-label="Close"]'

    def change_lang(self, lang):
        if isDisplayedLocator(self.driver, self.change_lang_btn, -20):
            wait_element(self.driver, self.change_lang_btn).click()
            if lang == Languages.EN:
                wait_element_quick(self.driver, self.lang_en_btn).click()
            elif lang == Languages.VI:
                wait_element_quick(self.driver, self.lang_vi_btn).click()

    def login_w_type(self, login_type):
        if login_type == LoginTypes.ACCOUNT:
            if isDisplayedLocator(self.driver, self.login_w_account_btn):
                login_acc = wait_element_quick(self.driver, self.login_w_account_btn)
                print(f"Found LOGIN TYPE: {login_acc}")
                login_acc.click()
            wait_element_quick(self.driver, self.user_name_txt).send_keys(LAZ_ACC)
            wait_element_quick(self.driver, self.password_txt).send_keys(LAZ_PASS)
            time.sleep(1)

            if isDisplayedLocatorQuick(self.driver, self.login_btn):
                wait_element_quick(self.driver, self.login_btn).click()
            elif isDisplayedLocatorQuick(self.driver, self.slide_btn):
                slide_element(self.driver, self.slide_btn, 500, 0)

        elif login_type == LoginTypes.QR:
            if isDisplayedLocator(self.driver, self.login_w_qr_btn):
                login_qr = wait_element_quick(self.driver, self.login_w_qr_btn)
                print(f"Found LOGIN TYPE: {login_qr}")
                login_qr.click()
            qr = wait_element_quick(self.driver, self.qr_elm)
            take_element_screenshot(self.driver, qr, filename='qr.png')
            while not isDisplayedLocatorQuick(self.driver, self.affiliate_link_converter):
                count_down = 300
                while count_down > 0:
                    time.sleep(1)
                    count_down -= 1
                    if count_down % 60 == 0:
                        if isDisplayedLocatorQuick(self.driver, self.affiliate_link_converter):
                            break
                        else:
                            if isDisplayedLocatorQuick(self.driver, self.qr_lbl):
                                wait_element(self.driver, self.qr_lbl).click()
                if isDisplayedLocatorQuick(self.driver, self.affiliate_link_converter):
                    break
                else:
                    if isDisplayedLocatorQuick(self.driver, self.refresh_expired_qr_btn):
                        wait_element_quick(self.driver, self.refresh_expired_qr_btn).click()
                        take_element_screenshot(self.driver, qr, filename='qr.png')

        # Login successful
        affiliate_converter_func = isDisplayedLocatorQuick(self.driver, self.affiliate_link_converter)
        if affiliate_converter_func:
            # Close Release Update popup
            release_popup = wait_element(self.driver, self.affiliate_release_update_close_btn)
            if release_popup:
                release_popup.click()

    def login(self, url, lang=Languages.EN, login_type=LoginTypes.ACCOUNT):
        self.driver.get(url)
        time.sleep(15)
        self.driver.save_screenshot('img.png')
        self.change_lang(lang)
        time.sleep(15)
        self.login_w_type(login_type)


