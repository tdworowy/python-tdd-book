from selenium import webdriver

browser = webdriver.Firefox(executable_path="driver/geckodriver.exe")

browser.get("http://localhost:8000")

assert 'Django' in browser.title
