import allure
import time
from sqlalchemy import text
class DbAssertions:
    def __init__(self, db_engine):
        self.engine = db_engine
    @allure.step('Проверить сохранение статуса {expected_status} в таблице {table_name}')
    def verify_last_status(self, table_name, expected_status, timeout=8):
        query = text(f'SELECT status FROM {table_name} ORDER BY created DESC LIMIT 1;')
        start_time = time.time()
        result = None
        while time.time() - start_time < timeout:
            with self.engine.connect() as conn:
                result = conn.execute(query).fetchone()
                if result is not None:
                    break
            time.sleep(0.5)
        actual_status = result[0]
        assert actual_status == expected_status, f'Ожидался статус {expected_status}, но в БД сохранен: {actual_status}'
