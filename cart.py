import re
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Cart:

    def __init__(self, driver):
        self.driver = driver
        self.cart_url = 'https://store.23andme.com/en-us/cart/'
        self.shipping_url = 'https://store.23andme.com/en-us/shipping/'
        self.listkitnames = [
            'John Doe',
            'Jeremy Smith',
            'Allison Dorner',
            'Bobby George',
            'Ashley Smith',
            'Sara Smalls',
            'Brittney Henderson',
            'Larry Mar',
            'Jos Levine',
            'Bryan Henry',
        ]

    def verifyheromsg(self):
        """ Verify the hero message is displayed """
        print('verifyheromsg')
        herotext = 'Buy one kit, get 10% off additional kits.'
        assert herotext in self.driver.page_source

    def addkitnames(self, names):
        """ Create a list of kit names """
        print('addkitnames')
        for n in names:
            self.listkitnames.append(n)

    def verifypagetitle(self, title):
        """ Verify the title of the page is correct """
        print('verifypagetitle')
        if '23andMe' not in title:
            raise Exception('Um, something appears to have gone wrong.')
        assert 'Store - 23andMe - DNA Genetic Testing & Analysis' in title
        self.driver.save_screenshot('testPageTitle.png')

    def additemstocart(self, kits):
        """ Add kits into the shopping cart """
        print('additemstocart')
        try:
            for n in xrange(1, kits):
                WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'img.js-add-kit')))
                self.driver.find_element_by_css_selector('img.js-add-kit').click()
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as env:
            print(env.message)
            print(env.stacktrace)
        finally:
            self.driver.save_screenshot('additemstocart.png')

    def testaddkitlink(self):
        """ Verify that the Add Kit link is working """
        print('testaddkitlink')
        try:
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.LINK_TEXT, 'Add a kit.')))
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as enve:
            print(enve.message)
            print(enve.stacktrace)
        finally:
            print(self.driver.session_id)
            self.driver.save_screenshot('testAddKitLink.png')

    def getcartqty(self):
        """ Get the number of kit items in your cart """
        print('getcartqty')
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'kit-quantity')))
        cartqty = int(self.driver.find_element_by_class_name('kit-quantity').text)
        return cartqty

    def getorderqty(self):
        """ Get the number of kits in the order table """
        WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'section.kit-list>.js-kit-item.cart-item-row')))
        orderqty = len(self.driver.find_elements_by_css_selector('section.kit-list>.js-kit-item.cart-item-row'))
        return orderqty

    def gettotalqty(self):
        """ Get total quantity from the totals section """
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.single.quantity-number')))
        totalqty = int(self.driver.find_element_by_css_selector('.single.quantity-number').text)
        return totalqty

    def getsubtotalqty(self):
        """ Get the qty in the subtotal label """
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.cart-details-row:nth-child(3)>.price-summary>div.label')))
        subtotalqty = int(re.sub(r'\D', '', self.driver.find_element_by_css_selector('div.cart-details-row:nth-child(3)>.price-summary>div.label').text))
        return subtotalqty

    def getgrandtotalqty(self):
        """ Get the qty in the grand total label """
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.cart-details-row:nth-child(5)>.price-summary>div.label')))
        grandtotalqty = int(re.sub(r'\D', '', self.driver.find_element_by_css_selector('div.cart-details-row:nth-child(5)>.price-summary>div.label').text))
        return grandtotalqty

    def getgrandtotalamt(self):
        """ Get the grand total amount from the shopping cart """
        grandamt = '$' + '{0:.2f}'.format(int((199.00 * self.getgrandtotalqty()) - (199.00 * (self.getgrandtotalqty() - 1) * 0.1)))
        return grandamt

    def kitcounter(self, numkits):
        """ Verify all quantities are correct (5 places) """
        if numkits > 1:
            cartqty = self.getcartqty()
            orderqty = self.getorderqty()
            totalqty = self.gettotalqty()
            subtotalqty = self.getsubtotalqty()
            grandtotalqty = self.getgrandtotalqty()
            assert orderqty == totalqty == cartqty == subtotalqty == grandtotalqty

        elif numkits == 1:
            cartqty = self.getcartqty()
            orderqty = self.getorderqty()
            totalqty = self.gettotalqty()
            grandtotalqty = self.getgrandtotalqty()
            assert cartqty == orderqty == totalqty == grandtotalqty
        else:
            raise Exception('Um, something appears to have gone wrong.')
        self.driver.save_screenshot('kitcounter.png')

    def verifysubtotal(self):
        """ Create method to verify the subtotal """
        # @TODO count number of kits with discounts and compare against the displayed subtotal
        try:
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, "div.cart-details-row:nth-child(3)>.price-summary>div.price-display")))
            subamt = self.driver.find_element_by_css_selector("div.cart-details-row:nth-child(3)>.price-summary>div.price-display").text
            calcsubamt = '$' + '{0:.2f}'.format(int(199.00 * self.getsubtotalqty()))
            assert subamt == calcsubamt
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as env:
            print(env.message)
            print(env.stacktrace)
        finally:
            self.driver.save_screenshot('verifysubtotal.png')

    def verifysavings(self):
        """ Create method to verify the savings (after discount) """
        # @TODO count number of kits with savings and compare against displayed savings
        try:
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, "div.cart-details-row:nth-child(4)>.price-summary>div.price-display")))
            savamt = self.driver.find_element_by_css_selector(
                "div.cart-details-row:nth-child(4)>.price-summary>div.price-display").text
            calcsavamt = '$' + '{0:.2f}'.format((199.00 * (self.getsubtotalqty() - 1) * 0.1))
            assert savamt == calcsavamt
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as env:
            print(env.message)
            print(env.stacktrace)
        finally:
            self.driver.save_screenshot('verifysavings.png')

    def verifygrandtotal(self):
        """ Create method to verify the grand total (subtotal - savings) """
        # @TODO count number of kits and subtract against savings and compare against displayed grand total
        try:
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, "div.cart-details-row:nth-child(5)>.price-summary>div.price-display")))
            grandamt = self.driver.find_element_by_css_selector(
                "div.cart-details-row:nth-child(5)>.price-summary>div.price-display").text
            calcgrandamt = '$' + '{0:.2f}'.format((199.00 * self.getgrandtotalqty()) - (199.00 * (self.getgrandtotalqty() - 1) * 0.1))
            assert grandamt == calcgrandamt
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as env:
            print(env.message)
            print(env.stacktrace)
        finally:
            self.driver.save_screenshot('verifygrandtotal.png')

    def verifycontbtn(self):
        """ Create a method to verify if continue button is disabled or not """
        print('verifycontbtn')
        try:
            WebDriverWait(self.driver, 30).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'input.submit.button-disabled')))
            self.driver.find_element_by_css_selector('input.submit.button-continue').click()
        except TimeoutException as te:
            print(te.message)
            print(te.stacktrace)
        except ElementNotVisibleException as enve:
            print(enve.stacktrace)
            print(enve.message)
        self.driver.save_screenshot('verifycontbtn.png')

    def sendkitnames(self):
        """ Create method to check all kits have names """
        print('sendkitnames')
        allkitnames = self.driver.find_elements_by_css_selector('input.js-kit-name')
        for kn in allkitnames:
            kn.clear()
            kn.send_keys(self.listkitnames.pop())
        self.driver.save_screenshot('verifykitnames.png')
