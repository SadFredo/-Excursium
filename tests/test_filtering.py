from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
import pytest


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def scroll_and_click(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def wait_for_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))


class ExcursionsListPage(BasePage):
    PRICE_FILTER_1000 = (By.ID, "priceRange_1000")
    EXCURSION_CARDS = (By.CSS_SELECTOR, '.col .card')

    def open_excursions_list(self):
        self.driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        time.sleep(2)
        return self

    def apply_price_filter_1000(self):
        self.scroll_and_click(self.PRICE_FILTER_1000)
        time.sleep(3)

    def get_excursion_cards_count(self):
        cards = self.wait_for_elements(self.EXCURSION_CARDS)
        return len(cards)


def test_filtering(browser):
    """Тест проверки фильтрации"""
    excursions_page = ExcursionsListPage(browser)

    excursions_page.open_excursions_list()
    excursions_page.apply_price_filter_1000()

    actual_count = excursions_page.get_excursion_cards_count()
    expected_count = 5

    assert actual_count == expected_count, f"Ожидалось {expected_count} карточек, но найдено {actual_count}"
    print("Тест пройден успешно!")
