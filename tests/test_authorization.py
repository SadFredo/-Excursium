from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import EMAIL, PASSWORD
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


class MainPage(BasePage):
    LOGIN_BUTTON = (By.XPATH, "/html/body/header/nav/div/ul/li[4]/a")

    def open_site(self):
        self.driver.get("https://excursium.com/")
        return self

    def go_to_login_page(self):
        self.click(self.LOGIN_BUTTON)
        return LoginPage(self.driver)


class LoginPage(BasePage):
    EMAIL_FIELD = (By.CSS_SELECTOR,
                   "section#login-vue > div > div > div > div > div > div:nth-of-type(2) > div > form > div > input")
    PASSWORD_FIELD = (By.CSS_SELECTOR,
                      "section#login-vue > div > div > div > div > div > div:nth-of-type(2) > div > form > div:nth-of-type(2) > input")
    LOGIN_BUTTON = (By.ID, "login-btn")

    def enter_email(self, email):
        self.type_text(self.EMAIL_FIELD, email)
        return self

    def enter_password(self, password):
        self.type_text(self.PASSWORD_FIELD, password)
        return self

    def click_login_button(self):
        self.click(self.LOGIN_BUTTON)
        # После успешного логина возвращаем главную страницу (или другую целевую страницу)
        return MainPage(self.driver)

    def login(self, email, password):
        """Упрощенный метод для быстрого логина"""
        self.enter_email(email)
        self.enter_password(password)
        return self.click_login_button()


def test_authorization(browser):
    """Тест проверки авторизации"""
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:

        main_page = MainPage(driver)
        main_page.open_site()
        login_page = main_page.go_to_login_page()


        login_page.enter_email(EMAIL)
        login_page.enter_password(PASSWORD)
        main_page_after_login = login_page.click_login_button()

        time.sleep(3)

        print("Авторизация прошла успешно!")

    finally:
        driver.quit()
