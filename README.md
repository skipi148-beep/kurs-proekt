# Инструкция по запуску проекта AQA Shop

## 1. Запуск инфраструктуры
Запуск базы данных PostgreSQL, эмулятора банковских шлюзов и Java-приложения осуществляется через Docker Compose:
```bash
docker compose up -d
```
Приложение будет доступно по адресу: http://localhost:8080

## 2. Запуск автотестов
1. Активируйте виртуальное окружение Python:
```bash
source venv/Scripts/activate
```
2. Запустите тесты с записью результатов для Allure-отчета:
```bash
pytest --alluredir=allure-results
```

## 3. Генерация отчетов Allure
Для сборки интерактивного HTML-отчета и его автоматического открытия в браузере выполните:
```bash
allure serve allure-results
```
