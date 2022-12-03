import pytest
import requests

url = 'https://playground.learnqa.ru/ajax/api/user_agent_check'

user_agent1 = ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30", {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'})
user_agent2 = ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1", {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'})
user_agent3 = ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'})
user_agent4 = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0", {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'})
user_agent5 = ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1", {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})

class TestUserAgent:
    user_agent_list = [user_agent1, user_agent2, user_agent3, user_agent4, user_agent5]

    @pytest.mark.parametrize('user_agent,expected_answer', user_agent_list)
    def test_user_agents(self, user_agent, expected_answer):
        resp = requests.get(url, headers={"User-Agent": user_agent})
        resp_json = dict(resp.json())

        for k, v in expected_answer.items():
            assert k in resp_json, f'Wrong answer - no key "{k}" in the answer!!!'
            assert resp_json[k] == v, f'Wrong value of key "{k}" in the answer! User-agent = {user_agent}'


