import requests

while True:
    username = input("What is your name?: ")
    password = input("input your password: ")
    message = input("Input your message: ")
    response = requests.post('http://127.0.0.1:5000/send',
                             json={"username": username,
                                   "password": password,
                                   "text": message})
    if not response.json()['ok']:
        print('Access denied')
        break


