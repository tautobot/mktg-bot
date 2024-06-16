from aqa.src.zapier.pages.chat_page import ChatAppPage
from aqa.src.base import BaseTest
from aqa.webdriver.selenium_webdriver import webdriver_local
from config import headless, CHROME_DRI_ENV, set_headless, set_chromedriver_env


class Test(BaseTest):

    def setUp_fixture(self):
        self.chat_page = ChatAppPage(self.driver)

    def get_chatgpt_response(self):
        set_headless('no')
        set_chromedriver_env('local')
        self.setUp_fixture()
        return self.chat_page.get_response(
            'https://tktbot.zapier.app/chat',
            "(HCM) COMBO Thùng 20 gói giấy ăn cao cấp mềm mịn, giấy rút tiện lợi cho gia đình Khăn Giấy Giấy Vệ Sinh",
            100
        )
