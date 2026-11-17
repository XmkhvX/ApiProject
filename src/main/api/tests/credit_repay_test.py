import pytest
from sqlalchemy.orm import Session
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account



@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay(self, api_manager: ApiManager, active_credit_response: tuple[CreateUserRequest, CreditResponse], db_session: Session):
        credit_user_request, credit_response = active_credit_response

        credit_repay_request = CreditRepayRequest(
            accountId=credit_response.id,
            amount=credit_response.amount,
            creditId=credit_response.creditId
        )
        credit_repay_response = api_manager.user_steps.credit_repay(
            credit_user_request, credit_repay_request)


        assert credit_repay_response.creditId == credit_repay_request.creditId, "Id при погашении кредита не соответсвует"
        assert credit_repay_response.amountDeposited == credit_repay_request.amount, "Расхождение в сумме погашения кредита"

        account_from_db = Account.get_account_by_id(db_session, credit_response.id)
        assert account_from_db is not None, "Счет не найден в БД"
        assert account_from_db.id == credit_response.id, "Id не соотвествует БД"
        assert account_from_db.balance == 0.0, "Ожидали баланс 0.0 после полного погашения кредита"


    @pytest.mark.parametrize(
        "amount",
        [
            1000.0,
            5000.1,
            4999.9
        ]
    )
    def test_credit_repay_invalid(self, api_manager: ApiManager, active_credit_response: tuple[CreateUserRequest, CreditResponse], amount:float, db_session: Session):
        credit_user_request, credit_response = active_credit_response

        credit_repay_request = CreditRepayRequest(
            accountId=credit_response.id,
            amount=amount,
            creditId=credit_response.creditId
        )

        credit_repay_response = api_manager.user_steps.credit_repay_invalid(
            credit_user_request, credit_repay_request)

        assert "error" in credit_repay_response.json(), "Ожидали ошибку error в ответе"

        account_from_db = Account.get_account_by_id(db_session, credit_response.id)
        assert account_from_db is not None, "Счет не найден в БД"
        assert account_from_db.balance == 5000.0, "После неудачного погашения ожидали баланс 5000.0"
