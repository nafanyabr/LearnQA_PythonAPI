import requests

url = 'https://playground.learnqa.ru/api/long_redirect'

response = requests.get(url)
print('Кол-во редиректов:', len(response.history))
print('Конечный url:', response.url)