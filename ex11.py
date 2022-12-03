import pytest
import requests

url = 'https://playground.learnqa.ru/api/homework_cookie'
cookie_name = 'HomeWork'
cookie_text = 'hw_value'

class TestCookie:
    def test_cookies(self):
        resp = requests.get(url)

        assert cookie_name in resp.cookies, f'Cookie with name {cookie_name} not found!'

        cookie_value = resp.cookies.get(cookie_name)
        assert cookie_value == cookie_text, 'Wrong cookie value!'
