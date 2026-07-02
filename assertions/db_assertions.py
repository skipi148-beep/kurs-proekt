cat << 'EOF' > assertions/db_assertions.py
import allure
from sqlalchemy import text
from selenium.webdriver.support.ui import WebDriverWait

class DbAssertions:
    def __init__(self, db_engine):
        self.engine = db_engine

    @allure.step("Проверить сохранение статуса {expected_status} в таблице {table_name}")
    def verify_last_status(self, table_name, expected_status, timeout=8):
        query = text(f"SELECT status FROM {table_name} ORDER BY created DESC LIMIT 1;")
        
        def check_db_condition(driver):
            with self.engine.connect() as conn:
                res = conn.execute(query).fetchone()
                return res if res is not None else False

        try:
            result = WebDriverWait(None, timeout=timeout, poll_frequency=0.5).until(check_db_condition)
        except:
            result = None
            
        assert result is not None, f"Запись в таблице {table_name} полностью отсутствует в СУБД!"
        # Извлекаем первый элемент кортежа SQLAlchemy корректно
        assert result[0] == expected_status, f"Ожидался статус {expected_status}, но в БД сохранен: {result[0]}"
EOF
