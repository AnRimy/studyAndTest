from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QDesktopWidget, QFrame)
import sys

import requestsSQL
from admin_panel import AdminPanel
from user_panel import UserPanel

class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.screen = QDesktopWidget().availableGeometry()
        self.setGeometry(100, 100, 500, 700)

    def widgets(self):
        self.login_frame = QFrame(self)
        self.login_frame.setGeometry(0, 0, self.width(), self.height())
        self.login_frame.setStyleSheet('background-color: #2c3e50')

        text_color = "#ffffff"

        self.label_username = QLabel('Имя пользователя:', self.login_frame)
        self.label_username.setGeometry(self.width() // 2 - 250, self.height() // 2 - 70, 200, 50)
        self.label_username.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_username.setStyleSheet(f'color: {text_color};')

        self.input_username = QLineEdit(self.login_frame)
        self.input_username.setGeometry(self.width() // 2 + 10, self.height() // 2 - 60, 200, 30)
        self.input_username.setStyleSheet('background-color: rgba(100 ,100, 100, 100); border-radius: 5px;')

        self.label_password = QLabel('Пароль:', self.login_frame)
        self.label_password.setGeometry(self.width() // 2 - 250, self.height() // 2 - 10, 200, 30)
        self.label_password.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_password.setStyleSheet(f'color: {text_color};')

        self.input_password = QLineEdit(self.login_frame)
        self.input_password.setGeometry(self.width() // 2 + 10, self.height() // 2 - 10, 200, 30)
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet('background-color: rgba(100 ,100, 100, 100); border-radius: 5px;')

        self.btn_login = QPushButton('Вход', self.login_frame)
        self.btn_login.setGeometry(self.width() // 2 - 100, self.height() // 2 + 40, 100, 30)
        self.btn_login.setStyleSheet('background-color: #27ae60; border-radius: 5px; color: #ffffff;')

        self.btn_exit = QPushButton('Выход', self.login_frame)
        self.btn_exit.setGeometry(self.width() // 2 + 10, self.height() // 2 + 40, 100, 30)
        self.btn_exit.setStyleSheet('background-color: #c0392b; border-radius: 5px; color: #ffffff;')
        self.btn_exit.clicked.connect(self.close)

        self.btn_login.clicked.connect(self.read_user_fromDB)
        
    
    def read_user_fromDB(self):
        read_users = requestsSQL.read_users(self.BD)
        for id, login, password, priv in read_users:
            if login == self.input_username.text() and password == self.input_password.text():
                self.loginInApp(login, int(priv))
            
        
    def loginInApp(self, login, priv):
        self.login_frame.setVisible(False)
        self.showFullScreen()
        AdminPanel(self, login, self.BD) if priv else UserPanel(self, login, self.BD)
        

    def run(self):
        self.BD = requestsSQL.create_connection('data.db')
        requestsSQL.create_tables(self.BD)
        self.widgets()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = MainWindows()
    windows.run()
    sys.exit(app.exec_())