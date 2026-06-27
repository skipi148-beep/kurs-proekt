# Инструкция по запуску проекта AQA Shop

## 1. Запуск инфраструктуры
docker compose up -d

## 2. Запуск автотестов
source venv/Scripts/activate
pytest --alluredir=allure-results

## 3. Генерация отчетов Allure
allure serve allure-results
