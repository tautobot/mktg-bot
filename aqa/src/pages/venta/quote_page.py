import datetime
from random import choice, randint

from selenium.webdriver.common.by import By

from aqa.utils.webdriver_util import wait_element, scroll_to_bottom, findElements_xpath


class PaQuotePage():
    def __init__(self, driver):
        self.driver                = driver
        self.got_it_btn            = By.XPATH, '//*[text()="GOT IT!"]'
        self.next_btn              = By.XPATH, '//*[text()="NEXT"]'
        self.proposed_checkbox     = By.XPATH, '//*[contains(text(),"I, the proposed insured")]/../button'
        self.declare_checkbox      = By.XPATH, '//*[contains(text(),"I declare ")]/../button'
                                   
    def click_on_got_it_btn(self):
        wait_element(self.driver,self.got_it_btn).click()

    def choose_coverage_level(self, coverage_level):
        level = wait_element(self.driver, (By.XPATH,f'//*[text()="{coverage_level}"]/../button'))
        level.click()

    def click_all_checkbox(self):
        wait_element(self.driver,self.proposed_checkbox).click()
        wait_element(self.driver,self.declare_checkbox).click()

    def click_next_btn(self):
        wait_element(self.driver,self.next_btn).click()


class FlepQuotePage():
    def __init__(self, driver):
        self.driver                   = driver
        self.gojek_icon               = By.XPATH,'//img[contains(@src,"gojek")]/../../button'
        self.not_gojek                = By.XPATH,'//*[text()="No, I don’t"]'
        self.next_btn                 = By.XPATH,'//*[text()="NEXT"]'
        self.indoor_btn               = By.XPATH,'//*[text()="Indoor "]/../../button'
        self.outdoor_btn              = By.XPATH,'//*[text()="Outdoor "]/../../button'
        self.transport_vehicle_detail = By.XPATH,'//*[@placeholder="Please specify"]'
        self.occupation_detail        = By.XPATH,'(//*[@placeholder="Please specify"])[1]'
        self.transport_mode_detail    = By.XPATH,'(//*[@placeholder="Please specify"])[last()]'
        self.dob                      = By.XPATH,'//*[text()="What is Your Date of Birth?"]/following-sibling::div[1]'
        self.date_picker_year         = By.XPATH,'//*[contains(@class, "MuiPickersToolbarButton-toolbarBtn")][1]'
        self.start_date               = By.XPATH,'//*[@class="gc-datepicker-custom"]'
        self.ok_btn                   = By.XPATH,'//*[text()="OK"]'
        self.check_box                = By.XPATH,'//*[contains(text(),"I, the proposed insured")]/../button'
    
    def choose_gojek(self):
        wait_element(self.driver, self.gojek_icon).click()
        wait_element(self.driver,self.next_btn).click()

    def choose_not_gojek(self):
        wait_element(self.driver,self.not_gojek).click()
        wait_element(self.driver,self.next_btn).click()

    def choose_indoor_environment(self):
        wait_element(self.driver,self.indoor_btn).click()
        wait_element(self.driver,self.next_btn).click()

    def choose_random_public_transport(self):
        transport_vehicle_list = ['Public Transport (MRT / Bus)', 'Car / Taxi', 'Motorcycle', 'Others']
        transport_vehicle = choice(transport_vehicle_list)
        wait_element(self.driver, (By.XPATH, f'//*[text()="{transport_vehicle}"]/../button')).click()
        if transport_vehicle == 'Others':
            wait_element(self.driver,self.transport_vehicle_detail).send_keys('walk')
        wait_element(self.driver,self.next_btn).click()
        return transport_vehicle

    def choose_motorcycle_transport(self):
        wait_element(self.driver, (By.XPATH, f'//*[text()="Motorcycle"]/../button')).click()
        wait_element(self.driver,self.next_btn).click()

    def choose_outdoor_environment(self):
        wait_element(self.driver,self.outdoor_btn).click()

    def choose_random_occupation(self):
        data = {}
        occupation_list = ['Private Hire Driver', 'Food / Logistic Delivery', 'Food Hawker', 'Cleaner / Handyman', 'Salesperson', 'Fitness Coach', 'Photographer / Film Professional', 'Others']
        occupation = choice(occupation_list)
        data['occupation'] = occupation
        wait_element(self.driver, (By.XPATH, f'//*[text()="{occupation}"]/../button')).click()

        data['transport_mode'] = ''
        if occupation == 'Others':
            wait_element(self.driver,self.occupation_detail).send_keys('Teacher')

        if occupation == 'Food / Logistic Delivery':
            scroll_to_bottom(self.driver)
            transport_list = ['Walk', 'Bicycle / PMD', 'Motorcycle', 'Car / Van', 'Others']
            transport = choice(transport_list)
            data['transport_mode'] = transport
            wait_element(self.driver, (By.XPATH, f'(//*[text()="{transport}"])[last()]/../button')).click()
            if transport == 'Others':
                wait_element(self.driver,self.transport_mode_detail).send_keys('Grab')
        scroll_to_bottom(self.driver)
        wait_element(self.driver,self.next_btn).click()
        return data

    def input_dob(self, year):
        wait_element(self.driver,self.dob).click()
        wait_element(self.driver,self.date_picker_year).click()
        wait_element(self.driver,(By.XPATH, f'//*[text()="{year}"]')).click()
        wait_element(self.driver,self.ok_btn).click()

    def choose_start_date(self):
        wait_element(self.driver,self.start_date).click()
        wait_element(self.driver,self.ok_btn).click()

    def click_checkbox(self):
        wait_element(self.driver,self.check_box).click()

    def click_next_btn(self):
        wait_element(self.driver,self.next_btn).click()


