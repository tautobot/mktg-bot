import unittest
from aqa.webdriver.appium_weddriver import android_webdriver
from aqa.android.tiktok.pages.home_page import AndroidTikTokHomePage
from aqa.android.tiktok.pages.shop_page import AndroidTikTokShopPage
from aqa.android.tiktok.pages.product_page import AndroidTikTokProductPage
from config import TIKTOK_ACC, TIKTOK_PASS, TIKTOK_LOGGED


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = android_webdriver()
        self.home_page = AndroidTikTokHomePage(self.driver)
        self.shop_page = AndroidTikTokShopPage(self.driver)
        self.product_page = AndroidTikTokProductPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # group fixed
    def test_login_tiktok(self):
        self.home_page.open_app()
        # self.home_page.login_w_username(TIKTOK_ACC, TIKTOK_PASS, TIKTOK_LOGGED)
        # self.shop_page.go_through_products_from_flash_sale(3)
        p = self.product_page.collect_product_details()
        e = self.product_page.collect_earn_details()
        self.product_page.create_shoppable_video(p)

        # self.shop_page.demo()

