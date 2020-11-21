from selenium import webdriver

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        self.add_list_item('Buy peacock feathers')
        self.add_list_item('Use peacock feathers to make a fly')

    def test_can_start_a_list_for_multiple_users(self):
        self.browser.get(self.live_server_url)

        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        self.add_list_item('Buy peacock feathers')
        self.add_list_item('Use peacock feathers to make a fly')

        list_url1 = self.browser.current_url
        self.assertRegex(list_url1, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path=self.DRIVER_PATH)
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Buy peacock feathers', page_text)
        self.assertNotIn('2: Use peacock feathers to make a fly', page_text)

        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        self.add_list_item('Buy milk')

        list_url2 = self.browser.current_url
        self.assertRegex(list_url2, '/lists/.+')

        self.assertNotEqual(list_url1, list_url2)
