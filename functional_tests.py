from selenium import webdriver
import unittest


class NewVisitorTEst(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="driver/geckodriver.exe")

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it(self):
        self.browser.get("http://localhost:8000")
        self.assertIn('To-Do', self.browser.title)


if __name__ == "__main__":
    unittest.main(warnings='ignore')
