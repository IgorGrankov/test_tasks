__author__ = 'igorgrankov'

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage(object):
    """
    Class contains abstraction for main page element & methods
    """
    def __init__(self, browser):
        self.browser = browser

    def go_to_login(self):
        login_link = self.browser.find_element_by_css_selector(
            'ul.menu li:nth-child(1) a')
        login_link.click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                            'sb-conteiner')))


class LoginPage(object):
    """
    Class contains abstraction for login page element & methods
    """
    def __init__(self, browser):
        self.browser = browser
        # Set test data as constants, but I understand that put then into
        # methods is better solution, just to save our time
        self.LOGIN = 'igorgrnv@gmail.com'
        self.PASSWORD = 'MyPass123'

    def fill_login_form(self):
        username_field = self.browser.find_element_by_id('email')
        password_field = self.browser.find_element_by_id('pass')

        username_field.send_keys(self.LOGIN)
        password_field.send_keys(self.PASSWORD)

    def click_submit(self):
        login_button = self.browser.find_element_by_name('login')
        login_button.click()


class Test(unittest.TestCase):
    """
    Test class implements login test scenarios

    1. Open main page
    2. Go to login form
    3. Click 'Login' button (Localization looks odd)
    4. Assert invalid credentials error is shown
    5. Fill form with valid credential
    6. Click 'Login'
    7. Assert that hat exit link appears
    """

    def setUp(self):
        self.index_page = 'http://fibogo.trustingdomains.com/'
        self.browser = webdriver.Firefox()
        self.browser.get(self.index_page)
        self.browser.set_window_size(1280, 800)
        self.browser.implicitly_wait(5)
        self.main_page = MainPage(self.browser)
        self.login = LoginPage(self.browser)

    def test_login_to_fibogo_negative(self):
        # Open main page
        # Click Login link
        self.main_page.go_to_login()
        self.login.click_submit()

        # On opened login form click 'Submit'
        error = self.browser.find_element_by_css_selector(
            'div.error p.error')

        # Assert error message is show
        self.assertEqual('Invalid username or password', error.text)

        # Fill form and click submit
        self.login.fill_login_form()
        self.login.click_submit()
        exit_link = self.browser.find_element_by_xpath(
            "//*[text()[contains(.,'Exit')]]")

        # Assert that exit link appears
        # BTW login & registration should be hidden - it is a bug,
        # but I didn't cover it
        self.assertTrue(exit_link.is_displayed())

    def tearDown(self):
        self.browser.close()

if __name__ == "__main__":
    unittest.main()
