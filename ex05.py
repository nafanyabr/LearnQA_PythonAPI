import json
from json.decoder import JSONDecodeError

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

key = 'messages'
num = 1

try:
    obj = json.loads(json_text)
    if key in obj:
        if len(key) >= num:
            print(obj[key][num])
        else:
            print(f'Ошибка! Сообщение с индексом {num} не найдено!')
    else:
        print(f'Ошибка! Нет ключа {key}!')
except JSONDecodeError:
    print('Ошибка! Переменная json_text не в JSON-формате!')

