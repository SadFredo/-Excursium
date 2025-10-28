from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def scroll_and_click(self, locator):
        """Скролл к элементу и клик"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    def wait_for(self, seconds=3):
        """Ожидание (замена time.sleep)"""
        time.sleep(seconds)


class ExcursionPage(BasePage):
    # Локаторы для страницы экскурсии
    BOOK_BUTTON = (By.CSS_SELECTOR,
                   "div#detail-vue > section:nth-of-type(3) > div > div > div:nth-of-type(2) > div > div > div > div:nth-of-type(5) > button")

    def open_excursion(self, url):
        self.driver.get(url)
        return self

    def click_book_button(self):
        self.scroll_and_click(self.BOOK_BUTTON)
        return BookingModal(self.driver)


class BookingModal(BasePage):
    # Локаторы для модального окна бронирования
    NAME_FIELD = (By.CSS_SELECTOR, "input#bookingUserName")
    PHONE_FIELD = (By.CSS_SELECTOR, "input#orderPhone")
    AGREEMENT_CHECKBOX = (By.CSS_SELECTOR, "input#agreeCheck")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, "div#bookingModal > div > div > div:nth-of-type(3) > button")

    def enter_name(self, name):
        self.type_text(self.NAME_FIELD, name)
        return self

    def enter_phone(self, phone):
        self.type_text(self.PHONE_FIELD, phone)
        return self

    def accept_agreement(self):
        self.click(self.AGREEMENT_CHECKBOX)
        return self

    def click_confirm_button(self):
        self.click(self.CONFIRM_BUTTON)
        # После подтверждения возвращаемся на страницу экскурсии или переходим на страницу подтверждения
        return ExcursionPage(self.driver)

    def fill_booking_form(self, name, phone):
        """Заполнить всю форму бронирования"""
        self.enter_name(name)
        self.wait_for(1)
        self.enter_phone(phone)
        self.wait_for(1)
        self.accept_agreement()
        self.wait_for(1)
        return self


def test_booking(browser):
    """Тест проверки бронирования"""
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:

        excursion_page = ExcursionPage(driver)
        excursion_page.open_excursion("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")

        booking_modal = excursion_page.click_book_button()

        booking_modal.fill_booking_form("Дарья", "1111111111")

        print("Бронирование прошло успешно!")

    finally:
        driver.quit()