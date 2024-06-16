from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from aqa.android.tiktok.pages.product_page import AndroidTikTokProductPage
from aqa.utils.webdriver_util import (
    click_on_element,
    click_on_element_location,
    send_text_into_element,
    check_element_displayed,
    wait_seconds,
    swipe_to_right_screen,
    swipe_to_left_screen,
    swipe_down,
    swipe_up,
    swipe_up_by_pages,
    swipe_down_by_pages,
    tap_on_location,
    scroll_from_el1_to_el2,
    press_android_keycode
)


class AndroidTikTokShopPage:
    def __init__(self, driver):
        self.driver = driver
        self.product_page = AndroidTikTokProductPage(self.driver)

        self.chrome_app = AppiumBy.ACCESSIBILITY_ID, 'Chrome'
        # self.tiktok_app = AppiumBy.ACCESSIBILITY_ID, 'TikTok'
        self.tiktok_app = AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("TikTok")'

        self.ads_pop         = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Coupon bundle"]'
        self.friends_top     = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/text1" and @text="Friends"]'
        self.following_top   = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/text1" and @text="Following"]'
        self.for_you_top     = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/text1" and @text="For You"]'

        self.home_btn = AppiumBy.ACCESSIBILITY_ID, 'Home'
        self.shop_btn = AppiumBy.ACCESSIBILITY_ID, 'Shop'
        self.friends_btn = AppiumBy.ACCESSIBILITY_ID, 'Friends'
        self.inbox_btn = AppiumBy.ACCESSIBILITY_ID, 'Inbox'
        self.profile_btn = AppiumBy.ACCESSIBILITY_ID, 'Profile'
        self.create_btn = AppiumBy.ACCESSIBILITY_ID, 'Create'

        self.orders                        = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Orders"]'
        self.free_shipping                 = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Free Shipping"]'
        self.messages                      = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Messages"]'
        self.buy_local                     = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Buy Local"]'
        self.bonus                         = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Bonus"]'
        self.creator                       = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Creator"]'
        self.address                       = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Address"]'
        self.payment                       = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Payment"]'
        self.help                          = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Help"]'
        self.policies                      = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Policies"]'
        self.flash_sale_all                = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="::"]'
        # self.flash_sale_all                = AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("::")'
        self.flash_sale_1                  = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[contains(@content-desc,"₫")][1]'
        self.flash_sale_2                  = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[contains(@content-desc,"₫")][2]'
        self.flash_sale_3                  = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[contains(@content-desc,"₫")][3]'
        self.flash_sale_4                  = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[contains(@content-desc,"₫")][4]'
        self.flash_sale_product            = '//com.lynx.tasm.behavior.ui.list.UIList/following-sibling::com.ss.android.ugc.aweme.ecommerce.ui.EcomFlattenUIImage[{0}]'
        self.view_more                     = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.list.UIList/following-sibling::com.ss.android.ugc.aweme.ecommerce.ui.EcomFlattenUIImage[{0}]/preceding-sibling::com.lynx.tasm.behavior.ui.LynxFlattenUI[@content-desc="View more"]'

        self.horizontal_menu_all           = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="All"]'
        self.horizontal_menu_beauty        = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Beauty"]'
        self.horizontal_menu_womenswear    = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Womenswear"]'
        self.horizontal_menu_menswear      = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Menswear"]'
        self.horizontal_menu_personal_care = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Personal care"]'
        self.horizontal_menu_electronics   = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Electronics"]'
        self.horizontal_menu_baby          = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Baby"]'
        self.horizontal_menu_food          = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Food"]'
        self.horizontal_menu_foodwear      = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Foodwear"]'
        self.horizontal_menu_sports        = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Sports"]'
        self.horizontal_menu_health        = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Health"]'
        self.horizontal_menu_accessories   = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Accessories"]'
        self.horizontal_menu_household     = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Household"]'
        self.horizontal_menu_vehicle       = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Vehicle"]'
        self.horizontal_menu_bags          = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Bags"]'
        self.horizontal_menu_appliances    = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Appliances"]'
        self.horizontal_menu_textiles      = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Textiles"]'
        self.horizontal_menu_kidswear      = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Kidswear"]'
        self.horizontal_menu_kitchen       = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Kitchen"]'
        self.horizontal_menu_toys          = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Toys"]'
        self.horizontal_menu_pets_and_toys = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc="Pets & Toys"]'

    def go_through_products_from_flash_sale(self, num):
        # if check_element_displayed(self.driver, self.for_you_top):
        #     tap_on_location(self.driver, [(700, 1200)])
        click_on_element_location(self.driver, self.shop_btn)
        wait_seconds(3)
        tap_on_location(self.driver, [(540, 50)])  # Skip ads popup
        # Click on flash sale
        # click_on_element_location(self.driver, self.flash_sale_all)
        # Improve by tapping on location
        tap_on_location(self.driver, [(540, 780)])  # Top center of flash sale section
        count = 0
        wait_seconds(3)
        product1 = AppiumBy.XPATH, self.flash_sale_product.format(1)
        product2 = AppiumBy.XPATH, self.flash_sale_product.format(4)
        for i in range(1, 3*num, 3):
            count += 1
            if count == 1:
                click_on_element(self.driver, product1)
            else:
                click_on_element(self.driver, product2)
            wait_seconds(2)
            # TODO: Create a page to add the product into owner shop
            self.product_page.collect_all_data_n_create_shoppable_video()
            # Finish creating a shoppable video, get back to products list
            press_android_keycode(self.driver, AndroidKey.BACK)
            # Each time scroll up a product, 2nd product will become 1st one
            scroll_from_el1_to_el2(self.driver, product2, product1, 1100)

    def demo(self):
        pass
