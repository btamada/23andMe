from shipping import Shipping
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class VerifyAddy:

    def __init__(self, driver):
        self.driver = driver
        self.shipInst = Shipping(self.driver)

    def verifyContent(self):
        """ Verify the content on the verify address page is correct """
        print('verifycontent')
        self.verifyStepTitle()
        self.clickEditShipAddy()
        self.clickVerifiedAddy()

    def verifyStepTitle(self):
        """ Verify the step title of this page """
        print('verifysteptitle')
        """ Verify step title and color """
        title = self.driver.find_element_by_css_selector('.step.active>span.step-title').text
        color = self.driver.find_element_by_css_selector('.step.active>span.step-title').value_of_css_property('color')
        assert title == 'shipping' and color == 'rgba(219, 9, 98, 1)'

    def clickUnverifiedAddy(self):
        """ Click on the unverified address link """
        print('clickunverifiedaddy')
        try:
            self.checkUnverifiedSection()
            WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'input.button-continue.use-unverified')))
            self.driver.find_element_by_css_selector('input.button-continue.use-unverified').click()
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as env:
            print(env.message)
            print(env.stacktrace)

    def clickVerifiedAddy(self):
        """ Click on the verified address link """
        print('clickverifiedaddy')
        try:
            self.checkVerifiedSection()
            WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'input.button-continue')))
            self.driver.find_element_by_css_selector('input.button-continue').click()
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as env:
            print(env.message)
            print(env.stacktrace)

    def clickEditShipAddy(self):
        """ Click on the Edit Shipping Address link """
        print('clickeditshipaddy')
        try:
            WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'button-edit')))
            self.driver.find_element_by_class_name('button-edit').click()
            WebDriverWait(self.driver, 10).until(ec.text_to_be_present_in_element((By.TAG_NAME, 'h2'), 'Shipping address'))
            assert 'shipping' in self.driver.current_url
            self.shipInst.clickContBtn()
            assert 'verifyaddress' in self.driver.current_url
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as env:
            print(env.message)
            print(env.stacktrace)

    def checkUnverifiedSection(self):
        """ Check the unverified address section """
        print('checkunverifiedsection')
        # TODO the correct way to do this is to parse the address section and verify the data programmatically
        assert 'Unverified Address' in self.driver.page_source
        assert 'John Doe' in self.driver.page_source
        assert 'Google' in self.driver.page_source
        assert '1600 Amphitheatre Parkway, 1234' in self.driver.page_source
        assert 'Mountain View, CA 94043' in self.driver.page_source
        assert 'US' in self.driver.page_source

    def checkVerifiedSection(self):
        """ Check the verified address section """
        print('checkverifiedsection')
        # TODO the correct way to do this is to parse the address section and verify the data programmatically
        assert 'Verified Address' in self.driver.page_source
        assert 'John Doe' in self.driver.page_source
        assert 'Google' in self.driver.page_source
        assert '1600 AMPHITHEATRE PKWY, # 1234' in self.driver.page_source
        assert 'MOUNTAIN VIEW, CA 94043-1351' in self.driver.page_source
        assert 'US' in self.driver.page_source