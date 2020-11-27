from functional_tests.base import FunctionalTest
from .list_page import ListPage


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        list_page = ListPage(self)

        input_box = list_page.get_item_input_box()
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 300, delta=100)

        list_page.add_list_item("testing")

        input_box = list_page.get_item_input_box()
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 300, delta=100)
