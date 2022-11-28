import requests

res = requests.get('https://playground.learnqa.ru/api/get_text')
print(res.text)