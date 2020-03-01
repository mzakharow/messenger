import requests
from PyQt5 import QtWidgets, QtCore
import clientui
from random import randint
from datetime import datetime

class MessengerWindow(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.pressed.connect(self.send_message)
        self.last_message_time = 0

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.getUpdates)
        self.timer.start()

    def send_message(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        message = self.textEdit.toPlainText()
        self.addText(username)
        self.addText(message)
        self.addText('-----------------------------')
        self.addText('')

        if not username:
            self.addText('ERROR: username is empty')
            return
        if not password:
            self.addText('ERROR: password is empty')
            return

        response = requests.post('http://127.0.0.1:5000/send',
                                 json={"username": username,
                                       "password": password,
                                       "text": message})
        if not response.json()['ok']:
            self.textBrowser.append('ERROR: Access denied')
            return

        self.textEdit.clear()
        self.textEdit.repaint()

    def addText(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()

    def getUpdates(self):
        response = requests.get('http://127.0.0.1:5000/history', params={'after': self.last_message_time})
        data = response.json()
        for message in data['messages']:
            time = datetime.fromtimestamp(message["time"])
            # time.strftime("%Y/%m/%d %H:%M:%S")
            # time = message["time"]
            self.addText(f'{time.strftime("%Y/%m/%d %H:%M:%S")} user: {message["username"]}')
            self.addText(message['text'])
            self.addText('')
            self.last_message_time = message['time']


app = QtWidgets.QApplication([])
window = MessengerWindow()
window.show()
app.exec_()
