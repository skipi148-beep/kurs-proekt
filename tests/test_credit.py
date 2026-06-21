import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import text

@allure.epic("Дипломный проект: Магазин Туров")
@allure.feature("Покупка тура в кредит")
@allure.story("Успешное оформление кредита картой APPROVED")
def test_successful_credit_via_card(driver, db_engine):
    with allure.step("Открыть главную страницу магазина"):
        driver.get("http://localhost:8080")

    with allure.step("Нажать кнопку 'Купить в кредит'"):
        driver.find_element(By.XPATH, "//button[contains(., 'Купить в кредит')]").click()

    with allure.step("Заполнить кредитную форму валидными данными"):
        driver.find_element(By.XPATH, "//input[@placeholder='0000 0000 0000 0000']").send_keys("4444 4444 4444 4441")
        driver.find_element(By.XPATH, "//input[@placeholder='08']").send_keys("12")
        driver.find_element(By.XPATH, "//input[@placeholder='22']").send_keys("27")
        driver.find_element(By.XPATH, "//span[text()='Владелец']/..//input").send_keys("Ivan Ivanov")
        driver.find_element(By.XPATH, "//input[@placeholder='999']").send_keys("123")
        driver.find_element(By.XPATH, "//button[contains(., 'Продолжить')]").click()

    with allure.step("Проверить появление всплывающего окна об успехе"):
        wait = WebDriverWait(driver, 15)
        success_notification = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'notification_status_ok')]"))
        )
        assert success_notification.is_displayed(), "Уведомление об успешной операции не появилось!"

    with allure.step("Сделать запрос к СУБД и проверить сохранение статуса APPROVED в кредитной таблице"):
        time.sleep(1.5)
        with db_engine.connect() as conn:
            result = conn.execute(text("SELECT status FROM credit_request_entity ORDER BY created DESC LIMIT 1;")).fetchone()
            assert result is not None, "Запись о кредите отсутствует в БД!"
            assert result[0] == "APPROVED", f"Ожидался статус APPROVED, но в базе сохранен: {result[0]}"
