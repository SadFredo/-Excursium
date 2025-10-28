import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import EMAIL, PASSWORD


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

    def go_to_login(self):
        self.click(self.LOGIN_BUTTON)
        return LoginPage(self.driver)


class LoginPage(BasePage):
    CREATE_ACCOUNT_LINK = (By.XPATH, "//a[contains(text(), 'Создать аккаунт')]")

    def go_to_registration(self):
        self.click(self.CREATE_ACCOUNT_LINK)
        return RegistrationPage(self.driver)


class RegistrationPage(BasePage):
    EMAIL_FIELD = (By.CSS_SELECTOR,
                   "section#login-vue > div > div > div > div > div > div:nth-of-type(2) > div > form:nth-of-type(2) > div > input")
    PASSWORD_FIELD = (By.CSS_SELECTOR,
                      "section#login-vue > div > div > div > div > div > div:nth-of-type(2) > div > form:nth-of-type(2) > div:nth-of-type(2) > input")
    AGREEMENT_CHECKBOX = (By.ID, "isAgreement")
    REGISTRATION_BUTTON = (By.ID, "registraion-btn")

    def register_user(self, email, password):
        self.type_text(self.EMAIL_FIELD, email)
        self.type_text(self.PASSWORD_FIELD, password)
        self.click(self.AGREEMENT_CHECKBOX)
        self.click(self.REGISTRATION_BUTTON)


def test_registration(browser):
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        main_page = MainPage(driver)
        main_page.open_site()
        login_page = main_page.go_to_login()
        registration_page = login_page.go_to_registration()
        registration_page.register_user(EMAIL, PASSWORD)
        time.sleep(3)

        print("Регистрация прошла успешно!")

    finally:
        driver.quit()