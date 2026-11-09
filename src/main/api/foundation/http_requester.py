from typing import Dict, Callable
from src.main.api.foundation.endpoint import Endpoint



class HttpRequester:
    def __init__(self, request_specs: Dict, endpoint: Endpoint, response_specs: Callable):
        self.request_specs = request_specs
        self.endpoint = endpoint
        self.response_specs = response_specs