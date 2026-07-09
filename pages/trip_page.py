import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TripPage:
    def __init__(self, driver):
        self.driver = driver
        self.buy_button = (By.XPATH, "//button[contains(., 'Купить')]")
        self.credit_button = (By.XPATH, "//button[contains(., 'Купить в кредит')]")
        self.card_input = (By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
        self.month_input = (By.XPATH, "//input[@placeholder='08']")
        self.year_input = (By.XPATH, "//input[@placeholder='22']")
        self.owner_input = (By.XPATH, "//span[text()='Владелец']/..//input")
        self.cvc_input = (By.XPATH, "//input[@placeholder='999']")
        self.submit_button = (By.XPATH, "//button[contains(., 'Продолжить')]")
        self.input_sub_error = (By.XPATH, "//span[contains(@class, 'input__sub')]")

    @allure.step('Открыть страницу покупки тура')
    def open(self):
        self.driver.get('http://localhost:8080')
        return self

    @allure.step('Выбрать обычную оплату по карте')
    def select_buy_via_card(self):
        self.driver.find_element(*self.buy_button).click()

    @allure.step('Выбрать покупку в кредит')
    def select_buy_via_credit(self):
        self.driver.find_element(*self.credit_button).click()

    @allure.step('Заполнить платежную форму')
    def fill_form(self, card_number, month, year, owner, cvc):
        self.driver.find_element(*self.card_input).send_keys(card_number)
        self.driver.find_element(*self.month_input).send_keys(month)
        self.driver.find_element(*self.year_input).send_keys(year)
        self.driver.find_element(*self.owner_input).send_keys(owner)
        self.driver.find_element(*self.cvc_input).send_keys(cvc)
        self.driver.find_element(*self.submit_button).click()

    @allure.step('Дождаться всплывающего окна об успехе операции')
    def wait_success_notification(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'notification_status_ok')]"))
        )

    @allure.step('Дождаться всплывающего окна об ошибке/отказе')
    def wait_error_notification(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'notification_status_error')]"))
        )

    @allure.step('Проверить, что под всеми 5 полями появились сообщения об ошибке валидации')
    def are_all_fields_invalid(self):
        error_elements = self.driver.find_elements(*self.input_sub_error)
        visible_errors = [el for el in error_elements if el.is_displayed()]
        return len(visible_errors) == 5

    @allure.step('Проверить, что появилась хотя бы одна ошибка валидации под полем')
    def is_any_validation_error_displayed(self):
        try:
            return self.driver.find_element(*self.input_sub_error).is_displayed()
        except:
            return False
