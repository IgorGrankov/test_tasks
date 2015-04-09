from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = 'igorgrnv@gmail.com'
FIRST_NAME = 'Igor'
LAST_NAME = 'Grankov'
PASSWORD = 'MyPass123'


class NascarTestCase(TestCase):

    browser = webdriver.Firefox()
    browser.get("http://www.nascar.com")
    browser.set_window_size(1280, 800)
    register = browser.find_element(By.XPATH, '//*[@id="registerOrLogin"]'
                                              '/a[2]')
    register.click()

    form = WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.ID, 'gigya-register-screen'))
    )

    email_field = browser.find_element_by_name('email')
    # name_field = browser.find_element(By.NAME, 'profile.firstName')
    # lastname_field = browser.find_element(By.NAME, 'profile.lastName')
    # password_field = browser.find_element(By.NAME, 'password')
    # confirm_field = browser.find_element(By.NAME, 'passwordRetype')
    submit_btn = browser.find_element_by_css_selector('input[type="submit"]')

    browser.find_element(By.XPATH, '//*[@id="gigya-register-screen"]/form/div[2]/div/div[2]/div[1]/div/input').click()
    email_field.send_keys(EMAIL)
    submit_btn.click()

