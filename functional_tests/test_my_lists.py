from .base import FunctionalTest
from .list_page import ListPage
from .my_list_page import MyListsPage


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session('edith@example.com')
        self.browser.get(self.live_server_url)

        list_page = ListPage(self)
        list_page.add_list_item('Reticulate splines')
        list_page.add_list_item('Immanentize eschaton')

        first_list_url = self.browser.current_url

        my_lists = MyListsPage(self).go_to_my_lists_page()

        my_lists.open_list('Reticulate splines')
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        self.browser.get(self.live_server_url)
        list_page.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        my_lists.go_to_my_lists_page()
        my_lists.open_list('Click cows')
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        ))
