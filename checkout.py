import unittest
import logging
import time
from cart import Cart
from billing import Billing
from shipping import Shipping
from verifyaddy import VerifyAddy
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Test23andMeWebsite(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome('/Users/User1/Downloads/chromedriver')
        self.driver.get('http://store.23andme.com/en-us/')
        time.sleep(5)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        # debug log
        self.debugLogger = logging.getLogger('debuglogger')
        debug_handler = logging.FileHandler('debug.log')
        debug_handler.setFormatter(formatter)
        self.debugLogger.addHandler(debug_handler)

        # info log
        self.infoLogger = logging.getLogger('infologger')
        info_handler = logging.FileHandler('info.log')
        info_handler.setFormatter(formatter)
        self.infoLogger.addHandler(info_handler)

        # error log
        self.errLogger = logging.getLogger('errlogger')
        err_handler = logging.FileHandler('err.log')
        err_handler.setFormatter(formatter)
        self.errLogger.addHandler(err_handler)

        self.cartInst = Cart(self.driver)
        self.billInst = Billing(self.driver)
        self.shipInst = Shipping(self.driver)
        self.verifyAddyInst = VerifyAddy(self.driver)
        self.driver.save_screenshot('setup.png')

    """ Check if the cart is empty or not """
    def testWebsiteFunc(self):
        print('testwebsitefunc')
        try:
            WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.LINK_TEXT, 'Add a kit.')))
            addkitlink = self.driver.find_element_by_link_text('Add a kit.')
            if addkitlink:
                print('CART EMPTY')
                addkitlink.click()
                self.cartInst.additemstocart(5)
                self.cartInst.sendkitnames()
                self.cartInst.verifysubtotal()
                self.cartInst.verifysavings()
                self.cartInst.verifygrandtotal()
                self.cartInst.verifycontbtn()
                self.shipInst.fillOutForm()
                assert 'verifyaddress' in self.driver.current_url
                self.verifyAddyInst.verifyContent()
                assert 'payment' in self.driver.current_url
                self.billInst.verifyContent()
            else:
                print('CART NOT EMPTY')
                self.cartInst.sendkitnames()
                self.cartInst.verifysubtotal()
                self.cartInst.verifysavings()
                self.cartInst.verifygrandtotal()
                self.cartInst.verifycontbtn()
                self.shipInst.fillOutForm()
                assert 'verifyaddress' in self.driver.current_url
                self.verifyAddyInst.verifyContent()
                assert 'payment' in self.driver.current_url
                self.billInst.verifyContent()
        except TimeoutException as te:
            self.errLogger.error(te.message)
            self.errLogger.error(te.stacktrace)
        except ElementNotVisibleException as enve:
            self.errLogger.error(enve.message)
            self.errLogger.error(enve.stacktrace)
        finally:
            self.debugLogger.debug(self.driver.session_id)
            self.driver.save_screenshot('testwebsitefunc.png')

    @classmethod
    def tearDown(self):
        self.driver.save_screenshot('teardown.png')
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
