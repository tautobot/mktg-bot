import unittest

from aqa.webdriver.appium_weddriver import *
from aqa.ios.app_file.util_ios import login_pocket_ios, wait, wait_accessibility_id


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = real_ios_webdriver(app_name='pocket')


    def tearDown(self): self.driver.quit()

    # group fixed

    #validation
    def test_min_validation(self):

        wait()
        wait_accessibility_id(self.driver, 'HomeButtonRow-Advance').click()

        try:
            wait_accessibility_id(self.driver, 'yesCB').click()
            wait_accessibility_id(self.driver, 'NEXT').click()
        except:
            pass

        wait_accessibility_id(self.driver, 'Advance-MakeARequest').click()
        wait()

        # Verify error msg when amount_request < 100,000
        wait_accessibility_id(self.driver, 'inputAmount').send_keys('1')
        wait_accessibility_id(self.driver, 'Done').click()
        wait_accessibility_id(self.driver, 'Advance-MakeRequestContinue').click()

        error_msg = wait_accessibility_id(self.driver, 'Advance-MakeRequestErrorText').text
        assert error_msg == 'The minimum advance amount is Rp 100.000. Please increase the amount.'


    def test_max_validation(self):
        login_pocket_ios(self.driver, 'a12233392@gigacover.com', 'A12233392')

        wait()
        wait_accessibility_id(self.driver, 'HomeButtonRow-Advance').click()

        try:
            wait_accessibility_id(self.driver, 'yesCB').click()
            wait_accessibility_id(self.driver, 'NEXT').click()
        except:
            pass

        salary_earned = wait_accessibility_id(self.driver, 'availableAmount').text

        wait_accessibility_id(self.driver, 'Advance-MakeARequest').click()
        wait()

        # Verify error msg when amount_request > available_amount
        amount_request = int(salary_earned.replace('.', '')) + 1
        wait_accessibility_id(self.driver, 'inputAmount').send_keys(str(amount_request))
        wait_accessibility_id(self.driver, 'Done').click()
        wait_accessibility_id(self.driver, 'Advance-MakeRequestContinue').click()

        error_msg = wait_accessibility_id(self.driver, 'Advance-MakeRequestErrorText').text
        assert error_msg == 'You don’t have enough balance. Please lower the amount.'
