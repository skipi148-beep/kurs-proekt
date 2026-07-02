import allure
import pytest
from pages.trip_page import TripPage
from data.cards import CardData
from assertions.db_assertions import DbAssertions

@allure.epic("Дипломный проект: Магазин Туров")
class TestTripShop:

    # ПОЗИТИВНЫЕ СЦЕНАРИИ
    @allure.feature("Покупка тура по дебетовой карте")
    @allure.story("Успешная оплата картой APPROVED")
    def test_successful_debit_payment(self, driver, db_engine):
        page = TripPage(driver).open()
        page.select_buy_via_card()
        page.fill_form(CardData.APPROVED_CARD, CardData.VALID_MONTH, CardData.VALID_YEAR, CardData.VALID_OWNER, CardData.VALID_CVC)
        DbAssertions(db_engine).verify_last_status("payment_entity", "APPROVED")

    @allure.feature("Покупка тура в кредит")
    @allure.story("Успешное оформление кредита картой APPROVED")
    def test_successful_credit_payment(self, driver, db_engine):
        page = TripPage(driver).open()
        page.select_buy_via_credit()
        page.fill_form(CardData.APPROVED_CARD, CardData.VALID_MONTH, CardData.VALID_YEAR, CardData.VALID_OWNER, CardData.VALID_CVC)
        DbAssertions(db_engine).verify_last_status("credit_request_entity", "APPROVED")

    # НЕГАТИВНЫЕ СЦЕНАРИИ
    @allure.feature("Покупка тура по дебетовой карте")
    @allure.story("Отказ в оплате картой DECLINED")
    def test_declined_debit_payment(self, driver, db_engine):
        page = TripPage(driver).open()
        page.select_buy_via_card()
        page.fill_form(CardData.DECLINED_CARD, CardData.VALID_MONTH, CardData.VALID_YEAR, CardData.VALID_OWNER, CardData.VALID_CVC)
        DbAssertions(db_engine).verify_last_status("payment_entity", "DECLINED")

    @allure.feature("Покупка тура в кредит")
    @allure.story("Отказ в кредите картой DECLINED")
    def test_declined_credit_payment(self, driver, db_engine):
        page = TripPage(driver).open()
        page.select_buy_via_credit()
        page.fill_form(CardData.DECLINED_CARD, CardData.VALID_MONTH, CardData.VALID_YEAR, CardData.VALID_OWNER, CardData.VALID_CVC)
        DbAssertions(db_engine).verify_last_status("credit_request_entity", "DECLINED")

    @allure.feature("Валидация формы")
    @allure.story("Отправка полностью пустой формы")
    def test_empty_form_validation(self, driver):
        page = TripPage(driver).open()
        page.select_buy_via_card()
        page.fill_form("", "", "", "", "")
        assert page.is_validation_error_displayed(), "Ошибки валидации пустых полей не отобразились!"

    @allure.feature("Валидация формы")
    @allure.story("Невалидный формат номера карты (15 цифр)")
    def test_short_card_number(self, driver):
        page = TripPage(driver).open()
        page.select_buy_via_card()
        page.fill_form("4444 4444 4444 444", CardData.VALID_MONTH, CardData.VALID_YEAR, CardData.VALID_OWNER, CardData.VALID_CVC)
        assert page.is_validation_error_displayed(), "Ошибка короткого номера карты не появилась!"

    @allure.feature("Валидация формы")
    @allure.story("Невалидное значение месяца (00)")
    def test_zero_month_validation(self, driver):
        page = TripPage(driver).open()
        page.select_buy_via_card()
        page.fill_form(CardData.APPROVED_CARD, "00", CardData.VALID_YEAR, CardData.VALID_OWNER, CardData.VALID_CVC)
        assert page.is_validation_error_displayed(), "Ошибка невалидного месяца (00) не появилась!"

    @allure.feature("Валидация формы")
    @allure.story("Невалидное значение месяца (13)")
    def test_invalid_max_month(self, driver):
        page = TripPage(driver).open()
        page.select_buy_via_card()
        page.fill_form(CardData.APPROVED_CARD, "13", CardData.VALID_YEAR, CardData.VALID_OWNER, CardData.VALID_CVC)
        assert page.is_validation_error_displayed(), "Ошибка невалидного месяца (13) не появилась!"

    @allure.feature("Валидация формы")
    @allure.story("Истекший срок действия карты (Прошедший год)")
    def test_past_year_validation(self, driver):
        page = TripPage(driver).open()
        page.select_buy_via_card()
        page.fill_form(CardData.APPROVED_CARD, CardData.VALID_MONTH, "23", CardData.VALID_OWNER, CardData.VALID_CVC)
        assert page.is_validation_error_displayed(), "Ошибка истекшего года карты не появилась!"

    @allure.feature("Валидация формы")
    @allure.story("Избыточный срок действия карты (Далекое будущее)")
    def test_future_year_validation(self, driver):
        page = TripPage(driver).open()
        page.select_buy_via_card()
        page.fill_form(CardData.APPROVED_CARD, CardData.VALID_MONTH, "35", CardData.VALID_OWNER, CardData.VALID_CVC)
        assert page.is_validation_error_displayed(), "Ошибка года из далекого будущего не появилась!"

    @allure.feature("Валидация формы")
    @allure.story("Невалидные данные в поле Владелец (Кириллица)")
    def test_cyrillic_owner_name(self, driver):
        page = TripPage(driver).open()
        page.select_buy_via_card()
        page.fill_form(CardData.APPROVED_CARD, CardData.VALID_MONTH, CardData.VALID_YEAR, "Иван Иванов", CardData.VALID_CVC)
        assert page.is_validation_error_displayed(), "Ошибка кириллицы в имени владельца не появилась!"

    @allure.feature("Валидация формы")
    @allure.story("Невалидный формат CVC/CVV кода (2 цифры)")
    def test_short_cvc_validation(self, driver):
        page = TripPage(driver).open()
        page.select_buy_via_card()
        page.fill_form(CardData.APPROVED_CARD, CardData.VALID_MONTH, CardData.VALID_YEAR, CardData.VALID_OWNER, "12")
        assert page.is_validation_error_displayed(), "Ошибка короткого CVC кода не появилась!"
