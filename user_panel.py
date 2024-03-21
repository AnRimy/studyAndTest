import sys
import json
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QLabel, QDesktopWidget, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QSizePolicy, QHBoxLayout, QFileDialog, QComboBox)

import requestsSQL
from view.createWidgets import CreateWidgets

def extract_themes(json_str):
    try:
        themes_list = json.loads(json_str)
        return [theme['title'] for theme in themes_list]
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON")
        return []

class UserPanel(QMainWindow):
    def __init__(self, parent, user_name, BD):
        super().__init__(parent)
        self.parent = parent
        self.user_name = user_name
        self.BD = BD
        self.screen = QDesktopWidget().availableGeometry()
        self.widgets()
        
    def widgets(self):
        self.main_frame = QFrame(self.parent)
        self.main_frame.setGeometry(0, 0, self.screen.width(), self.screen.height())
        self.main_frame.setStyleSheet('background-color: rgb(51, 51, 51)')
        self.main_frame.setVisible(True)


        self.theme_combo = QComboBox(self.main_frame)
        self.theme_combo.setGeometry(50, 50, 200, 30)
        
        print(type(requestsSQL.read_tasks(self.BD)[0][1]))

        for item in requestsSQL.read_tasks(self.BD)[0][1]:
            themes = extract_themes(item)
            self.theme_combo.addItems(themes)





