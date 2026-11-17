import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_user_request import TransferUserRequest
from sqlalchemy.orm import Session



@pytest.mark.api
class TestTransfer:
    def test_transfer(self, api_manager: ApiManager, transfer_data: tuple[CreateUserRequest, CreateAccountResponse, CreateAccountResponse], db_session: Session):
        create_user_request, from_account, to_account = transfer_data

        transfer_user_request=TransferUserRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=1000.0,
        )
        transfer_response = api_manager.user_steps.transfer(
            create_user_request,
            transfer_user_request
        )

        assert transfer_response.fromAccountId == from_account.id, "Id отправителя не сходится"
        assert transfer_response.toAccountId == to_account.id, "Id получателя не сходится"
        assert transfer_response.fromAccountIdBalance == 4000.0, "Ожидали остаток 4000.0 на балансе отправителя"

        account_from_db = Account.get_account_by_id(db_session, from_account.id)
        assert account_from_db is not None, "Счёт не найден в БД"
        assert account_from_db.id == transfer_user_request.fromAccountId, "Аккаунт отправителя некоректный"
        assert account_from_db.balance == 4000.0, "Баланс отправителя не равен 4000.0"
        account_to_db = Account.get_account_by_id(db_session, to_account.id)
        assert account_to_db is not None, "Счет не найден в БД"
        assert account_to_db.id == transfer_user_request.toAccountId, "Аккаунт получателя некоректный"
        assert account_to_db.balance == 1000.0, "Баланс получателя не равен 1000.0"



    def test_transfer_invalid_transfer(self, api_manager: ApiManager, transfer_data: tuple[CreateUserRequest, CreateAccountResponse, CreateAccountResponse], db_session: Session):
        create_user_request, from_account, to_account = transfer_data

        transfer_user_request=TransferUserRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=6000.0,
        )
        transfer_response = api_manager.user_steps.transfer_invalid_transfer(
            create_user_request,
            transfer_user_request
        )

        assert "Insufficient funds" in transfer_response.json()["error"], "Ожидали ошибку: Недостаточно средств!"

        account_from_db = Account.get_account_by_id(db_session, from_account.id)
        assert account_from_db is not None, "Счет не найден в БД"
        assert account_from_db.balance == 5000.0, "Баланс отправителя изменился после неудачного перевода"
        account_to_db = Account.get_account_by_id(db_session, to_account.id)
        assert account_to_db is not None, "Счет получателя не найден"
        assert account_to_db.balance == 0.0, "Баланс получателя изменился после неуспешного перевода"
