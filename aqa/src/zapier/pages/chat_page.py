import time
from selenium.webdriver.common.by import By
from aqa.utils.enums import Languages, LoginTypes
from aqa.utils.webdriver_util import (
    wait_element,
    take_element_screenshot,
    slide_element,
    check_element_displayed,
    send_text_into_element,
    click_on_element,
    get_element_text,
    wait_seconds
)


class ChatAppPage():
    def __init__(self, driver):
        self.driver          = driver
        self.user_prompt_txt = By.XPATH, '//textarea[@data-testid="user-prompt"]'
        self.user_prompt_btn = By.XPATH, '//textarea[@data-testid="user-prompt"]/following-sibling::button'
        self.last_res_lbl    = By.XPATH, '//li[contains(@class,"items-start")][last()]//div[@data-testid="bot-message"]/p'

    def test_get_response(self, url, prompt, chars_limit):
        self.driver.get(url)
        while not check_element_displayed(self.driver, self.user_prompt_txt):
            wait_seconds(1)
        wait_seconds(3)
        send_text_into_element(
            self.driver,
            self.user_prompt_txt,
            prompt + f'. Vui lòng rút gọn và cải thiện tiêu đề nội dung sản phẩm này nhưng không làm thay đổi ý nghĩa. Nội dung sau khi rút gọn ít hơn {chars_limit} kí tự.')
        click_on_element(self.driver, self.user_prompt_btn)
        wait_seconds(3)
        chat_res_ = get_element_text(self.driver, self.last_res_lbl)
        print(chat_res_)
        return chat_res_
