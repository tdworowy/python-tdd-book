from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from .base import wait


class ListPage:
    def __init__(self, test: webdriver):
        self.test: webdriver = test

    def get_table_rows(self) -> list:
        return self.test.browser.find_elements_by_css_selector('#id_list_table tr')

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):
        excepted_row_text = f'{item_number}: {item_text}'
        rows = self.get_table_rows()
        self.test.assertIn(excepted_row_text, [row.text for row in rows])

    def get_item_input_box(self) -> WebElement:
        return self.test.browser.find_element_by_id('id_text')

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )

    def get_shared_with_list(self):
        return self.test.browser.find_elements_by_css_selector(
            '.list-sharee'
        )

    def share_list_with(self, email):
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(
            email,
            [item.text for item in self.get_shared_with_list()]
        ))

    def add_list_item(self, item_text):
        new_item_no = len(self.get_table_rows()) + 1
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(item_text, new_item_no)
        return self

    def get_list_owner(self) -> str:
        return self.test.browser.find_element_by_id('id_list_owner').text

    @wait
    def enter_email(self, email):
        self.test.browser.find_element_by_name('email').send_keys(email)
        self.test.browser.find_element_by_name('email').send_keys(Keys.ENTER)
        self.test.assertIn( 'Check your email', self.test.browser.find_element_by_tag_name('body').text)

    def log_out(self):
        self.test.browser.find_element_by_link_text('Log out').click()

    @wait
    def wait_to_be_logged_in(self, email):
        self.test.browser.find_element_by_link_text('Log out')
        navbar = self.test.browser.find_element_by_css_selector('.navbar')
        self.test.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.test.browser.find_element_by_name('email')
        navbar = self.test.browser.find_element_by_css_selector('.navbar')
        self.test.assertNotIn(email, navbar.text)
