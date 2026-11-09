import pytest
from src.main.api.models.deposit_request import DepositRequest



@pytest.mark.api
class TestDeposit:

    @pytest.mark.parametrize(
        "amount",
        [
            1000.0,
            9000.0
        ]
    )
    def test_deposit_valid(self, amount, api_manager, create_user_request):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId=account_response.id,
            amount=amount
        )

        response = api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )

        assert response.id == account_response.id
        assert response.balance ==(account_response.balance + deposit_request.amount)

    @pytest.mark.parametrize(
        "amount",
        [
            999.99,
            9000.1
        ]
    )
    def test_deposit_invalid(self, amount, api_manager, create_user_request):
        account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId=account_response.id,
            amount=amount
        )

        response = api_manager.user_steps.deposit_invalid(
            create_user_request,
            deposit_request
        )

        assert "error" in response.json()
