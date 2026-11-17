import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.test_data.credit_data import CREDIT_AMOUNT, CREDIT_TERM_MONTHS



@pytest.fixture
def create_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def credit_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def second_credit_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def active_credit_response(api_manager: ApiManager, credit_user_request: CreditRequest):
    account_response = api_manager.user_steps.create_account(credit_user_request)

    credit_request = CreditRequest(
        accountId=account_response.id,
        amount=CREDIT_AMOUNT,
        termMonths=CREDIT_TERM_MONTHS,
    )
    credit_response = api_manager.user_steps.credit(credit_user_request, credit_request)
    return credit_user_request, credit_response

@pytest.fixture
def transfer_data(api_manager: ApiManager, create_user_request: CreateUserRequest):
    from_account = api_manager.user_steps.create_account(create_user_request)
    to_account = api_manager.user_steps.create_account(create_user_request)

    deposit_request = DepositRequest(
        accountId=from_account.id,
        amount=5000.0,
    )
    api_manager.user_steps.deposit(
        create_user_request,
        deposit_request
    )
    return create_user_request, from_account, to_account