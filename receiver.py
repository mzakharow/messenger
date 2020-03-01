from datetime import datetime
from time import sleep

import requests

# {
#     "messages": [
#         {"username": "str", "text": "str", "time": float},
#     ]
# }

last_message_time = 0

while True:
    response = requests.get('http://127.0.0.1:5000/history', params={'after': last_message_time})
    data = response.json()
    for message in data['messages']:
        time = datetime.fromtimestamp(message["time"])
        # time.strftime("%Y/%m/%d %H:%M:%S")
        # time = message["time"]
        print(f'{time.strftime("%Y/%m/%d %H:%M:%S")} user: {message["username"]}')
        print(message['text'])
        print()
        last_message_time = message['time']

    sleep(1)
