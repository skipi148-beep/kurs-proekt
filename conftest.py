import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from sqlalchemy import create_engine, text

@pytest.fixture(scope="session")
def db_engine():
    db_user = "app"
    db_password = "password"
    db_host = "localhost"
    db_port = "5432"
    db_name = "app"
    
    url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(url)
    yield engine
    engine.dispose()

@pytest.fixture(autouse=True)
def clean_db(db_engine):
    with db_engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE order_entity, payment_entity, credit_request_entity RESTART IDENTITY CASCADE;"))
        conn.commit()
    yield

@pytest.fixture()
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # Отключаем GPU, чтобы убрать ошибку CheckFormatSupport
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
