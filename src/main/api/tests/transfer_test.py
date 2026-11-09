import pytest
from src.main.api.models.transfer_user_request import TransferUserRequest
from src.main.api.models.deposit_request import DepositRequest


@pytest.mark.api
class TestTransfer:
    def test_transfer(self, api_manager, create_user_request):
        from_account=api_manager.user_steps.create_account(create_user_request)
        to_account=api_manager.user_steps.create_account(create_user_request)

        deposit_request=DepositRequest(
            accountId=from_account.id,
            amount=5000.0,
        )
        response = api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )

        transfer_user_request=TransferUserRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=1000.0,
        )
        transfer_response = api_manager.user_steps.transfer(
            create_user_request,
            transfer_user_request
        )

        assert transfer_response.fromAccountId == from_account.id
        assert transfer_response.toAccountId == to_account.id
        assert transfer_response.fromAccountIdBalance == 4000.0

    @pytest.mark.parametrize(
        "amount",
        [
            499.9,
            10000.1
        ]
    )
    def test_transfer_invalid(self, amount,api_manager, create_user_request):
        from_account=api_manager.user_steps.create_account(create_user_request)
        to_account=api_manager.user_steps.create_account(create_user_request)

        deposit_request=DepositRequest(
            accountId=from_account.id,
            amount=9000.0)

        api_manager.user_steps.deposit(
            create_user_request,
            deposit_request,
        )
        api_manager.user_steps.deposit(
            create_user_request,
            deposit_request,
        )

        transfer_user_request=TransferUserRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=amount,
        )
        transfer_response = api_manager.user_steps.transfer_invalid(
            create_user_request,
            transfer_user_request
        )

        assert "error" in transfer_response.json()

    def test_transfer_invalid_transfer(self, api_manager, create_user_request):
        from_account=api_manager.user_steps.create_account(create_user_request)
        to_account=api_manager.user_steps.create_account(create_user_request)

        deposit_request=DepositRequest(
            accountId=from_account.id,
            amount=1000.0
        )
        api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )
        transfer_user_request=TransferUserRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=5000.0,
        )
        transfer_response = api_manager.user_steps.transfer_invalid_transfer(
            create_user_request,
            transfer_user_request
        )

        assert "Insufficient funds" in transfer_response.json()["error"]
