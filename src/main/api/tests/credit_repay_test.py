import pytest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest

@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay(self, api_manager, credit_user_request):
        account_response = api_manager.user_steps.create_account(credit_user_request)

        credit_request = CreditRequest(
            accountId=account_response.id,
            amount=5000.0,
            termMonths=12
        )
        credit_response = api_manager.user_steps.credit(credit_user_request, credit_request)

        credit_repay_request = CreditRepayRequest(
            accountId=account_response.id,
            amount=credit_response.amount,
            creditId=credit_response.creditId
        )
        credit_repay_response = api_manager.user_steps.credit_repay(
            credit_user_request, credit_repay_request)


        assert credit_repay_response.creditId == credit_repay_request.creditId
        assert credit_repay_response.amountDeposited == credit_repay_request.amount

    @pytest.mark.parametrize(
        "amount",
        [
            1000.0,
            5000.1,
            4999.9
        ]
    )
    def test_credit_repay_invalid(self, api_manager, credit_user_request, amount):
        account_response = api_manager.user_steps.create_account(credit_user_request)

        credit_request = CreditRequest(
            accountId=account_response.id,
            amount=5000.0,
            termMonths=12
        )
        credit_response = api_manager.user_steps.credit(credit_user_request, credit_request)

        credit_repay_request = CreditRepayRequest(
            accountId=account_response.id,
            amount=amount,
            creditId=credit_response.creditId
        )
        credit_repay_response = api_manager.user_steps.credit_repay_invalid(
            credit_user_request, credit_repay_request)

        assert "error" in credit_repay_response.json()
