import allure
from selenium.webdriver.common.by import By

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
        # Локатор для поиска ошибок валидации под полями (красный текст)
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

    @allure.step('Проверить отображение ошибки валидации под полями')
    def is_validation_error_displayed(self):
        try:
            return self.driver.find_element(*self.input_sub_error).is_displayed()
        except:
            return False
