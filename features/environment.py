from selenium import webdriver

DRIVER_PATH = "driver/geckodriver.exe"


def before_all(context):
    context.browser = webdriver.Firefox(executable_path=DRIVER_PATH)


def after_all(context):
    context.browser.quit()


def before_feature(context, feature):
    pass
