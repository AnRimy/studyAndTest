from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTextEdit
import sys

class CreateWidgets(QWidget):        
    def get_button(parent: QWidget, geometry: list, text: str, font: list, style: str, visible: bool = True, icon: str = None):
        button = QPushButton(parent)
        button.setGeometry(*geometry)
        button.setText(text)
        button.setFont(QFont(*font))
        button.setStyleSheet(style)
        button.setVisible(visible)
        button.setIcon(QIcon(icon))
        button.setIconSize(QSize(button.width() - 4, button.height() - 4))
        return button
    
    
    def get_label(parent: QWidget, geometry: list, text: str, font: list, style: str, visible: bool = True):
        label = QLabel(parent)
        label.setGeometry(*geometry)
        label.setText(text)
        label.setFont(QFont(*font))
        label.setStyleSheet(style)
        label.setVisible(visible)
        return label
    
    
    def get_textEdit(parent: QWidget, geometry: list, font: list, style: str, visible: bool = True):
        textEdit = QTextEdit(parent)
        textEdit.setGeometry(*geometry)
        textEdit.setFont(QFont(*font))
        textEdit.setStyleSheet(style)
        textEdit.setVisible(visible)
        return textEdit
    