class CdwQuotePage():
    def __init__(self, driver):
        self.driver                               = driver
        self.get_started_btn                      = By.XPATH, '//button[text()="GET STARTED"]'
        self.next_btn                             = By.XPATH, '//*[text()="NEXT"][not(@disabled)]'
        self.ss2                                  = By.XPATH, '//*[text()="Section 2"]/../following-sibling::button[1]'
        self.option_b                             = By.XPATH, '//*[text()="Option B"]/../button'
        self.reduce_excess                        = By.XPATH, '//*[(text()="What amount do you want to lower your excess to?")]/following-sibling::div[1]/button'
        self.reduce_excess_value                  = By.XPATH, '//*[(text()="What amount do you want to lower your excess to?")]/following-sibling::div[1]'
        self.daily_rate                           = By.XPATH, '//*[text()="Your Daily Rate:"]/following-sibling::h1'
        self.premium                              = By.XPATH, '//*[contains(text(), "Total:")]/following-sibling::div'
        self.individual_option                    = By.XPATH, '//*[text()="Individual"]/..'
        self.young_and_inexperienced_yes_option   = By.XPATH, '//*[text()="Are you a Young & Inexperienced Driver?"]/following-sibling::div//img[@src="/img/cdw-question/check.svg"]'
        self.young_and_inexperienced_no_option    = By.XPATH, '//*[text()="Are you a Young & Inexperienced Driver?"]/following-sibling::div//img[@src="/img/cdw-question/cross.svg"]'
        self.additional_coverage_yes_option       = By.XPATH, '//*[text()="Do you require more additional private settlement coverage?"]/following-sibling::div//img[@src="/img/cdw-question/check.svg"]'
        self.additional_coverage_no_option        = By.XPATH, '//*[text()="Do you require more additional private settlement coverage?"]/following-sibling::div//img[@src="/img/cdw-question/cross.svg"]'
        self.quote_checkbox1                      = By.XPATH, '//*[contains(text(), "I understand that I notify claims within 30 days")]/../button'
        self.quote_checkbox2                      = By.XPATH, '//*[contains(text(), "I understand that CDW pays out benefits")]/../button'

        #CDWY
        self.rented_vehicle                       = By.XPATH, '//*[text()="Rented"]/..'
        self.personal_vehicle                     = By.XPATH, '//*[text()="Personal"]/..'

        #newdrivers
        self.acknowledge_btn                      = By.XPATH, '//button[text()="I acknowledge"]'
        self.vehicle_reg                          = By.NAME, 'vehicle_reg'
        self.combined_excess_input                = By.NAME, 'combined_excess'
        self.yid_excess_list                      = By.NAME, 'suitablePricingObject'
        self.purchase_now_btn                     = By.XPATH, '//button[text()="PURCHASE NOW"]'
        self.maximum_benefit_claim                = By.XPATH, '//*[text()="MAXIMUM BENEFIT PER CLAIM"]/following-sibling::div'
        self.buy_now_btn                          = By.XPATH, '//button[text()="BUY NOW"]'
        self.your_total_payable                   = By.XPATH, '//*[text()="YOUR TOTAL PAYABLE IS:"]/following-sibling::div[1]'
        self.weekly_package                       = By.XPATH, '//*[text()="WEEKLY PLAN"]'
        self.monthly_package                      = By.XPATH, '//*[text()="MONTHLY PLAN"]'
        self.policy_start                         = By.XPATH, '//*[text()="SELECT YOUR POLICY START:"]/following-sibling::div[1]'
        self.ok_btn                               = By.XPATH, '//*[text()="Ok"][not(@disabled)]/..'
        self.continue_btn                         = By.XPATH, '//button[text()="CONTINUE"]'
        self.unspecified_option                   = By.XPATH, '//*[text()="No, it is unspecified."]/../button'
        self.list_acknowledge_checkbox            = '//*[contains(text(),"Insurer’s own damage YID excess:")]/../following-sibling::div[1]/button'

    def choose_individual_option(self):
        wait_element(self.driver, self.get_started_btn).click()
        wait_element(self.driver, self.individual_option).click()

    def is_young_and_inexperienced(self):
        wait_element(self.driver, self.young_and_inexperienced_yes_option).click()

    def is_not_young_and_inexperienced(self):
        wait_element(self.driver, self.young_and_inexperienced_no_option).click()

    def choose_additional_coverage(self):
        wait_element(self.driver, self.additional_coverage_yes_option).click()
        wait_element(self.driver, self.next_btn).click()

    def not_choose_additional_coverage(self):
        wait_element(self.driver, self.additional_coverage_no_option).click()
        wait_element(self.driver, self.next_btn).click()

    def choose_rented_vehicle(self):
        wait_element(self.driver, self.rented_vehicle).click()
        wait_element(self.driver, self.next_btn).click()

    def choose_personal_vehicle(self):
        wait_element(self.driver, self.personal_vehicle).click()

    def choose_vehicle(self):
        vehicle_list = ['Car', 'Van', 'Motorcycle']
        vehicle = choice(vehicle_list)
        wait_element(self.driver,(By.XPATH, f'//*[text()="{vehicle}"]/..')).click()
        return vehicle

    def choose_ss1_ss2(self):
        data = {}
        ss1_list = [0, 1000, 1400, 1500, 1800, 2000, 2500, 3000, 3500, 4000]
        ss1 = choice(ss1_list)
        wait_element(self.driver,(By.XPATH, f'//*[text()="Section 1"]/../following-sibling::button[text()="{ss1}"]')).click()

        wait_element(self.driver,self.ss2).click()
        data['ss1'] = f'${ss1}'
        data['ss2'] = wait_element(self.driver,self.ss2).text
        return data

    def choose_option_b(self):
        wait_element(self.driver,self.option_b).click()

    def choose_combine_excess(self):
        scroll_to_bottom(self.driver)
        combine_excess_list = [2000, 2500, 3000, 3500, 4000]
        combine_excess = choice(combine_excess_list)
        wait_element(self.driver,(By.XPATH, f'//*[text()="Combined Excess"]/../following-sibling::button[text()="{combine_excess}"]')).click()
        return combine_excess

    def choose_yid_type(self):
        type_list = ['Additional', 'Lump Sum']
        type = choice(type_list)
        wait_element(self.driver, (By.XPATH, f'//*[text()="{type}"]')).click()

    def choose_yid_excess_list(self):
        yid_access_list = [1000, 1500, 2000, 2500, 3000, 3500, 4000]
        yid_access = choice(yid_access_list)
        wait_element(self.driver,(By.XPATH, f'//*[contains(text(),"Insurer’s own damage YID excess:")]/..//option[@value="{yid_access}"]')).click()

    def choose_reduce_excess(self):
        wait_element(self.driver,self.reduce_excess).click()
        return wait_element(self.driver,self.reduce_excess_value).text

    def get_daily_rate(self):
        return wait_element(self.driver,self.daily_rate).text

    def click_on_quote_page_checkbox(self):
        wait_element(self.driver, self.quote_checkbox1).click()
        wait_element(self.driver, self.quote_checkbox2).click()

    def get_premium(self):
        return wait_element(self.driver,self.premium).text

    def click_next_btn(self):
        wait_element(self.driver,self.next_btn).click()

    #CDWY
    def click_purchase_now_btn(self):
        wait_element(self.driver, self.purchase_now_btn).click()

    def click_on_acknowledge_btn(self):
        wait_element(self.driver, self.acknowledge_btn).click()

    def choose_unspecified_option(self):
        wait_element(self.driver, self.unspecified_option).click()

    def click_on_all_acknowledge_checkbox(self):
        list_acknowledge_checkbox = findElements_xpath(self.driver, self.list_acknowledge_checkbox)
        for i in list_acknowledge_checkbox:
            i.click()
    def input_combined_excess(self):
        wait_element(self.driver, self.combined_excess_input).send_keys('1000')

    def get_maximum_benefit_claim(self):
        return wait_element(self.driver, self.maximum_benefit_claim).text

    def click_buy_now_btn(self):
        wait_element(self.driver, self.buy_now_btn).click()

    def get_your_total_payable(self):
        return wait_element(self.driver, self.your_total_payable).text

    def input_vehicle_reg(self, vehicle_reg):
        wait_element(self.driver, self.vehicle_reg).send_keys(vehicle_reg)

    def choose_start_date(self):
        wait_element(self.driver, self.policy_start).click()
        today_plus_1 = (datetime.date.today() + datetime.timedelta(days=1)).day
        wait_element(self.driver, (By.XPATH, f'//button[text()="{today_plus_1}"]')).click()

    def choose_weekly_package(self):
        wait_element(self.driver, self.weekly_package).click()

    def choose_monthly_package(self):
        wait_element(self.driver, self.monthly_package).click()

    def click_continue_btn(self):
        wait_element(self.driver, self.continue_btn).click()

