import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException


class Shipping:

    def __init__(self, driver):
        self.driver = driver

    def verifyStepTitle(self):
        """ Verify the step title and color """
        print('verifysteptitle')
        title = self.driver.find_element_by_css_selector('.step.active>span.step-title').text
        color = self.driver.find_element_by_css_selector('.step.active>span.step-title').value_of_css_property('color')
        assert title == 'shipping' and color == 'rgba(219, 9, 98, 1)'

    def fillOutForm(self):
        """ Fill out the form """
        print('filloutform')
        try:
            assert 'shipping' in self.driver.current_url
            self.verifyStepTitle()
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_first_name')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_last_name')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_company')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_address')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_address2')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_city')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_state')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_postal_code')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_country')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_shipping_method')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_email')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_int_phone')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_add_gift')))
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'id_gift_message')))
            fname = self.driver.find_element_by_id('id_first_name')
            fname.clear()
            fname.send_keys('John')
            lname = self.driver.find_element_by_id('id_last_name')
            lname.clear()
            lname.send_keys('Doe')
            company = self.driver.find_element_by_id('id_company')
            company.clear()
            company.send_keys('Google')
            address = self.driver.find_element_by_id('id_address')
            address.clear()
            address.send_keys('1600 Amphitheatre Parkway')
            address2 = self.driver.find_element_by_id('id_address2')
            address2.clear()
            address2.send_keys('1234')
            city = self.driver.find_element_by_id('id_city')
            city.clear()
            city.send_keys('Mountain View')
            Select(self.driver.find_element_by_id('id_state')).select_by_value('CA')
            postal_code = self.driver.find_element_by_id('id_postal_code')
            postal_code.clear()
            postal_code.send_keys('94043')
            Select(self.driver.find_element_by_id('id_country')).select_by_value('US')
            Select(self.driver.find_element_by_id('id_shipping_method')).select_by_value('matrixrate_express')
            email = self.driver.find_element_by_id('id_email')
            email.clear()
            email.send_keys('jdoe@mail.com')
            self.driver.find_element_by_class_name('selected-flag').click()
            self.driver.find_element_by_xpath("//ul[@class='country-list']/li[1]").click()
            phone = self.driver.find_element_by_id('id_int_phone')
            phone.clear()
            phone.send_keys('4251234567')
            addgift = self.driver.find_element_by_id('id_add_gift')
            addgift.click()
            giftmsg = self.driver.find_element_by_id('id_gift_message')
            giftmsg.clear()
            giftmsg.send_keys('I just wanted to show my thanks for helping me out the other day!')
            self.giftMsgPopup()
            self.clickContBtn()
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as env:
            print(env.message)
            print(env.stacktrace)
        finally:
            self.driver.save_screenshot('filloutform.png')

    def giftMsgPopup(self):
        """ Verify gift message popup """
        print('giftmsgpopup')
        try:
            gifttip = self.driver.find_element_by_class_name('gift-tip')
            ActionChains(self.driver).click_and_hold(gifttip).perform()
            gifttiptext = 'Your gift message will be printed on the packing slip for the entire order. The price will not appear.'
            WebDriverWait(self.driver, 10).until(ec.text_to_be_present_in_element((By.CLASS_NAME, 'tpd-content'), gifttiptext))
            time.sleep(10)
            fromgifttip = self.driver.find_element_by_class_name('tpd-content').text
            time.sleep(10)
            ActionChains(self.driver).move_by_offset(10, 10).perform()
            assert gifttiptext == fromgifttip
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as env:
            print(env.message)
            print(env.stacktrace)
        finally:
            self.driver.save_screenshot('giftmsgpopup.png')

    def verifyFormFilled(self):
        """ Verify form information has been filled out """
        # TODO check field to see if they have been filled out
        print('verifyformfilled')

    def clickContBtn(self):
        """ Click on the continue button """
        print('clickcontbtn')
        try:
            assert 'shipping' in self.driver.current_url
            WebDriverWait(self.driver, 30).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, 'input.submit.button-continue')))
            self.driver.find_element_by_css_selector('input.submit.button-continue').click()
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as enve:
            print(enve.stacktrace)
            print(enve.message)
        finally:
            self.driver.save_screenshot('shippingclickcontbtn.png')
