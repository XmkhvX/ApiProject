import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.credit_request import CreditRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account



@pytest.mark.api
class TestCreditUser:
    def test_credit_user(self, api_manager: ApiManager, credit_user_request: CreditRequest, db_session: Session):
        account_response = api_manager.user_steps.create_account(credit_user_request)

        credit_request=CreditRequest(
            accountId=account_response.id,
            amount=5000.0,
            termMonths=12
        )
        credit_response=api_manager.user_steps.credit(credit_user_request, credit_request)

        assert credit_response.id == account_response.id, "Id созданного кредита не соответсвует"
        assert credit_response.amount == credit_request.amount, "Ошибка с запросом денежных средств кредита"
        assert credit_response.termMonths == credit_request.termMonths, "Расхождение в сроке выдачи кредита"
        assert credit_response.balance == credit_request.amount, "Расхождение в сумме выдачи кредита"

        account_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_from_db is not None, "Счет не найден в БД"
        assert account_from_db.id == credit_response.id, "Id счета не совподают в БД"
        assert account_from_db.balance == credit_request.amount, "Ожидали баланс равный сумме пополнения"




    def test_credit_invalid_user(self, api_manager: ApiManager, credit_user_request: CreditRequest, db_session: Session):
        account_response = api_manager.user_steps.create_account(credit_user_request)

        credit_request=CreditRequest(
            accountId=account_response.id,
            amount=5000.0,
            termMonths=12
        )
        api_manager.user_steps.credit(credit_user_request, credit_request)


        second_account_response = api_manager.user_steps.create_account(credit_user_request)

        second_credit_request=CreditRequest(
            accountId=second_account_response.id,
            amount=5000.0,
            termMonths=12
        )
        response=api_manager.user_steps.credit_invalid(credit_user_request, second_credit_request)

        assert response.json()["error"] == ("Only one active credit allowed per user"), "Ожидали ошибку при запросе второго кредитного счета"

        account_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_from_db is not None, "Счет не найден в БД"
        assert account_from_db.id == account_response.id, "Id не совподает в БД"
        assert account_from_db.balance == credit_request.amount, "Ожидали баланс 5000.0 после запроса кредита на 5000.0"
        account_to_db = Account.get_account_by_id(db_session, second_account_response.id)
        assert account_to_db is not None, "Счет не найден в БД"
        assert account_to_db.id == second_account_response.id, "Id не совподает в БД"
        assert account_to_db.balance == 0.0, "Ожидали 0.0 баланс полсе запроса кредита на втрой счет"




    def test_credit_excess(self, api_manager: ApiManager, credit_user_request: CreditRequest, db_session: Session):
        account_response = api_manager.user_steps.create_account(credit_user_request)

        credit_request = CreditRequest(
            accountId=account_response.id,
            amount=15000.1,
            termMonths=12
        )
        response=api_manager.user_steps.credit_invalid(credit_user_request, credit_request)

        assert response.json()["error"] == ("Credit amount cannot exceed 15000"), "Ожидали ошибку из за превышения лимита запроса в 15.000"

        account_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_from_db is not None, "Счет не найден в БД"
        assert account_from_db.id == account_response.id, "Id не совподает в БД"
        assert account_from_db.balance == 0.0, "Ожидали баланс счета 0.0 полсе невалидного запроса"
