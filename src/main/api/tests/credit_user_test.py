import pytest
from src.main.api.models.credit_request import CreditRequest

@pytest.mark.api
class TestCreditUser:
    def test_credit_user(self, api_manager, credit_user_request):
        account_response = api_manager.user_steps.create_account(credit_user_request)

        credit_request=CreditRequest(
            accountId=account_response.id,
            amount=5000.0,
            termMonths=12
        )
        credit_response=api_manager.user_steps.credit(credit_user_request, credit_request)

        assert credit_response.id == account_response.id
        assert credit_response.amount == credit_request.amount
        assert credit_response.termMonths == credit_request.termMonths
        assert credit_response.balance == credit_request.amount


    def test_credit_invalid_user(self, api_manager, credit_user_request):
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

        assert response.json()["error"] == ("Only one active credit allowed per user")

    def test_credit_excess(self, api_manager, credit_user_request):
        account_response = api_manager.user_steps.create_account(credit_user_request)

        credit_request = CreditRequest(
            accountId=account_response.id,
            amount=15000.1,
            termMonths=12
        )
        response=api_manager.user_steps.credit_invalid(credit_user_request, credit_request)

        assert response.json()["error"] == ("Credit amount cannot exceed 15000")

