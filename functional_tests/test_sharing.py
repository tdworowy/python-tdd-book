from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_list_page import MyListsPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except Exception:
        pass


class SharingTest(FunctionalTest):
    def test_can_share_a_list_witch_another_user(self):
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        oni_browser = webdriver.Firefox(executable_path=self.DRIVER_PATH)
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.create_pre_authenticated_session('oniciferous@example.com')

        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.add_list_item('Get help')

        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'), 'yourfriend@example.com'
        )

        list_page.share_list_with('oniciferous@example.com')

        MyListsPage(self).go_to_my_lists_page()
        self.browser.find_elements_by_link_text('Get help').click()

        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(), 'edith@example.com'
        ))

        list_page.add_list_item('Hi Edith!')

        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith!', 2)