import requests
import json
from json.decoder import JSONDecodeError
import time

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'

# 1 Create task
try:
    resp = requests.get(url)
    obj = json.loads(resp.text)
    if ('token' in obj) and ('seconds' in obj):
        token = obj['token']
        seconds = obj['seconds']
    else:
        print('Wrong answer format! Try again later.')
        exit()
except JSONDecodeError:
    print('Incorrect response!', resp.text)

# 2 Check task
params = {'token': token}

try:
    resp = requests.get(url, params=params)
    obj = json.loads(resp.text)
    if ('status' in obj) and obj['status'] == 'Job is NOT ready':
        print(f'Status OK. Waiting {seconds} seconds...')
        time.sleep(seconds)
    else:
        print('Wrong status!')
        exit()
except JSONDecodeError:
    print('Incorrect response!', resp.text)

# 3 Check task after sleep

try:
    resp = requests.get(url, params=params)
    obj = json.loads(resp.text)

    if ('status' in obj) and (obj['status'] == 'Job is ready'):
        if 'result' in obj:
            print('Task completed! Result:', obj['result'])
        else:
            print('Error! No result!')
    else:
        print('Wrong status!')
        exit()
except JSONDecodeError:
    print('Incorrect response!', resp.text)
