from src.main.api.models.base_model import BaseModel


class TransferUserRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: float