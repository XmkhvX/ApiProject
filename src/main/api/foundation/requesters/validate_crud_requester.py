from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
import allure



class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_specs, endpoint, response_specs):
        super().__init__(request_specs, endpoint, response_specs)
        self.crud_requester = CrudRequester(
            request_specs=request_specs,
            endpoint=endpoint,
            response_specs=response_specs
        )


    def post(self, model: Optional[BaseModel] = None) -> Optional[BaseModel]:
        response=self.crud_requester.post(model)

        with allure.step(f"POST {Config.fetch("backendUrl")}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")


        self.response_specs(response)
        return self.endpoint.value.response_model.model_validate(response.json())


    def delete(self, user_id: int):
        response=self.crud_requester.delete(user_id)
        self.response_specs(response)
        return self.endpoint.value.response_model.model_validate(response.json())