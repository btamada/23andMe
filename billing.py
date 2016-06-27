import time
from cart import Cart
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Billing:

    def __init__(self, driver):
        self.driver = driver
        self.cartInst = Cart(self.driver)

    def verifyContent(self):
        """ Verify billing content is correct """
        self.verifyStepTitle()
        self.verifyPaymentSection()
        self.verifyBillingSection()
        self.clickContBtn()

    def verifyStepTitle(self):
        """ Verify step title is correct """
        print('verifystoptitle')
        time.sleep(10)
        title = self.driver.find_element_by_css_selector('.step.active>span.step-title').text
        color = self.driver.find_element_by_css_selector('.step.active>span.step-title').value_of_css_property('color')
        assert title == 'billing' and color == 'rgba(219, 9, 98, 1)'

    def verifyPaymentSection(self):
        """ Verify payment section content is correct """
        print('verifypaymentsection')
        time.sleep(10)
        assert 'Payment' in self.driver.page_source
        assert 'Billing address' in self.driver.page_source
        assert 'Card number' in self.driver.page_source
        assert 'Exp date' in self.driver.page_source
        assert 'CVV' in self.driver.page_source
        assert self.cartInst.getgrandtotalamt() in self.driver.page_source

    def verifyBillingSection(self):
        """ Verify billing address content is correct """
        print('verifybillingsection')
        time.sleep(10)
        assert 'Use same as shipping' in self.driver.page_source
        assert 'Enter a new address' in self.driver.page_source

    # click the continue button
    def clickContBtn(self):
        """ Click on the continue button """
        print('clickcontbtn')
        try:
            assert 'shipping' in self.driver.current_url
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.submit.button-continue')))
            self.driver.find_element_by_css_selector('input.submit.button-continue').click()
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as enve:
            print(enve.stacktrace)
            print(enve.message)
        self.driver.save_screenshot('billingclickcontbtn.png')