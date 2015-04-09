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

    def test_get_links(self):
        more = self.browser.find_element(By.ID, 'uh-more-link')
        more_button = self.browser.find_element_by_class_name('more-link')
        actions = ActionChains(self.browser)
        actions.move_to_element(more)
        actions.click(more_button)
        actions.perform()

        items = self.browser.find_elements(By.XPATH,
                                           '//*[@id="uh-more-link"]/ul/li/a')

        for item in items:
            self.links.append(item.get_attribute('href'))

        for link in self.links:
            start = time.time()
            ff = webdriver.Firefox()
            ff.get(link)
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "fptoday-img")))
            end = time.time()
            load_time = end - start
            self.assertTrue(load_time, 7)
            ff.quit()

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
