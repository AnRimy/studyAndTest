from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QLabel, QDesktopWidget, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QSizePolicy, QHBoxLayout, QFileDialog)
import sys

import requestsSQL
from view.createWidgets import CreateWidgets

class AdminPanel(QMainWindow):
    def __init__(self, parent, BD):
        super().__init__(parent)
        self.parent = parent
        self.BD = BD
        self.screen = QDesktopWidget().availableGeometry()
        self.widgets()


    def widgets(self):
        self.main_frame = QFrame(self.parent)
        self.main_frame.setGeometry(0, 0, self.screen.width(), self.screen.height())
        self.main_frame.setStyleSheet('background-color:rgb(0, 0, 0)')
        self.main_frame.setVisible(True)
        
        self.widgets_info()
        self.widgets_user()
        self.widgets_task()
        self.left_panel()
          
        
    def left_panel(self):
        self.left_panel_frame = QFrame(self.main_frame)
        self.left_panel_frame.setGeometry(0, 0, 500, self.screen.height())
        self.left_panel_frame.setStyleSheet('background-color:rgb(90, 90, 90)')
        self.left_panel_frame.setVisible(True)
        
        self.mainInfo_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 10, 480, 100), 
                                                       'Основная информация',
                                                       ("Arial", 17),
                                                       'background-color:rgb(41, 128, 185); border-radius:10px')
        self.user_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 120, 480, 100), 
                                                       'Пользователи',
                                                       ("Arial", 17),
                                                       'background-color:rgb(141, 128, 185); border-radius:10px')
        self.task_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 230, 480, 100), 
                                                       'Задания',
                                                       ("Arial", 17),
                                                       'background-color:rgb(41, 128, 185); border-radius:10px')
        self.exit_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 970, 480, 100), 
                                                       'Выйти',
                                                       ("Arial", 17),
                                                       'background-color:rgb(231, 76, 60); border-radius:10px')
        
        self.mainInfo_button.clicked.connect(self.show_info)
        self.user_button.clicked.connect(self.show_user)
        self.task_button.clicked.connect(self.show_task)
        self.exit_button.clicked.connect(self.close_program)
        
        
    def widgets_info(self):
        self.info_panel_frame = QFrame(self.main_frame)
        self.info_panel_frame.setGeometry(500, 0, 1420, 1080)
        self.info_panel_frame.setStyleSheet('background-color: rgb(75, 75, 75); color: rgb(255, 255, 255);')
        self.info_panel_frame.setVisible(True)
        
        self.len_users_label = QLabel(self.info_panel_frame)
        self.len_users_label.setGeometry(10, 10, 700, 100)
        self.len_users_label.setText(f'Пользователей: {requestsSQL.len_users(self.BD)}\nЗаданий: {requestsSQL.len_tasks(self.BD)}')
        self.len_users_label.setFont(QFont("Arial", 17))
        self.len_users_label.setStyleSheet('color: rgb(255, 255, 255);')
        self.len_users_label.setVisible(True)

     
    def widgets_user(self):
        def del_user():
            selected_row = self.table.currentRow() + 1
            if selected_row >= 0:
                print(selected_row + 1)
                requestsSQL.delete_user(self.BD, selected_row)
                refresh_table()
                
        def refresh_table():
            self.table.clearContents()
            users = requestsSQL.read_users(self.BD)
            self.table.setRowCount(len(users))
            for row in range(len(users)):
                for col in range(len(users[0])):    
                    self.table.setItem(row, col, QTableWidgetItem(users[row][col]))
            
        self.user_panel_frame = QFrame(self.main_frame)
        self.user_panel_frame.setGeometry(500, 0, 1420, 1080)
        self.user_panel_frame.setStyleSheet('background-color: rgb(75, 75, 75);')
        
        self.delete_user_button = CreateWidgets.get_button(self.user_panel_frame,
                                                            (10, 970, 200, 100),
                                                            'Удалить',
                                                            ("Arial", 17),
                                                            'background-color:rgb(125, 125, 255); border-radius:10px; color: white;')
        self.delete_user_button.clicked.connect(del_user)
        
        users = requestsSQL.read_users(self.BD)
        self.table = QTableWidget(self.user_panel_frame)
        self.table.setGeometry(0, 0, 1420, 700)
        self.table.setStyleSheet('background-color:rgb(125, 125, 125); color: white;')
        self.table.setColumnCount(len(users[0]))
        self.table.setRowCount(len(users))
        self.table.setHorizontalHeaderLabels(['id', 'Логин', 'Пароль'])
        for row in range(len(users)):
            for col in range(len(users[0])):    
                self.table.setItem(row, col, QTableWidgetItem(users[row][col]))
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setVisible(True)

    
    def widgets_task(self):
        self.slide_index = 0
        self.slide = {}
        self.allSlides = []
        
        def addInBD():
            text = self.variantsForTask_textEdit.toPlainText()
            requestsSQL.add_task(self.BD, str(self.allSlides), str(text))
        
        def choice_image():
            self.file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image files (*.jpg *.jpeg *.png *.bmp)")
            if self.file_name:
                self.photo_name_label.setText(str(self.file_name.split('/')[-1]))
                
        def show_slide(index):
            if 0 <= index < len(self.slide):
                self.slide_index_label.setText(str(self.slide_index + 1))
                slide = self.allSlides[index]
                self.slide_index_label.setText(str(index))
                self.titlestudy_textEdit.setText(slide['title'])
                self.photo_name_label.setText(slide['photo'].split('/')[-1])
                self.desc_textEdit.setText(slide['desc'])
                
        def show_back_slide():            
            self.slide_index -= 1
            if self.slide_index < 0:
                self.slide_index = len(self.slide) - 1
            show_slide(self.slide_index)

        def show_next_slide():            
            self.slide_index += 1
            if self.slide_index >= len(self.slide):
                self.slide_index = 0
            try:
                show_slide(self.slide_index)
            except:
                self.titlestudy_textEdit.setText('')
                self.photo_name_label.setText('')
                self.desc_textEdit.setText('')
        
        def add_slide():   
            self.slide['title'] = self.titlestudy_textEdit.toPlainText()
            self.slide['photo'] = self.file_name
            self.slide['desc'] = self.desc_textEdit.toPlainText()
            print(self.slide_index, '\n', self.allSlides)
            try:
                if (self.allSlides[self.slide_index]['title'] != self.slide['title'] or 
                    self.allSlides[self.slide_index]['photo'] != self.slide['photo'] or 
                    self.allSlides[self.slide_index]['desc'] != self.slide['desc']):
                    self.allSlides[self.slide_index] = self.slide.copy()
                    print(self.slide_index, '\n', self.allSlides)
                    return  
                else:
                    return  
            except IndexError:
                pass  
            for i, slide in enumerate(self.allSlides):
                if (slide['title'] == self.slide['title'] and 
                    slide['photo'] == self.slide['photo'] and 
                    slide['desc'] == self.slide['desc']):
                    self.slide_index = i
                    print(self.slide_index, '\n', self.allSlides)
                    return  
            self.allSlides.append(self.slide.copy())
            self.slide_index = len(self.allSlides) - 1  
            print(self.slide_index, '\n', self.allSlides)

        self.task_panel_frame = QFrame(self.main_frame)
        self.task_panel_frame.setGeometry(500, 0, 1420, 1080)
        self.task_panel_frame.setStyleSheet('background-color: rgb(75, 75, 75);')

        task_panel_layout = QHBoxLayout(self.task_panel_frame)

        self.study_frame = QFrame()
        self.study_frame.setStyleSheet('background-color: rgb(0, 200, 150); border-radius: 10px;')
        task_panel_layout.addWidget(self.study_frame)

        self.test_frame = QFrame()
        self.test_frame.setStyleSheet('background-color: rgb(255, 100, 100); border-radius: 10px;')
        task_panel_layout.addWidget(self.test_frame)

        self.task_panel_frame.setLayout(task_panel_layout)

        self.variants_label = CreateWidgets.get_label(self.test_frame, 
                                                (10, 110, 150, 50),
                                                'Вопросы',
                                                ("Arial", 17),
                                                'background-color: rgb(125, 125, 255); border-radius: 10px;')
        self.variantsForTask_textEdit = CreateWidgets.get_textEdit(self.test_frame, 
                                                        (10, 160, 500, 500),
                                                        ("Arial", 12),
                                                        'background-color: rgb(255, 255, 255);')

        self.addTexInDB = CreateWidgets.get_button(self.test_frame, 
                                                (10, 950, 200, 100),
                                                    'Добавить',
                                                    ("Arial", 17),
                                                    'background-color: rgb(125, 125, 255); border-radius: 10px; color: white;')
        
        
        self.slide_index_label = CreateWidgets.get_label(self.study_frame,
                                                (650, 10, 50, 50),
                                                '1',
                                                    ("Arial", 14),
                                                    'background-color: rgb(125, 125, 255); border-radius: 10px;')

        self.study_name_label = CreateWidgets.get_label(self.study_frame,
                                                        (10, 10, 100, 50),
                                                        'Тема',
                                                        ("Arial", 17),
                                                        'background-color: rgb(125, 125, 255);')

        self.titlestudy_textEdit = CreateWidgets.get_textEdit(self.study_frame,
                                                        (10, 60, 500, 50),
                                                        ("Arial", 12),
                                                        'background-color: rgb(255, 255, 255);')

        self.study_phono_button = CreateWidgets.get_button(self.study_frame,
                                                        (10, 150, 200, 50),
                                                        'Выберите фото',
                                                        ("Arial", 17),
                                                        'background-color: rgb(125, 125, 255); border-radius: 10px; color: white;')

        self.photo_name_label = CreateWidgets.get_label(self.study_frame,
                                                (250, 150, 100, 50),
                                                '',
                                                ("Arial", 14),
                                                'background-color: rgb(0, 200, 150);')

        self.study_name_label = CreateWidgets.get_label(self.study_frame,
                                                        (10, 210, 150, 50),
                                                        'Описание',
                                                        ("Arial", 17),
                                                        'background-color: rgb(125, 125, 255);')

        self.desc_textEdit = CreateWidgets.get_textEdit(self.study_frame, 
                                                        (10, 260, 500, 500),
                                                        ("Arial", 14),
                                                        'background-color: rgb(255, 255, 255);')

        self.back_study_button = CreateWidgets.get_button(self.study_frame,
                                                    (10, 950, 200, 100),
                                                    'Назад',
                                                    ("Arial", 17),
                                                    'background-color: rgb(125, 125, 255); border-radius: 10px; color: white;')

        self.next_study_button = CreateWidgets.get_button(self.study_frame,
                                                (490, 950, 200, 100),
                                                'Вперед',
                                                ("Arial", 17),
                                                'background-color: rgb(125, 125, 255); border-radius: 10px; color: white;')

        self.add_study_button = CreateWidgets.get_button(self.study_frame,
                                                (250, 950, 200, 100),
                                                'Dобавить/\nИзменть',
                                                ("Arial", 17),
                                                'background-color: rgb(125, 125, 255); border-radius: 10px; color: white;')

        self.back_study_button.clicked.connect(show_back_slide)
        self.next_study_button.clicked.connect(show_next_slide)
        self.add_study_button.clicked.connect(add_slide)
        self.study_phono_button.clicked.connect(choice_image)
        self.addTexInDB.clicked.connect(addInBD)
                                           

        
        
    def show_info(self):
        for widget in self.main_frame.children():
            if widget.isWidgetType():
                widget.hide() 
        self.left_panel_frame.show()
        self.info_panel_frame.show()
    
        
    def show_user(self):
        for widget in self.main_frame.children():
            if widget.isWidgetType():
                widget.hide() 
        self.left_panel_frame.show()
        self.user_panel_frame.show()
        
        
    def show_task(self):
        for widget in self.main_frame.children():
            if widget.isWidgetType():
                widget.hide()    
        self.left_panel_frame.show()
        self.task_panel_frame.show()
        
        
    def close_program(self):
        exit()
        