import allure
from time import time
from time import sleep as wait_interval
from sqlalchemy import text

class DbAssertions:
    def __init__(self, db_engine):
        self.engine = db_engine

    @allure.step("Проверить сохранение статуса {expected_status} в таблице {table_name}")
    def verify_last_status(self, table_name, expected_status, timeout=8):
        query = text(f"SELECT status FROM {table_name} ORDER BY created DESC LIMIT 1;")
        start_time = time()
        result = None
        
        while time() - start_time < timeout:
            with self.engine.connect() as conn:
                res = conn.execute(query).fetchone()
                if res is not None:
                    result = res
                    break
            wait_interval(0.5)
            
        assert result is not None, f"Запись в таблице {table_name} полностью отсутствует!"
        assert result == expected_status, f"Ожидался статус {expected_status}, но в БД сохранен: {result}"
import allure
from time import time
from time import sleep as wait_interval
from sqlalchemy import text

class DbAssertions:
    def __init__(self, db_engine):
        self.engine = db_engine

    @allure.step("Проверить сохранение статуса {expected_status} в таблице {table_name}")
    def verify_last_status(self, table_name, expected_status, timeout=8):
        query = text(f"SELECT status FROM {table_name} ORDER BY created DESC LIMIT 1;")
        start_time = time()
        result = None
        
        while time() - start_time < timeout:
            with self.engine.connect() as conn:
                res = conn.execute(query).fetchone()
                if res is not None:
                    result = res
                    break
            wait_interval(0.5)
            
        assert result is not None, f"Запись в таблице {table_name} полностью отсутствует!"
        assert result == expected_status, f"Ожидался статус {expected_status}, но в БД сохранен: {result}"
