from .base import wait


class MyListsPage(object):

    def __init__(self, test):
        self.test = test

    def go_to_my_lists_page(self):
        self.test.browser.get(self.test.live_server_url)
        self.test.browser.find_element_by_link_text("My lists").click()
        self.test.wait_for(
            lambda: self.test.assertEqual(
                self.test.browser.find_element_by_tag_name("h1").text, "My Lists"
            )
        )
        return self

    @wait
    def open_list(self, name):
        self.test.browser.find_element_by_link_text(name).click()
