import os
import time
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from .management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server, reset_database

MAX_WAIT = 10

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "screen_dumps"
)


def wait(fn):
    def modified(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    return modified


class FunctionalTest(StaticLiveServerTestCase):
    DRIVER_PATH = "driver/geckodriver.exe"

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=self.DRIVER_PATH)
        self.staging_server = os.environ.get("STAGING_SERVER")
        if self.staging_server:
            self.live_server_url = "http://" + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
                self.take_screenshot()
                self.dump_html()

        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        file_name = self._get_filename() + ".png"
        print("screenshotting to", file_name)
        self.browser.get_screenshot_as_file(file_name)

    def dump_html(self):
        file_name = self._get_filename() + ".html"
        print("dumping page HTML to", file_name)
        with open(file_name, "w") as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(":", ".")[:19]
        return "{folder}/{classname}.{method}-window{windowid}-{timestamp}".format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp,
        )

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        self.browser.get(self.live_server_url + "/404_not_such_url/")
        self.browser.add_cookie(
            dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path="/")
        )

    @wait
    def wait_for(self, fn):
        return fn()
