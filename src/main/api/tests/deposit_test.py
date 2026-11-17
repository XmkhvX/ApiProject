import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import Session



@pytest.mark.api
class TestDeposit:

    @pytest.mark.parametrize(
        "amount",
        [
            1000.0,
            9000.0
        ]
    )
    def test_deposit_valid(self, amount: float, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId=account_response.id,
            amount=amount
        )

        response = api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )

        assert response.id == account_response.id, "Полученый Id не соответствует id при создании счета"
        assert response.balance == (account_response.balance + deposit_request.amount), "Расхождение в сумме пополнения"

        account_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_from_db is not None, "Счет не найден в БД"
        assert account_from_db.id == account_response.id, "ID счёта в БД не совпадает с ID созданного счёта"
        assert account_from_db.balance == deposit_request.amount, "Баланс на счете в БД не совпадает"



    @pytest.mark.parametrize(
        "amount",
        [
            999.99,
            9000.1
        ]
    )
    def test_deposit_invalid(self, amount: float, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId=account_response.id,
            amount=amount
        )

        response = api_manager.user_steps.deposit_invalid(
            create_user_request,
            deposit_request
        )

        assert "error" in response.json(), "Ожидали ошибку error в сыром ответе"

        account_from_db = Account.get_account_by_id(db_session, account_response.id)
        assert account_from_db is not None, "Счет не найден в БД"
        assert account_from_db.id == account_response.id, "ID счёта в БД не совпадает с ID созданного счёта"
        assert account_from_db.balance == 0.0, "Баланс на счете в БД не совпадает"

