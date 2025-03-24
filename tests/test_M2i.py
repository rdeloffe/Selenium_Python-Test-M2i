import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from pages.homePage import HomePage
from pages.widgetsPage import WidgetPage

@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.get("https://demoqa.com/")
    yield browser    
    browser.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)

# def test_homepage(driver,wait):
#     home_page = HomePage(driver,wait)
#     home_page.verif_page_homepage()
#     home_page.click_menu_item_widget()

def test_date_picker(driver,wait):
    home_page = HomePage(driver,wait)
    home_page.verif_page_homepage()
    home_page.click_menu_item_widget()

    widget_page = WidgetPage(driver,wait)
    widget_page.click_date_picker()
    widget_page.select_date()
    widget_page.select_date_hour()



