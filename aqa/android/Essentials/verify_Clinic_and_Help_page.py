import unittest

from testcases.lib.generic import read_cell_in_excel_file
from aQA.webdriver.appium_weddriver import *
from aQA.android.src.app_file.util import *

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))
excel_file = f'{app_path}/fixtures/benefits_template_no_nricfin.xlsx'

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = android_webdriver(app_name='pouch')

    def tearDown(self): self.driver.quit()

    def test_00_verify_Clinic_and_Help_page(self):
        email = read_cell_in_excel_file(excel_file, 'F4')
        pwd = read_cell_in_excel_file(excel_file, 'E4')

        login_pouch(self.driver, email, pwd)
        wait()
        tutorial_welcome(self.driver)

        wait_xpath(self.driver, '//*[@text="Doctor (GP)"]').click()
        wait_xpath(self.driver, '//*[@text="CLOSE"]').click()

        wait()
        wait_xpath(self.driver, '//*[@text="SKIP"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="DONE"]').click()

        wait_xpath(self.driver, '//*[@text="Find a Clinic"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="All"]').click()

        # region verify GP clinic information
        wait()
        area = wait_xpath(self.driver, "//*[@text='Alexandra']")
        area.click()

        wait()
        clinic_name = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[1]").text
        assert clinic_name == 'TOWN HALL CLINIC (ALEXANDRA)'

        address = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[2]").text
        assert address == '438C ALEXANDRA ROAD  #01-01 ALEXANDRA TECHNOPARK THE HUB  SINGAPORE 119976  '

        clinic_area = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[3]").text
        assert clinic_area == 'ALEXANDRA'

        open_time = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[4]").text
        assert open_time == 'MON-FRI: 8.30AM-12.00PM, 2.00PM-4.15PM | SAT: 8.30AM-10.15AM | SUN: CLOSED | PH: CLOSED'

        phone_number = wait_xpath(self.driver, "(//android.widget.ScrollView//android.widget.TextView)[6]").text
        assert phone_number == '62788088'
        # endregion

        # region verify TCM clinic information
        self.driver.back()
        self.driver.back()

        wait()
        TCM = wait_xpath(self.driver, '//*[@text="Traditional Chinese Medicine"]')
        TCM.click()

        wait_xpath(self.driver, '//*[@text="CLOSE"]').click()
        wait_xpath(self.driver, '//*[@text="Find a Clinic"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="All"]').click()

        wait()
        area = wait_xpath(self.driver, "//*[@text='Beach Road']")
        area.click()

        wait()
        clinic_name = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[1]").text
        assert clinic_name == 'ADVANCED TCM CLINIC'

        address = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[2]").text
        assert address == '371 BEACH ROAD  #B1-46 CITY GATE  SINGAPORE 199597'

        clinic_area = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[3]").text
        assert clinic_area == 'BEACH ROAD'

        open_time = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[4]").text
        assert open_time == 'MON-FRI : 10.00AM-9.30PM | SAT : 10.00AM-9.30PM | SUN : 10.00AM-6.00PM | PH : 10.00AM-6.00PM'

        phone_number = wait_xpath(self.driver, "(//android.widget.ScrollView//android.widget.TextView)[6]").text
        assert phone_number == '63369781'
        # endregion

        # region verify Dental clinic information
        self.driver.back()
        self.driver.back()

        wait()
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Traditional Chinese Medicine"]'), wait_xpath(self.driver, "//*[@text='Doctor (GP)']"))

        dental = wait_xpath(self.driver, '//*[@text="Dental"]')
        dental.click()

        wait_xpath(self.driver, '//*[@text="CLOSE"]').click()
        wait_xpath(self.driver, '//*[@text="Find a Clinic"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="All"]').click()

        wait()
        area = wait_xpath(self.driver, "//*[@text='Balestier']")
        area.click()

        wait()
        clinic_name = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[1]").text
        assert clinic_name == 'ADVANCED DENTAL CLINIC WHAMPOA PTE LTD'

        address = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[2]").text
        assert address == 'BLK 88 WHAMPOA DRIVE  #01-853  SINGAPORE 320088'

        clinic_area = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[3]").text
        assert clinic_area == 'BALESTIER'

        open_time = wait_xpath(self.driver, "//android.widget.ScrollView//android.widget.TextView[4]").text
        assert open_time == 'MON/TUE/WED: 9.00AM-9.00PM   THUR/FRI: 9.00AM-5.00PM | SAT: 9.00AM-5.00PM | SUN: 9.00AM-5.00PM | PH: CLOSED'

        phone_number = wait_xpath(self.driver, "(//android.widget.ScrollView//android.widget.TextView)[6]").text
        assert phone_number == '63520828'
        # endregion
