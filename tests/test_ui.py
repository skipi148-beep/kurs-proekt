import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import text

@allure.epic("Дипломный проект: Магазин Туров")
@allure.feature("Покупка тура по дебетовой карте")
@allure.story("Успешная оплата картой APPROVED")
def test_successful_payment_via_card(driver, db_engine):
    # 1. Открываем сайт
    with allure.step("Открыть главную страницу магазина"):
        driver.get("http://localhost:8080")

    # 2. Кликаем по кнопке покупки
    with allure.step("Нажать кнопку 'Купить'"):
        driver.find_element(By.XPATH, "//button[contains(., 'Купить')]").click()

    # 3. Заполняем платежную форму валидными данными карты APPROVED
    with allure.step("Заполнить платежную форму валидными данными"):
        driver.find_element(By.XPATH, "//input[@placeholder='0000 0000 0000 0000']").send_keys("4444 4444 4444 4441")
        driver.find_element(By.XPATH, "//input[@placeholder='08']").send_keys("12")
        driver.find_element(By.XPATH, "//input[@placeholder='22']").send_keys("27")
        driver.find_element(By.XPATH, "//span[text()='Владелец']/..//input").send_keys("Ivan Ivanov")
        driver.find_element(By.XPATH, "//input[@placeholder='999']").send_keys("123")
        driver.find_element(By.XPATH, "//button[contains(., 'Продолжить')]").click()

    # 4. Ожидаем появление сообщения об успешной операции на UI
    with allure.step("Проверить появление всплывающего окна об успехе"):
        wait = WebDriverWait(driver, 15)
        success_notification = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'notification_status_ok')]"))
        )
        assert success_notification.is_displayed(), "Уведомление об успешной операции не появилось!"

    # 5. Проверяем СУБД с умным циклом ожидания записи (Polling)
    with allure.step("Сделать запрос к СУБД и дождаться сохранения статуса APPROVED"):
        result = None
        # Опрашиваем БД в течение 5 секунд (5 попыток по 1 секунде)
        for _ in range(5):
            with db_engine.connect() as conn:
                result = conn.execute(text("SELECT status FROM payment_entity ORDER BY created DESC LIMIT 1;")).fetchone()
                if result is not None:
                    break  # Запись появилась, выходим из цикла
            time.sleep(1)
            
        assert result is not None, "Запись о дебетовом платеже полностью отсутствует в БД!"
        assert result[0] == "APPROVED", f"Ожидался статус APPROVED, но в базе сохранен: {result[0]}"
