import allure
from pages.trip_page import TripPage
from data.cards import CardData
from assertions.db_assertions import DbAssertions
@allure.epic('Дипломный проект: Магазин Туров')
@allure.feature('Покупка тура по дебетовой карте')
def test_successful_debit_payment(driver, db_engine):
    page = TripPage(driver).open()
    page.select_buy_via_card()
    page.fill_form(CardData.APPROVED_CARD, CardData.VALID_MONTH, CardData.VALID_YEAR, CardData.VALID_OWNER, CardData.VALID_CVC)
    validator = DbAssertions(db_engine)
    validator.verify_last_status('payment_entity', 'APPROVED')
