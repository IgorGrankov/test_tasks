import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class YahooTest(unittest.TestCase):

    def setUp(self):
        self.links = []
        self.browser = webdriver.Firefox()
        self.browser.get("http://www.yahoo.com")
        self.browser.set_window_size(1280, 800)

    def get_dropdown_urls(self):
        # Set locator for 'More' menu
        more = self.browser.find_element(By.ID, 'uh-more-link')
        more_button = self.browser.find_element_by_class_name('more-link')

        # Set focus on 'More' menu
        actions = ActionChains(self.browser)
        actions.move_to_element(more)
        actions.click(more_button)
        actions.perform()

        # Get all elements xpath
        items = self.browser.find_elements(By.XPATH,
                                           '//*[@id="uh-more-link"]/ul/li/a')

        # Fetch urls for each element
        for item in items:
            self.links.append(item.get_attribute('href'))
        return self.links

    def test_get_links(self):
        self.get_dropdown_urls()

        for link in self.links:
            start = time.time()
            ff = webdriver.Firefox()
            ff.get(link)

            # Define that page is loaded after biggest image is loaded
            # A little bit risky
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "fptoday-img")))
            end = time.time()
            load_time = end - start

            # Assert that load time is less than 7 seconds
            self.assertTrue(load_time < 7)
            ff.quit()

    def tearDown(self):
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()
