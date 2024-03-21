from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QDesktopWidget, QFrame)
import sys

import requestsSQL
from admin_panel import AdminPanel

class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.screen = QDesktopWidget().availableGeometry()
        self.setGeometry(100, 100, 500, 700)

    def widgets(self):
        self.login_frame = QFrame(self)
        self.login_frame.setGeometry(0, 0, self.width(), self.height())
        self.login_frame.setStyleSheet('background-color:rgb(255, 125, 125)')

        self.label_username = QLabel('Username:', self.login_frame)
        self.label_username.setGeometry(self.width() // 2 - 250, self.height() // 2 - 60, 200, 50)
        self.label_username.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.input_username = QLineEdit(self.login_frame)
        self.input_username.setGeometry(self.width() // 2 + 10, self.height() // 2 - 50, 200, 30)

        self.label_password = QLabel('Password:', self.login_frame)
        self.label_password.setGeometry(self.width() // 2 - 250, self.height() // 2, 200, 30)
        self.label_password.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.input_password = QLineEdit(self.login_frame)
        self.input_password.setGeometry(self.width() // 2 + 10, self.height() // 2, 200, 30)
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton('Login', self.login_frame)
        self.btn_login.setGeometry(self.width() // 2 - 100, self.height() // 2 + 50, 90, 30)

        self.btn_register = QPushButton('Register', self.login_frame)
        self.btn_register.setGeometry(self.width() // 2 + 10, self.height() // 2 + 50, 90, 30)

        self.btn_exit = QPushButton('Exit', self.login_frame)
        self.btn_exit.setGeometry(self.width() // 2 - 100, self.height() // 2 + 100, 90, 30)
        self.btn_exit.clicked.connect(self.close)
        
        self.btn_register.clicked.connect(self.add_user_inBD)
        self.btn_login.clicked.connect(self.read_user_fromDB)
    
        
    def add_user_inBD(self):
        requestsSQL.create_table_users(self.BD)
        login = self.input_username.text()
        password = self.input_password.text()
        requestsSQL.add_user(conn=self.BD, username=login, password=password)
        
    
    def read_user_fromDB(self):
        read_users = requestsSQL.read_users(self.BD)
        for id, login, password in read_users:
            self.loginInApp() if login == self.input_username.text() and password == self.input_password.text() else print()
            
        
    def loginInApp(self):
        self.login_frame.setVisible(False)
        self.showFullScreen()
        requestsSQL.create_table_tasks(self.BD)
        AdminPanel(self, self.BD)


    def run(self):
        self.BD = requestsSQL.create_connection('data.db')
        self.widgets()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = MainWindows()
    windows.run()
    sys.exit(app.exec_())