from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import os
from functional_tests.base import FunctionalTest

# TODO need refactor


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        pass
