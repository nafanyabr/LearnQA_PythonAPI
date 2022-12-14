import requests

url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'
methods = ['POST', 'GET', 'PUT', 'DELETE']

def print_info(resp):
    print(resp.request.method, resp.request.url)
    print(resp.status_code, resp.text)
    print('-'*10)

print('Вопрос 1')
response = requests.get(url)
print_info(response)

print('Вопрос 2')
response = requests.head(url, data='HEAD')
print_info(response)

print('Вопрос 3')
response = requests.post(url, data={'method':'POST'})
print_info(response)

print('Вопрос 4')
for method in methods:
    params = {'method': method}

    print('\nCheck new method parameter:', params)

    response = requests.get(url, params=params)
    print_info(response)

    response = requests.post(url, data=params)
    print_info(response)

    response = requests.put(url, data=params)
    print_info(response)

    response = requests.delete(url, data=params)
    print_info(response)

print('Метод DELETE отвечает успешно при method = GET!')