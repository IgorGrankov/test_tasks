import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class NascarTest(unittest.TestCase):
    # Set constants for test class
    DEFAULT_TIMEOUT = 45
    CHROME_DRIVER_PATH = '/Users/igorgrankov/learning/Omnigon/chromedriver'
    PREFIX = str(time.time())
    EMAIL = '{}igorgrnv@gmail.com'.format(PREFIX)
    FIRST_NAME = 'Igor'
    LAST_NAME = 'Grankov'
    PASSWORD = 'MyPass123'

    def setUp(self):
        self.browser = webdriver.Chrome(self.CHROME_DRIVER_PATH)
        self.browser.get("http://www.nascar.com")
        self.browser.set_window_size(1280, 800)

        # I was trying to avoid sleep, but still didn't figure out how
        # WebDriverWait has no effect
        self.wait = WebDriverWait(self.browser, self.DEFAULT_TIMEOUT)
        time.sleep(5)

    def registration(self):
        # Click on registration link
        register = self.browser.find_element_by_xpath(
            '//*[@id="registerOrLogin"]/a[2]')
        register.click()

        # Wait until form is loaded
        form = self.wait.until(
            EC.presence_of_element_located((By.ID, "gigya-register-screen"))
        )

        # Set focus on registration form
        actions = ActionChains(self.browser)
        actions.move_to_element(form)
        actions.click(form)
        actions.perform()

        # Create locators
        email_field = self.browser.find_element_by_css_selector(
            'div#gigya-register-screen input[name="email"]')
        name_field = self.browser.find_element_by_css_selector(
            'div#gigya-register-screen input[name="profile.firstName"]')
        last_field = self.browser.find_element_by_css_selector(
            'div#gigya-register-screen input[name="profile.lastName"]')
        pw = self.browser.find_element_by_css_selector(
            'div#gigya-register-screen input[name="password"]')
        confirm_pw = self.browser.find_element_by_css_selector(
            'div#gigya-register-screen input[name="passwordRetype"]')
        submit_button = self.browser.find_element_by_css_selector(
            'div#gigya-register-screen input[type="submit"]')

        # Fill registration form fields
        email_field.send_keys(self.EMAIL)
        name_field.send_keys(self.FIRST_NAME)
        last_field.send_keys(self.LAST_NAME)
        pw.send_keys(self.PASSWORD)
        confirm_pw.send_keys(self.PASSWORD)

        # Click submit button
        submit_button.click()

    def logout(self):
        # Set locator for 'profile' link
        my_profile_link = self.wait.until(
            EC.visibility_of_element_located((By.ID, 'myProfileLink'))
        )
        # Click on link
        my_profile_link.click()

        # Set 'logout'
        logout_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            'div#gigya-update-profile-screen'
                                            ' div.logout-button'))
        )
        # Click on link
        logout_button.click()

        # Wait for redirect to login dialog
        # call to login dialog automatically looks oddly
        self.wait.until(
            EC.presence_of_element_located((By.ID, "gigya-login-screen"))
        )

    def login(self):
        # Set focus on login dialog
        login_screen = self.browser.find_element_by_id('gigya-login-screen')
        login_actions = ActionChains(self.browser)
        login_actions.move_to_element(login_screen)
        login_actions.click(login_screen)
        login_actions.perform()

        # Set locators for login screen
        login_email = self.browser.find_element_by_css_selector(
            'div#gigya-login-screen input[name="username"]')
        login_pw = self.browser.find_element_by_css_selector(
            'div#gigya-login-screen input[name="password"]')
        submit_login_button = self.browser.find_element_by_css_selector(
            'div#gigya-login-screen input[type="submit"]')

        # Fill login form
        login_email.send_keys(self.EMAIL)
        login_pw.send_keys(self.PASSWORD)

        # Submit form
        submit_login_button.click()

    def test_nascar_new_user_creation(self):
        self.registration()
        self.logout()
        self.login()

        # Assert user is successfully logged in
        my_profile_link_logged = self.wait.until(
            EC.visibility_of_element_located((By.ID, 'myProfileLink'))
        )
        self.assertTrue(my_profile_link_logged.is_displayed())

    def tearDown(self):
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()