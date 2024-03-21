from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTextEdit
import sys

class CreateWidgets(QWidget):        
    def get_button(parent: QWidget, geometry: list, text: str, font: list, style: str, visible: bool = True):
        button = QPushButton(parent)
        button.setGeometry(*geometry)
        button.setText(text)
        button.setFont(QFont(*font))
        button.setStyleSheet(style)
        button.setVisible(visible)
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
    