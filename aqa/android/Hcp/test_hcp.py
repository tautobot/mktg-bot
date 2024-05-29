import os
import unittest
from random import choice
from aQA.webdriver.appium_weddriver import android_webdriver
from aQA.android.src.app_file.util import login_pouch, wait, wait_xpath, change_password_from_API
from appium.webdriver.common.touch_action import TouchAction

from testcases.lib.generic import generate_mobile_sgd

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = android_webdriver()

    def tearDown(self): self.driver.quit()

    def test_claim_Eng_UI(self):
        self.driver.push_file(destination_path="/sdcard/Pictures/1.jpg", source_path=f"{app_path}/fixtures/1.jpg")
        self.driver.push_file(destination_path="/sdcard/Pictures/2.jpg", source_path=f"{app_path}/fixtures/2.jpg")
        self.driver.push_file(destination_path="/sdcard/Pictures/3.jpg", source_path=f"{app_path}/fixtures/3.jpg")
        self.driver.push_file(destination_path="/sdcard/Pictures/4.jpg", source_path=f"{app_path}/fixtures/4.jpg")
        self.driver.push_file(destination_path="/sdcard/Pictures/5.jpg", source_path=f"{app_path}/fixtures/5.jpg")
        self.driver.push_file(destination_path="/sdcard/Pictures/6.jpg", source_path=f"{app_path}/fixtures/6.jpg")
        self.driver.push_file(destination_path="/sdcard/Pictures/7.jpg", source_path=f"{app_path}/fixtures/7.jpg")
        self.driver.push_file(destination_path="/sdcard/Pictures/8.jpg", source_path=f"{app_path}/fixtures/8.jpg")
        self.driver.push_file(destination_path="/sdcard/Pictures/9.jpg", source_path=f"{app_path}/fixtures/9.jpg")

        login_pouch(self.driver, 'S4581509I@gigacover.com', 'S4581509I')

        wait()
        wait_xpath(self.driver, '//*[@text="Claims"]').click()

        wait()
        TouchAction(self.driver).tap(x=212, y=513).perform()

        wait()
        wait_xpath(self.driver, '//*[@text="Claimant’s Name"]').send_keys('Claimant’s Name')
        wait_xpath(self.driver, '//*[@text="Inpatient"]').click()
        wait_xpath(self.driver, '//android.widget.TextView[@text="Next"]').click()
        wait_xpath(self.driver, '//*[@text="Date of Admission"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()
        wait_xpath(self.driver, '//*[@text="Date of Discharge"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()
        wait_xpath(self.driver, '//*[@text="Diagnosis"]').send_keys('test')
        wait_xpath(self.driver, '//*[@text="Date of First Diagnosed"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Date of First Diagnosed"]'), wait_xpath(self.driver, '//*[@text="Date of Admission"]'))

        wait_xpath(self.driver, '//*[@text="The Main Complaint that Appears"]').send_keys('The Main Complaint that Appears')
        wait_xpath(self.driver, '//*[@text="Date the First Symptoms / Complaint occured"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Date the First Symptoms / Complaint occured"]'), wait_xpath(self.driver, '//*[@text="Date of First Diagnosed"]'))
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Name of Doctor or Hospital"]'), wait_xpath(self.driver, '//*[@text="Date the First Symptoms / Complaint occured"]'))

        wait_xpath(self.driver, '//*[@text="Name of Doctor or Hospital"]').send_keys('Name of Doctor or Hospital')
        wait_xpath(self.driver, '//*[@text="Address"]').send_keys('Address')

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Address"]'), wait_xpath(self.driver, '//*[@text="Claims"]'))

        wait_xpath(self.driver, '//*[@text="Diagnosis"]').send_keys('Diagnosis')

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Diagnosis"]'), wait_xpath(self.driver, '//*[@text="Address"]'))

        wait_xpath(self.driver, '//*[@text="Date"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()
        wait_xpath(self.driver, '//*[@text="Next"]').click()

        wait_xpath(self.driver, '//*[@text="Date of Accident"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()
        wait_xpath(self.driver, '//*[@text="Place of Accident"]').send_keys('Place of Accident')
        wait_xpath(self.driver, '//*[@text="Chronology of Accident"]').send_keys('Chronology of Accident')

        wait_xpath(self.driver, '//*[@text="Next"]').click()

        wait_xpath(self.driver, '//*[@text="Name"]').send_keys('Name')
        wait_xpath(self.driver, '//*[@text="Mobile Phone Number"]').send_keys(generate_mobile_sgd())
        wait_xpath(self.driver, '//*[@text="Email Address"]').send_keys('test_aqa_hcp@gigacover.com')
        wait_xpath(self.driver, '//*[@text="Next"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="Next"]').click()
        wait_xpath(self.driver, '//*[@text="Allow"]').click()

        wait()
        self.driver.scroll(wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[1]'), wait_xpath(self.driver, '//*[@text="You may submit a maximum of 3 photos"]'))

        wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[5]').click()
        wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[6]').click()

        wait()
        wait_xpath(self.driver, '//android.widget.TextView[@text="Next"]').click()

        wait()
        wait_xpath(self.driver, '//android.widget.TextView[@text="Next"]').click()

        wait()
        wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[1]').click()
        wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[2]').click()
        wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[3]').click()

        wait()
        wait_xpath(self.driver, '//*[@text="Next"]').click()

        wait_xpath(self.driver, '//*[@text="ID/KTP"]').send_keys('ID/KTP')
        wait_xpath(self.driver, '//*[@text="Name of Bank"]').send_keys('Name of Bank')
        wait_xpath(self.driver, '//*[@text="Name of Bank Account Holder"]').send_keys('Name of Bank Account Holder')
        wait_xpath(self.driver, '//*[@text="Bank Account Number"]').send_keys('Bank Account Number')

        wait_xpath(self.driver, '//*[@text="SAVE"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="CONFIRM"]').click()
        wait_xpath(self.driver, '//*[@text="Yes, I have read and agree to the “Delcaration and Authorization”"]').click()
        wait_xpath(self.driver, '//*[@text="Submit"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="SUBMIT"]').click()
        assert wait_xpath(self.driver, '//*[@text="Claim successfully submitted!"]').is_displayed() is True

    def test_claim_Indo_UI(self):
        login_pouch(self.driver, 'S3504396I@gigacover.com', 'S3504396I')

        wait_xpath(self.driver, '//*[@text="EN"]').click()
        wait_xpath(self.driver, '//*[@text="ID"]').click()

        wait()
        wait_xpath(self.driver, '//*[@text="Klaim"]').click()

        wait()
        TouchAction(self.driver).tap(x=212, y=513).perform()

        wait()
        wait_xpath(self.driver, '//*[@text="Nama Pemohon Klaim"]').send_keys('Claimant’s Name')
        wait_xpath(self.driver, '//*[@text="Rawat Inap"]').click()
        wait_xpath(self.driver, '//*[@text="Lanjutkan"]').click()
        wait_xpath(self.driver, '//*[@text="Tanggal Masuk Perawatan"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()
        wait_xpath(self.driver, '//*[@text="Tanggal Keluar Perawatan"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()
        wait_xpath(self.driver, '//*[@text="Diagnosa Penyakit"]').send_keys('test')
        wait_xpath(self.driver, '//*[@text="Tanggal Pertama Kali Terdiagnosa"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Tanggal Pertama Kali Terdiagnosa"]'), wait_xpath(self.driver, '//*[@text="Tanggal Masuk Perawatan"]'))

        wait_xpath(self.driver, '//*[@text="Gejala / Keluhan Utama Yang Muncul"]').send_keys('The Main Complaint that Appears')
        wait_xpath(self.driver, '//*[@text="Tanggal Gejala / Keluhan Tersebut Pertama Kali Dirasakan"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Tanggal Gejala / Keluhan Tersebut Pertama Kali Dirasakan"]'), wait_xpath(self.driver, '//*[@text="Tanggal Pertama Kali Terdiagnosa"]'))
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Nama Dokter atau Rumah Sakit"]'), wait_xpath(self.driver, '//*[@text="Tanggal Gejala / Keluhan Tersebut Pertama Kali Dirasakan"]'))

        wait_xpath(self.driver, '//*[@text="Nama Dokter atau Rumah Sakit"]').send_keys('Name of Doctor or Hospital')
        wait_xpath(self.driver, '//*[@text="Alamat"]').send_keys('Address')

        try:
            self.driver.scroll(wait_xpath(self.driver, '//*[@text="Alamat"]'), wait_xpath(self.driver, '//*[@text="Tanggal Gejala / Keluhan Tersebut Pertama Kali Dirasakan"]'))
        except:
            pass

        wait_xpath(self.driver, '//*[@text="Diagnosa Penyakit"]').send_keys('Diagnosis')

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Diagnosa Penyakit"]'), wait_xpath(self.driver, '//*[@text="Alamat"]'))

        wait_xpath(self.driver, '//*[@text="Tanggal"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()
        wait_xpath(self.driver, '//*[@text="Lanjutkan"]').click()

        wait_xpath(self.driver, '//*[@text="Tanggal Kecelakaan"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()
        wait_xpath(self.driver, '//*[@text="Tempat Kecelakaan"]').send_keys('Place of Accident')
        wait_xpath(self.driver, '//*[@text="Kronologi Kecelakaan Singkat"]').send_keys('Chronology of Accident')

        wait_xpath(self.driver, '//*[@text="Lanjutkan"]').click()

        wait_xpath(self.driver, '//*[@text="Nama"]').send_keys('Name')
        wait_xpath(self.driver, '//*[@text="Nomor Telepon Seluler"]').send_keys(generate_mobile_sgd())
        wait_xpath(self.driver, '//*[@text="Alamat Email"]').send_keys('test_aqa_hcp@gigacover.com')
        wait_xpath(self.driver, '//*[@text="Lanjutkan"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="Lanjutkan"]').click()
        wait_xpath(self.driver, '//*[@text="Allow"]').click()

        wait()
        self.driver.scroll(wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[1]'), wait_xpath(self.driver, '//*[@text="FOTO (0) DIPILIH"]'))

        wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[5]').click()
        wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[6]').click()

        wait()
        wait_xpath(self.driver, '//*[@text="Lanjutkan"]').click()

        wait()
        wait_xpath(self.driver, '//*[@text="Lanjutkan"]').click()

        wait()
        wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[1]').click()
        wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[2]').click()
        wait_xpath(self.driver, '(//android.widget.ScrollView//android.widget.ImageView)[3]').click()

        wait()
        wait_xpath(self.driver, '//*[@text="Lanjutkan"]').click()

        wait_xpath(self.driver, '//*[@text="ID/KTP"]').send_keys('ID/KTP')
        wait_xpath(self.driver, '//*[@text="Nama Bank"]').send_keys('Name of Bank')
        wait_xpath(self.driver, '//*[@text="Nama Pemilik Rekening"]').send_keys('Name of Bank Account Holder')
        wait_xpath(self.driver, '//*[@text="Nomor Rekening Bank"]').send_keys('Bank Account Number')

        wait_xpath(self.driver, '//*[@text="SIMPAN"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="KONFIRMASI"]').click()
        wait_xpath(self.driver, '//*[@text="Ya, saya telah membaca dan menyetujui “Pernyataan dan Kuasa”"]').click()
        wait_xpath(self.driver, '//*[@text="Kirim"]').click()
        wait()
        wait_xpath(self.driver, '//*[@text="KIRIM"]').click()
        assert wait_xpath(self.driver, '//*[@text="Pengajuan klaim berhasil!"]').is_displayed() is True

    def test_self_bought_hcp(self):
        email = 'S4984534J@gigacover.com'
        change_password_from_API(email)
        login_pouch(self.driver, email, 'Test1234')
        wait()

        purchase = wait_xpath(self.driver, '//*[@text="PURCHASE"]')
        purchase.click()

        hcp = wait_xpath(self.driver, '//*[@text="Hospital Cash Plan"]')
        hcp.click()

        buy = wait_xpath(self.driver, '//*[@text="BUY"]')
        buy.click()

        wait_xpath(self.driver, '//*[@text="Inpatient Compensation"]').click()
        hcp_plan = ['Rp 100.000', 'Rp 300.000', 'Rp 400.000', 'Rp 500.000', 'Rp 600.000', 'Rp 700.000', 'Rp 800.000']
        plan = choice(hcp_plan)
        wait_xpath(self.driver, f'//*[@text="{plan}"]').click()

        wait_xpath(self.driver, '//*[@text="Coverage Period"]').click()
        hcp_unit = ['1 Month', '3 Months', '6 Months', '1 Year']
        unit = choice(hcp_unit)
        wait_xpath(self.driver, f'//*[@text="{unit}"]').click()

        wait_xpath(self.driver, '//*[@text="Starting Date"]').click()
        wait_xpath(self.driver, '//*[@text="OK"]').click()

        wait_xpath(self.driver, '//*[@text="Continue"]').click()

        gender = wait_xpath(self.driver, '//*[@text="Gender"]')
        gender.click()
        gender_list = ['Male', 'Female']
        b = choice(gender_list)
        wait_xpath(self.driver, f'//*[@text="{b}"]').click()

        wait_xpath(self.driver, '//*[@text="Place of Birth"]').send_keys('Place of Birth')

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Date of Birth"]'), wait_xpath(self.driver, "//*[@text='Place of Birth']"))

        wait_xpath(self.driver, '//*[@text="ID Number"]').send_keys('1111111111221133')

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="ID Number"]'), wait_xpath(self.driver, "//*[@text='Personal Info']"))

        wait_xpath(self.driver, '//*[@text="Address"]').send_keys('Address')
        wait_xpath(self.driver, '//*[@text="City"]').send_keys('City')
        wait_xpath(self.driver, '//*[@text="Postal Code"]').send_keys('123456')

        self.driver.scroll(wait_xpath(self.driver, '//*[@text="Address"]'), wait_xpath(self.driver, "//*[@text='Personal Info']"))
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="City"]'), wait_xpath(self.driver, "//*[@text='Personal Info']"))
        self.driver.scroll(wait_xpath(self.driver, '//*[@text="b."]'), wait_xpath(self.driver, "//*[@text='Personal Info']"))

        wait_xpath(self.driver, '//*[@text="I have read, understood and accepted the Benefits and Terms of the Hospital Cash Plan product. "]').click()
        wait_xpath(self.driver, '//*[@text="Continue To Payment"]').click()

        wait_xpath(self.driver, '//*[@text="OVO e-Wallet"]').click()
        wait_xpath(self.driver, '//*[@text="Pay"]').click()

        wait_xpath(self.driver, '//*[@text="08"]').send_keys('1234567')
        wait_xpath(self.driver, '//*[@text="Continue"]').click()
        wait_xpath(self.driver, '//*[@text="Done"]').click()

        # TODO check later why policy is pending
        # wait()
        #
        # # Logout and Login again to refresh API
        # wait_xpath(self.driver, '//*[@text="Account"]').click()
        #
        # self.driver.scroll(wait_xpath(self.driver, '//*[@text="Balance"]'), wait_xpath(self.driver, "//*[@text='Personal Details']"))
        #
        # wait_xpath(self.driver, '//*[@text="Logout"]').click()
        #
        # next_btn = wait_xpath(self.driver, "//*[@text='NEXT']")
        # next_btn.click()
        #
        # pass_box = wait_xpath(self.driver, "//*[@text='Enter your password']")
        # pass_box.send_keys('Test1234')
        #
        # next_btn = wait_xpath(self.driver, "//*[@text='NEXT']")
        # next_btn.click()
        #
        # wait()
        #
        # # Verify HCP PLan is exist
        # assert wait_xpath(self.driver, '//*[@text="Hospital Cash Plan"]').is_displayed()