class ZeekQuotePage():
    def __init__(self, driver):
        self.driver                        = driver
        self.driver_occupation             = By.XPATH, '//*[text()="Drivers (Cars, Vans)"]/../button'
        self.moto_occupation               = By.XPATH, '//*[text()="Motorcyclists or Cyclists"]/../button'
        self.pa_driver_plan                = By.XPATH, '//*[text()="S$10,000 Sum Assured"]/../button'
        self.pa_moto_plan                  = By.XPATH, '//*[text()="S$5,000 Sum Assured"]/../button'
        self.next_btn                      = By.XPATH, '//*[text()="NEXT"]'

    def choose_driver_occupation(self):
        wait_element(self.driver,self.driver_occupation).click()
        wait_element(self.driver,self.next_btn).click()

    def choose_moto_occupation(self):
        wait_element(self.driver,self.moto_occupation).click()
        wait_element(self.driver,self.next_btn).click()

    def choose_flep_driver_plan(self):
        plan_list = ['S$80 daily cash benefit', 'S$100 daily cash benefit']
        plan = choice(plan_list)
        choose_plan = wait_element(self.driver,(By.XPATH, f'//*[text()="{plan}"]/../button'))
        choose_plan.click()
        wait_element(self.driver,self.next_btn).click()
        return plan

    def choose_flep_moto_plan(self):
        plan_list = ['S$40 daily cash benefit', 'S$50 daily cash benefit']
        plan = choice(plan_list)
        choose_plan = wait_element(self.driver,(By.XPATH, f'//*[text()="{plan}"]/../button'))
        choose_plan.click()
        wait_element(self.driver,self.next_btn).click()
        return plan

    def choose_pa_driver_plan(self):
        wait_element(self.driver,self.pa_driver_plan).click()
        wait_element(self.driver,self.next_btn).click()

    def choose_pa_moto_plan(self):
        wait_element(self.driver,self.pa_moto_plan).click()
        wait_element(self.driver,self.next_btn).click()

    def choose_moto_occupation_plan(self):
        plan_list = ['S$40 daily cash benefit', 'S$50 daily cash benefit']
        plan = choice(plan_list)
        choose_plan = wait_element(self.driver,(By.XPATH, f'//*[text()="{plan}"]/../button'))
        choose_plan.click()
        wait_element(self.driver,self.next_btn).click()


