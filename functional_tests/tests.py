from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import os


# TODO need refactor
class NewVisitorTEst(StaticLiveServerTestCase):
    MAX_WAIT = 10
    DRIVER_PATH = "driver/geckodriver.exe"

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=self.DRIVER_PATH)
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = "http://" + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                break
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.1)

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

    def test_can_start_a_list_for_multiple_users(self):
        self.browser.get(self.live_server_url)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        list_url1 = self.browser.current_url
        self.assertRegex(list_url1, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path=self.DRIVER_PATH)
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Buy peacock feathers', page_text)
        self.assertNotIn('2: Use peacock feathers to make a fly', page_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        list_url2 = self.browser.current_url
        self.assertRegex(list_url2, '/lists/.+')

        self.assertNotEqual(list_url1, list_url2)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 300, delta=100)
        
        input_box.send_keys("testing")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 300, delta=100)