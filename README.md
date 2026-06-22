# Инструкция по запуску автотестов (AQA Shop)

## 1. Запуск инфраструктуры:
docker compose up -d

## 2. Запуск тестов:
pytest --alluredir=allure-results

## 3. Просмотр Allure:
allure serve allure-results
