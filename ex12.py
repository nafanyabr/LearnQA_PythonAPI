import pytest
import requests

url = 'https://playground.learnqa.ru/api/homework_header'

header_name = 'x-secret-homework-header'
header_text = 'Some secret value'

class TestHeader:
    def test_header(self):
        resp = requests.get(url)

        assert header_name in resp.headers, f'Header with name {header_name} not found!'

        header_value = resp.headers.get(header_name)
        assert header_value == header_text, 'Wrong header value!'
