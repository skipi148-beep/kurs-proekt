import allure
import time
from sqlalchemy import text

class DbAssertions:
    def __init__(self, db_engine):
        self.engine = db_engine

    @allure.step("Проверить сохранение статуса {expected_status} в таблице {table_name}")
    def verify_last_status(self, table_name, expected_status, timeout=8, poll_frequency=0.5):
        query = text(f"SELECT status FROM {table_name} ORDER BY created DESC LIMIT 1;")
        start_time = time.time()
        result = None
        
        # Чистый кастомный polling-цикл без привязки к Selenium WebDriver
        while time.time() - start_time < timeout:
            with self.engine.connect() as conn:
                res = conn.execute(query).fetchone()
                if res is not None:
                    result = res
                    break
            time.sleep(poll_frequency)
            
        assert result is not None, f"Запись в таблице {table_name} полностью отсутствует в СУБД!"
        # Сверяем извлеченную строку с ожидаемым статусом
        assert result[0] == expected_status, f"Ожидался статус {expected_status}, но в БД сохранен: {result[0]}"