class HealthQuotePage():
    def __init__(self, driver):
        self.driver                     = driver
        self.dependent_plan             = By.XPATH, '//*[text()="LEVEL I"]'
        self.dependent_num              = By.XPATH, '//*[text()="Number of your Dependents"]/following-sibling::div//button[2]'
        self.total_annual_payable       = By.XPATH, '//*[text()="YOUR TOTAL ANNUAL PAYABLE IS:"]/following-sibling::div[1]'
        self.next_btn                   = By.XPATH, '//*[text()="NEXT"]'
        self.skip_btn                   = By.XPATH, '//*[text()="SKIP"]'
        self.plan_1C                   = By.XPATH, '//*[contains(text(), "PLAN 1C")]/..'
        self.plan_2C                   = By.XPATH, '//*[contains(text(), "PLAN 2C")]/..'

    def choose_random_plan_for_primary(self):
        list_of_plan = ['PLAN 1A', 'PLAN 1B', 'PLAN 1C', 'PLAN 2A', 'PLAN 2B', 'PLAN 2C', 'PLAN 3', 'PLAN 4', 'PLAN 5', 'PLAN 6']
        plan = choice(list_of_plan)
        wait_element(self.driver, (By.XPATH, f'//*[contains(text(), "{plan}")]/..')).click()
        wait_element(self.driver,self.next_btn).click()
        return plan

    def choose_random_plan_for_dependent(self):
        list_of_plan = ['PLAN 1A', 'PLAN 1B', 'PLAN 2A', 'PLAN 2B', 'PLAN 3', 'PLAN 4', 'PLAN 5', 'PLAN 6']
        plan = choice(list_of_plan)
        wait_element(self.driver, (By.XPATH, f'//*[contains(text(), "{plan}")]/..')).click()
        wait_element(self.driver,self.next_btn).click()
        return plan

    def choose_plan_failed_Ewallet(self):
        wait_element(self.driver, self.plan_1C).click()
        wait_element(self.driver,self.next_btn).click()

    def choose_plan_failed_card(self):
        wait_element(self.driver, self.plan_2C).click()
        wait_element(self.driver,self.next_btn).click()

    def get_total_annual_payable(self):
        return wait_element(self.driver, self.total_annual_payable).text
    def choose_dependent_num(self):
        wait_element(self.driver,self.dependent_num).click()

    def click_skip_btn(self):
        wait_element(self.driver,self.skip_btn).click()

    def click_next_btn(self):
        wait_element(self.driver,self.next_btn).click()


