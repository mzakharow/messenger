from datetime import datetime
import time

from flask import Flask, request

app = Flask(__name__)

messages = [
    {'username': 'Jack', 'text': 'Hello', 'time': time.time()}
]

users = {
    # username: password
    'jack': '12345',
    'mary': '123'
}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/status')
def status():
    return {
        'status_code': True,
        'time': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'messages_count': len(messages),
        'users_count': len(users)
    }


@app.route('/history')
def history():
    """
        request: after = 12345.4534
        response: {
            "messages": [
                {"username": "str", "text": "str", "timr": float},
            ]
        }
    """
    after = float(request.args['after'])

    # filtered_messages = []
    # for message in messages:
    #     if after < message['time']:
    #         filtered_messages.append(messages)

    filtered_messages = [message for message in messages if after < message['time']]

    return {'messages': filtered_messages}


@app.route('/send', methods=['POST'])
def send():
    """
    request: {"username": "str", "password": "str", "text": "str", "time": "time"}
    response: {"ok": true}
    """
    data = request.json
    username = data['username']
    password = data['password']
    text = data['text']

    if username in users:
        real_password = users[username]
        if real_password != password:
            return {"ok": False}
    else:
        users[username] = password

    messages.append({'username': username, 'text': text, 'time': time.time()})

    return {"ok": True}


# @app.route('/messages')
# def messages():
#     return {'status_code': 404, 'messages': messages}


if __name__ == '__main__':
    app.run()
