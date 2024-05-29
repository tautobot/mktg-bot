import unittest

from aqa.webdriver.appium_weddriver import *
from aqa.android.app_file.util import get_advances, login_pocket, wait, wait_xpath, wait_id
from appium import webdriver

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = android_webdriver(app_name='tiktok-34-9-5')

    def tearDown(self): self.driver.quit()

    # group fixed
    def test_request_advances_Eng_UI(self):
        advance = get_advances('a12233390@gigacover.com', 'A12233390')
        login_pocket(self.driver, 'a12233390@gigacover.com', 'A12233390')

        wait()
        wait_xpath(self.driver, '//*[@text="Advance"]').click()
        wait_xpath(self.driver, '//*[@text="Yes"]').click()
        wait_xpath(self.driver, '//*[@text="NEXT"]').click()

        wait()
        # Verify display correctly info from advance API
        salary_earned = wait_id(self.driver, 'availableAmount').text
        assert salary_earned == format(advance["available_amount"], ',d').replace(',', '.')

        payroll_days = wait_id(self.driver, 'payroll_days').text
        assert payroll_days == f'{str(advance["payroll_days"])} days this month'

        eligibility_period = wait_id(self.driver, 'period').text
        assert eligibility_period == f'{str(advance["advance_start_day"])}-{str(advance["advance_end_day"])} of each month'

        wait_xpath(self.driver, '//*[@text="Make A Request"]').click()
        wait()

        instructionBalance = wait_id(self.driver, 'instructionBalance').text
        assert instructionBalance == f"Available salary balance: Rp {format(advance['available_amount'], ',d').replace(',', '.')}"

        instructionMinimum = wait_id(self.driver, 'instructionMinimum').text
        assert instructionMinimum == 'Minimum request amount is Rp 100.000'

        amount_request = '100000'
        wait_id(self.driver, 'inputAmount').clear()
        wait_id(self.driver, 'inputAmount').send_keys(amount_request)
        wait_xpath(self.driver, '//*[@text="Continue"]').click()

        wait()

        # Verify number of amount_request and total_amount_transferred correctly after minus fee
        confirm_amount_request = self.driver.find_element_by_accessibility_id('selectedAmount').text
        assert confirm_amount_request.replace('.', '') == amount_request

        fee = wait_id(self.driver, 'Service fee').text
        assert fee == '- Rp 20.000'

        total_amount_transferred = wait_id(self.driver, 'Amount to be transferred').text
        assert int(total_amount_transferred.split(' ')[1].replace('.', '')) == int(confirm_amount_request.replace('.', '')) - 20000

        balance_after_transfer = wait_id(self.driver, 'Balance after transfer').text
        assert int((balance_after_transfer.split(' ')[1]).replace('.', '')) == int(advance["available_amount"]) - int(amount_request)

        amout_receive = wait_id(self.driver, 'You will receive').text
        assert amout_receive == total_amount_transferred

        wait_xpath(self.driver, '//*[@text="Submit Request"]').click()

        wait()

        # Verify text of success UI
        assert wait_xpath(self.driver, '//*[@text="Advance request received"]').is_displayed() is True

    def test_request_advances_Indo_UI(self):
        advance = get_advances('a12233391@gigacover.com', 'A12233391')
        login_pocket(self.driver, 'a12233391@gigacover.com', 'A12233391')

        wait()

        # wait_xpath(self.driver, '//*[@text="Profile"]').click()
        # wait_xpath(self.driver, '//*[@text="Settings"]').click()
        # wait_xpath(self.driver, '//*[@text="Bahasa"]').click()
        #
        # wait_xpath(self.driver, '(//*[@text="Pengaturan"]/../android.view.ViewGroup)[1]').click()
        # wait_xpath(self.driver, '//*[@text="Beranda"]').click()

        wait_xpath(self.driver, '//*[@text="Advance"]').click()
        wait_xpath(self.driver, '//*[@text="Ya"]').click()
        wait_xpath(self.driver, '//*[@text="LANJUT"]').click()

        wait()
        # Verify display correctly info from advance API
        salary_earned = wait_id(self.driver, 'availableAmount').text
        assert salary_earned == format(advance["available_amount"], ',d').replace(',', '.')

        payroll_days = wait_id(self.driver, 'payroll_days').text
        assert payroll_days == f'{str(advance["payroll_days"])} hari di bulan ini'

        eligibility_period = wait_id(self.driver, 'period').text
        assert eligibility_period == f'{str(advance["advance_start_day"])}-{str(advance["advance_end_day"])} setiap bulannya'

        wait_xpath(self.driver, '//*[@text="Ajukan Sekarang"]').click()
        wait()

        instructionBalance = wait_id(self.driver, 'instructionBalance').text
        assert instructionBalance == f"Saldo tersedia saat ini: Rp {format(advance['available_amount'], ',d').replace(',', '.')}"

        instructionMinimum = wait_id(self.driver, 'instructionMinimum').text
        assert instructionMinimum == 'Jumlah minimum penarikan Rp. 100.000'

        amount_request = '100000'
        wait_id(self.driver, 'inputAmount').clear()
        wait_id(self.driver, 'inputAmount').send_keys(amount_request)
        wait_xpath(self.driver, '//*[@text="Lanjutkan"]').click()

        wait()

        # Verify number of amount_request and total_amount_transferred correctly after minus fee
        confirm_amount_request = self.driver.find_element_by_accessibility_id('selectedAmount').text
        assert confirm_amount_request.replace('.', '') == amount_request

        fee = wait_id(self.driver, 'Biaya admin').text
        assert fee == '- Rp 20.000'

        total_amount_transferred = wait_id(self.driver, 'Jumlah yang ditransfer').text
        assert int(total_amount_transferred.split(' ')[1].replace('.', '')) == int(confirm_amount_request.replace('.', '')) - 20000

        balance_after_transfer = wait_id(self.driver, 'Saldo setelah transfer').text
        assert int((balance_after_transfer.split(' ')[1]).replace('.', '')) == int(advance["available_amount"]) - int(amount_request)

        amout_receive = wait_id(self.driver, 'Anda akan menerima').text
        assert amout_receive == total_amount_transferred

        wait_xpath(self.driver, '//*[@text="Ajukan Advance"]').click()

        wait()

        #Verify text of success UI
        assert wait_xpath(self.driver, '//*[@text="Pengajuan Advance telah diterima "]').is_displayed() is True

    # group tier https://gigacover.atlassian.net/browse/GC-4867
    def test_request_advances_Eng_tier_1(self):
        advance = get_advances('a12233340@gigacover.com', 'A12233340')
        login_pocket(self.driver, 'a12233340@gigacover.com', 'A12233340')

        wait()
        wait_xpath(self.driver, '//*[@text="Advance"]').click()

        try:
            wait_xpath(self.driver, '//*[@text="Yes"]').click()
            wait_xpath(self.driver, '//*[@text="NEXT"]').click()
        except:
            pass

        wait()
        # Verify display correctly info from advance API
        salary_earned = wait_id(self.driver, 'availableAmount').text
        assert salary_earned == format(advance["available_amount"], ',d').replace(',', '.')

        payroll_days = wait_id(self.driver, 'payroll_days').text
        assert payroll_days == f'{str(advance["payroll_days"])} days this month'

        eligibility_period = wait_id(self.driver, 'period').text
        assert eligibility_period == f'{str(advance["advance_start_day"])}-{str(advance["advance_end_day"])} of each month'

        wait_xpath(self.driver, '//*[@text="Make A Request"]').click()
        wait()

        instructionBalance = wait_id(self.driver, 'instructionBalance').text
        assert instructionBalance == f"Available salary balance: Rp {format(advance['available_amount'], ',d').replace(',', '.')}"

        instructionMinimum = wait_id(self.driver, 'instructionMinimum').text
        assert instructionMinimum == 'Minimum request amount is Rp 100.000'

        # tier 1: 100 - 500K
        amount_request = '500000'
        wait_id(self.driver, 'inputAmount').clear()
        wait_id(self.driver, 'inputAmount').send_keys(amount_request)
        wait_xpath(self.driver, '//*[@text="Continue"]').click()

        wait()

        #Verify number of amount_request and total_amount_transferred correctly after minus fee
        confirm_amount_request = self.driver.find_element_by_accessibility_id('selectedAmount').text
        assert confirm_amount_request.replace('.', '') == amount_request

        fee = wait_id(self.driver, 'Service fee').text
        assert fee == '- Rp 10.000'

        total_amount_transferred = wait_id(self.driver, 'Amount to be transferred').text
        assert int(total_amount_transferred.split(' ')[1].replace('.', '')) == int(confirm_amount_request.replace('.', '')) - 10000

        balance_after_transfer = wait_id(self.driver, 'Balance after transfer').text
        assert int((balance_after_transfer.split(' ')[1]).replace('.', '')) == int(advance["available_amount"]) - int(amount_request)

        amout_receive = wait_id(self.driver, 'You will receive').text
        assert amout_receive == total_amount_transferred

        wait_xpath(self.driver, '//*[@text="Submit Request"]').click()

        wait()

        #Verify text of success UI
        assert wait_xpath(self.driver, '//*[@text="Advance request received"]').is_displayed() is True


    def test_request_advances_Eng_tier_2(self):
        advance = get_advances('a12233340@gigacover.com', 'A12233340')
        login_pocket(self.driver, 'a12233340@gigacover.com', 'A12233340')

        wait()
        wait_xpath(self.driver, '//*[@text="Advance"]').click()

        try:
            wait_xpath(self.driver, '//*[@text="Yes"]').click()
            wait_xpath(self.driver, '//*[@text="NEXT"]').click()
        except:
            pass

        wait()
        # Verify display correctly info from advance API
        salary_earned = wait_id(self.driver, 'availableAmount').text
        assert salary_earned == format(advance["available_amount"], ',d').replace(',', '.')

        payroll_days = wait_id(self.driver, 'payroll_days').text
        assert payroll_days == f'{str(advance["payroll_days"])} days this month'

        eligibility_period = wait_id(self.driver, 'period').text
        assert eligibility_period == f'{str(advance["advance_start_day"])}-{str(advance["advance_end_day"])} of each month'

        wait_xpath(self.driver, '//*[@text="Make A Request"]').click()
        wait()

        instructionBalance = wait_id(self.driver, 'instructionBalance').text
        assert instructionBalance == f"Available salary balance: Rp {format(advance['available_amount'], ',d').replace(',', '.')}"

        instructionMinimum = wait_id(self.driver, 'instructionMinimum').text
        assert instructionMinimum == 'Minimum request amount is Rp 100.000'

        # tier 2: > 500K - 1 mil
        amount_request = '1000000'
        wait_id(self.driver, 'inputAmount').clear()
        wait_id(self.driver, 'inputAmount').send_keys(amount_request)
        wait_xpath(self.driver, '//*[@text="Continue"]').click()

        wait()

        #Verify number of amount_request and total_amount_transferred correctly after minus fee
        confirm_amount_request = self.driver.find_element_by_accessibility_id('selectedAmount').text
        assert confirm_amount_request.replace('.', '') == amount_request

        fee = wait_id(self.driver, 'Service fee').text
        assert fee == '- Rp 30.000'

        total_amount_transferred = wait_id(self.driver, 'Amount to be transferred').text
        assert int(total_amount_transferred.split(' ')[1].replace('.', '')) == int(confirm_amount_request.replace('.', '')) - 30000

        balance_after_transfer = wait_id(self.driver, 'Balance after transfer').text
        assert int((balance_after_transfer.split(' ')[1]).replace('.', '')) == int(advance["available_amount"]) - int(amount_request)

        amout_receive = wait_id(self.driver, 'You will receive').text
        assert amout_receive == total_amount_transferred

        wait_xpath(self.driver, '//*[@text="Submit Request"]').click()

        wait()

        #Verify text of success UI
        assert wait_xpath(self.driver, '//*[@text="Advance request received"]').is_displayed() is True


    def test_request_advances_Eng_tier_3(self):
        advance = get_advances('a12233340@gigacover.com', 'A12233340')
        login_pocket(self.driver, 'a12233340@gigacover.com', 'A12233340')

        wait()
        wait_xpath(self.driver, '//*[@text="Advance"]').click()

        try:
            wait_xpath(self.driver, '//*[@text="Yes"]').click()
            wait_xpath(self.driver, '//*[@text="NEXT"]').click()
        except:
            pass

        wait()
        # Verify display correctly info from advance API
        salary_earned = wait_id(self.driver, 'availableAmount').text
        assert salary_earned == format(advance["available_amount"], ',d').replace(',', '.')

        payroll_days = wait_id(self.driver, 'payroll_days').text
        assert payroll_days == f'{str(advance["payroll_days"])} days this month'

        eligibility_period = wait_id(self.driver, 'period').text
        assert eligibility_period == f'{str(advance["advance_start_day"])}-{str(advance["advance_end_day"])} of each month'

        wait_xpath(self.driver, '//*[@text="Make A Request"]').click()
        wait()

        instructionBalance = wait_id(self.driver, 'instructionBalance').text
        assert instructionBalance == f"Available salary balance: Rp {format(advance['available_amount'], ',d').replace(',', '.')}"

        instructionMinimum = wait_id(self.driver, 'instructionMinimum').text
        assert instructionMinimum == 'Minimum request amount is Rp 100.000'

        # tier 3: > 1 mil
        amount_request = '1100000'
        wait_id(self.driver, 'inputAmount').clear()
        wait_id(self.driver, 'inputAmount').send_keys(amount_request)
        wait_xpath(self.driver, '//*[@text="Continue"]').click()

        wait()

        #Verify number of amount_request and total_amount_transferred correctly after minus fee
        confirm_amount_request = self.driver.find_element_by_accessibility_id('selectedAmount').text
        assert confirm_amount_request.replace('.', '') == amount_request

        fee = wait_id(self.driver, 'Service fee').text
        assert fee == '- Rp 50.000'

        total_amount_transferred = wait_id(self.driver, 'Amount to be transferred').text
        assert int(total_amount_transferred.split(' ')[1].replace('.', '')) == int(confirm_amount_request.replace('.', '')) - 50000

        balance_after_transfer = wait_id(self.driver, 'Balance after transfer').text
        assert int((balance_after_transfer.split(' ')[1]).replace('.', '')) == int(advance["available_amount"]) - int(amount_request)

        amout_receive = wait_id(self.driver, 'You will receive').text
        assert amout_receive == total_amount_transferred

        wait_xpath(self.driver, '//*[@text="Submit Request"]').click()

        wait()

        #Verify text of success UI
        assert wait_xpath(self.driver, '//*[@text="Advance request received"]').is_displayed() is True


    #min - max validation
    def test_min_validation(self):
        advance = get_advances('a12233392@gigacover.com', 'A12233392')
        login_pocket(self.driver, 'a12233392@gigacover.com', 'A12233392')

        wait()
        wait_xpath(self.driver, '//*[@text="Advance"]').click()

        try:
            wait_xpath(self.driver, '//*[@text="Yes"]').click()
            wait_xpath(self.driver, '//*[@text="NEXT"]').click()
        except:
            pass

        wait()
        # Verify display correctly info from advance API
        salary_earned = wait_id(self.driver, 'availableAmount').text
        assert salary_earned == format(advance["available_amount"], ',d').replace(',', '.')

        payroll_days = wait_id(self.driver, 'payroll_days').text
        assert payroll_days == f'{str(advance["payroll_days"])} days this month'

        eligibility_period = wait_id(self.driver, 'period').text
        assert eligibility_period == f'{str(advance["advance_start_day"])}-{str(advance["advance_end_day"])} of each month'

        wait_xpath(self.driver, '//*[@text="Make A Request"]').click()
        wait()

        instructionBalance = wait_id(self.driver, 'instructionBalance').text
        assert instructionBalance == f"Available salary balance: Rp {format(advance['available_amount'], ',d').replace(',', '.')}"

        instructionMinimum = wait_id(self.driver, 'instructionMinimum').text
        assert instructionMinimum == 'Minimum request amount is Rp 100.000'

        # Verify error msg when amount_request < 100,000
        wait_id(self.driver, 'inputAmount').send_keys('1')
        wait_xpath(self.driver, '//*[@text="Continue"]').click()
        error_msg = wait_xpath(self.driver, '//*[@text="The minimum advance amount is Rp 100.000. Please increase the amount."]').is_displayed()
        assert error_msg is True


    def test_max_validation(self):
        advance = get_advances('a12233392@gigacover.com', 'A12233392')
        login_pocket(self.driver, 'a12233392@gigacover.com', 'A12233392')

        wait()
        wait_xpath(self.driver, '//*[@text="Advance"]').click()

        try:
            wait_xpath(self.driver, '//*[@text="Yes"]').click()
            wait_xpath(self.driver, '//*[@text="NEXT"]').click()
        except:
            pass

        wait()
        # Verify display correctly info from advance API
        salary_earned = wait_id(self.driver, 'availableAmount').text
        assert salary_earned == format(advance["available_amount"], ',d').replace(',', '.')

        payroll_days = wait_id(self.driver, 'payroll_days').text
        assert payroll_days == f'{str(advance["payroll_days"])} days this month'

        eligibility_period = wait_id(self.driver, 'period').text
        assert eligibility_period == f'{str(advance["advance_start_day"])}-{str(advance["advance_end_day"])} of each month'

        wait_xpath(self.driver, '//*[@text="Make A Request"]').click()
        wait()

        instructionBalance = wait_id(self.driver, 'instructionBalance').text
        assert instructionBalance == f"Available salary balance: Rp {format(advance['available_amount'], ',d').replace(',', '.')}"

        instructionMinimum = wait_id(self.driver, 'instructionMinimum').text
        assert instructionMinimum == 'Minimum request amount is Rp 100.000'

        # Verify error msg when amount_request > available_amount
        amount_request = int(salary_earned.replace('.', '')) + 1
        wait_id(self.driver, 'inputAmount').send_keys(str(amount_request))
        wait_xpath(self.driver, '//*[@text="Continue"]').click()
        error_msg = wait_xpath(self.driver, '//*[@text="You don’t have enough balance. Please lower the amount."]').is_displayed()
        assert error_msg is True


    def test_max_requested_validation(self):
        advance = get_advances('a12233393@gigacover.com', 'A12233393')
        login_pocket(self.driver, 'a12233393@gigacover.com', 'A12233393')

        wait()
        wait_xpath(self.driver, '//*[@text="Advance"]').click()

        try:
            wait_xpath(self.driver, '//*[@text="Yes"]').click()
            wait_xpath(self.driver, '//*[@text="NEXT"]').click()
        except:
            pass

        wait()

        for i in range(1, advance['requests_remain'] + 1):
            wait_xpath(self.driver, '//*[@text="Make A Request"]').click()
            wait()
            amount_request = 100000
            wait_id(self.driver, 'inputAmount').send_keys(str(amount_request))
            wait_xpath(self.driver, '//*[@text="Continue"]').click()
            wait_xpath(self.driver, '//*[@text="Submit Request"]').click()
            wait_id(self.driver, 'backBtn').click()

        error_msg = wait_xpath(self.driver, '//*[@text="Number of requests exceeds number of request allowed"]').is_displayed()
        assert error_msg is True