class PetQuotePage():
    def __init__(self, driver):
        self.driver                     = driver
        self.dog_pawtection_btn         = By.XPATH, '//*[text()="DOG PAWTECTION"]/..'
        self.cat_purrtection_btn        = By.XPATH, '//*[text()="CAT PURRTECTION"]/..'
        self.next_btn                   = By.XPATH, '//button[text()="NEXT"]'
        self.add_more_pet_btn           = By.XPATH, '//*[text()="Number of your Pets"]/following-sibling::div//button[contains(@class, "bg-main-green")]'
        self.type_of_dog_dropdown       = By.XPATH, '(//*[text()="Type of Dog"]/following-sibling::div/select)[1]'
        self.total_annual_payable       = By.XPATH, '//*[text()="YOUR TOTAL ANNUAL PAYABLE IS:"]/following-sibling::div[1]'

        self.review_class_of_pet        = By.XPATH, '//*[contains(text(), "Classification: ")]/span'
        self.review_type_of_dog         = By.XPATH, '//*[contains(text(), "Type of dog: ")]/span'
        self.review_type_of_cat         = By.XPATH, '//*[contains(text(), "Type of cat: ")]/span'

    def choose_dog_pawtection(self):
        wait_element(self.driver, self.dog_pawtection_btn).click()

    def choose_cat_purrtection(self):
        wait_element(self.driver, self.cat_purrtection_btn).click()

    def click_next_btn(self):
        wait_element(self.driver, self.next_btn).click()

    def click_on_add_more_pet_btn(self):
        wait_element(self.driver, self.add_more_pet_btn).click()

    def choose_random_type_of_dog(self):
        wait_element(self.driver, self.type_of_dog_dropdown).click()
        random_index = randint(0, 100)
        class_of_dog = wait_element(self.driver, (By.XPATH, f'(//*[text()="Type of Dog"]/following-sibling::div/select)[1]/option[{random_index}]')).text
        wait_element(self.driver, (By.XPATH, f'(//*[text()="Type of Dog"]/following-sibling::div/select)[1]/option[{random_index}]')).click()

        type_of_dog = wait_element(self.driver, (By.XPATH, '//*[contains(text(), "PET #")]/following-sibling::div[2]')).text
        wait_element(self.driver, self.next_btn).click()
        return class_of_dog.strip(), type_of_dog.strip()

    def get_class_and_type_of_dog(self):
        data = {}
        data['class_of_dog'] = wait_element(self.driver, self.review_class_of_pet).text
        data['type_of_dog'] = wait_element(self.driver, self.review_type_of_dog).text
        return data

    def get_class_and_type_of_cat(self):
        data = {}
        data['class_of_cat'] = wait_element(self.driver, self.review_class_of_pet).text
        data['type_of_cat'] = wait_element(self.driver, self.review_type_of_cat).text
        return data


