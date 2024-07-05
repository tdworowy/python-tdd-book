from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector(".has-error")

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)

        list_page.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid"),
        )

        list_page.get_item_input_box().send_keys("Buy milk")
        self.wait_for(
            lambda: self.browser.find_elements_by_css_selector("#id_text:valid")
        )

        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table("Buy milk", 1)

        list_page.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid"),
        )

        list_page.get_item_input_box().send_keys("Make tea")
        self.wait_for(
            lambda: self.browser.find_elements_by_css_selector("#id_text:valid")
        )
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        list_page.wait_for_row_in_list_table("Buy milk", 1)
        list_page.wait_for_row_in_list_table("Make tea", 2)

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)

        list_page.add_list_item("Buy wellies")

        list_page.get_item_input_box().send_keys("Buy wellies")
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertEqual(
                self.get_error_element().text, "You've already got this in your list"
            )
        )

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)

        list_page.add_list_item("Banter too thick")
        list_page.get_item_input_box().send_keys("Banter too thick")
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))

        list_page.get_item_input_box().send_keys("a")
        self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()))
