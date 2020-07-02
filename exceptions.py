import requests


class HTTPException(Exception):
    def __init__(self, response: requests.Response):
        super().__init__(f'HTTP code {response.status_code}\n{response.content}')
        self.response = response
