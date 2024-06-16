from selenium.webdriver.common.by import By
from aqa.webdriver.selenium_webdriver import webdriver_local
from aqa.utils.webdriver_util import (
    check_element_displayed,
    send_text_into_element,
    click_on_element,
    get_element_text,
    wait_seconds
)

ai_response = None


def ai_shorten_desc(prompt, chars_limit):
    try:
        driver = webdriver_local('local', 'yes')
        user_prompt_txt = By.XPATH, '//textarea[@data-testid="user-prompt"]'
        user_prompt_btn = By.XPATH, '//textarea[@data-testid="user-prompt"]/following-sibling::button'
        last_res_lbl    = By.XPATH, '//li[contains(@class,"items-start")][last()]//div[@data-testid="bot-message"]/p'
        driver.get('https://tktbot.zapier.app/chat')
        while not check_element_displayed(driver, user_prompt_txt):
            wait_seconds(1)
        wait_seconds(3)
        send_text_into_element(
            driver,
            user_prompt_txt,
            prompt + f'. Vui lòng rút gọn và cải thiện tiêu đề nội dung sản phẩm này nhưng không làm thay đổi ý nghĩa. Nội dung sau khi rút gọn ít hơn {chars_limit} kí tự.')
        click_on_element(driver, user_prompt_btn)
        wait_seconds(3)
        return get_element_text(driver, last_res_lbl)
    except Exception as e:
        print("An error occurred:", e)
        return None


def run_ai_shorten_desc(prompt, chars_limit):
    global ai_response
    ai_response = ai_shorten_desc(prompt, chars_limit)