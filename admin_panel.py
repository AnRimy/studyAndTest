import json
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QHeaderView, QMainWindow, QLabel, QDesktopWidget, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QSizePolicy, QHBoxLayout, QFileDialog)
import ast

import requestsSQL
from view.createWidgets import CreateWidgets

class AdminPanel(QMainWindow):
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
        
        self.widgets_user()
        self.widgets_task()
        self.widgets_editTask()
        self.widgets_info()
        self.left_panel()
        
        
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


    def show_editTask(self):
        for widget in self.main_frame.children():
            if widget.isWidgetType():
                widget.hide()    
        self.left_panel_frame.show()
        self.editTask_panel_frame.show()
          
        
    def left_panel(self):
        self.left_panel_frame = QFrame(self.main_frame)
        self.left_panel_frame.setGeometry(0, 0, 500, self.screen.height())
        self.left_panel_frame.setStyleSheet('background-color:rgb(50, 250, 200)')
        self.left_panel_frame.setVisible(True)
        
        self.mainInfo_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 10, 480, 100), 
                                                       'Основная информация',
                                                       ("Arial", 17),
                                                       'background-color: rgb(41, 128, 185); border-radius: 10px;')
        self.user_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 120, 480, 100), 
                                                       'Пользователи',
                                                       ("Arial", 17),
                                                       'background-color: rgb(41, 128, 185); border-radius: 10px;')
        self.task_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 230, 480, 100), 
                                                       'Задания',
                                                       ("Arial", 17),
                                                       'background-color: rgb(41, 128, 185); border-radius: 10px;')
        self.editTask_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 340, 480, 100), 
                                                       'Работа с Заданиями',
                                                       ("Arial", 17),
                                                       'background-color: rgb(41, 128, 185); border-radius: 10px;')
        self.exit_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 970, 480, 100), 
                                                       'Выйти',
                                                       ("Arial", 17),
                                                       'background-color: rgb(231, 76, 60); border-radius: 10px;')
        
        self.mainInfo_button.clicked.connect(self.show_info)
        self.user_button.clicked.connect(self.show_user)
        self.task_button.clicked.connect(self.show_task)
        self.editTask_button.clicked.connect(self.show_editTask)
        self.exit_button.clicked.connect(self.close_program)
        
        
    def widgets_info(self):
        self.info_panel_frame = QFrame(self.main_frame)
        self.info_panel_frame.setGeometry(500, 0, self.screen.width()-500, 1080)
        self.info_panel_frame.setStyleSheet('background-color:rgb(75, 75, 75)')
        self.info_panel_frame.setVisible(True)
        
        info_panel_layout = QHBoxLayout(self.info_panel_frame)
        
        self.info_frame = QFrame()
        self.info_frame.setStyleSheet('background-color: rgb(0, 200, 150); border-radius: 10px;')
        info_panel_layout.addWidget(self.info_frame)
        
        self.len_users_label = QLabel(self.info_frame)
        self.len_users_label.setGeometry(10, 10, 700, 100)
        self.len_users_label.setText(f'Вход: {self.user_name}\nПользователей: {requestsSQL.len_users(self.BD)}\nЗаданий: {requestsSQL.len_tasks(self.BD)}')
        self.len_users_label.setFont(QFont("Arial", 17))
        self.len_users_label.setStyleSheet('background-color:rgb(0, 200, 150)')
        self.len_users_label.setVisible(True)
    


    def widgets_user(self):
        def add_user_inBD():
            selected_row = self.user_table.currentRow()
            if selected_row >= 0:
                login = self.user_table.item(selected_row, 1).text()  
                password = self.user_table.item(selected_row, 2).text()
                priv = self.user_table.item(selected_row, 3).text()
                requestsSQL.add_user(conn=self.BD, username=login, password=password, priv=priv)
                refresh_table()
                
        def del_user_inBD():
            selected_row = self.user_table.currentRow() + 1
            if selected_row >= 0:
                requestsSQL.delete_user(self.BD, selected_row)
                refresh_table()
                
        def refresh_table():
            self.user_table.clearContents()
            users = requestsSQL.read_users(self.BD)
            self.user_table.setRowCount(len(users))
            for row in range(len(users)):
                for col in range(len(users[0])):
                    self.user_table.setItem(row, col, QTableWidgetItem(users[row][col]))


        
        def add_row_to_table():
            row_count = self.user_table.rowCount()
            self.user_table.insertRow(row_count)

        self.user_panel_frame = QFrame(self.main_frame)
        self.user_panel_frame.setGeometry(500, 0, self.screen.width()-500, 1080)
        self.user_panel_frame.setStyleSheet('background-color: rgb((75, 75, 75);')
        
        user_panel_layout = QHBoxLayout(self.user_panel_frame)
        
        self.user_frame = QFrame()
        self.user_frame.setStyleSheet('background-color: rgb(0, 200, 150); border-radius: 10px;')
        user_panel_layout.addWidget(self.user_frame)


        self.add_user_button = CreateWidgets.get_button(self.user_frame,
                                                        (300, 950, 200, 100),
                                                        'Добавить',
                                                        ("Arial", 17),
                                                        'background-color:rgb(125, 125, 255); border-radius:10px; color: white;')

        self.delete_user_button = CreateWidgets.get_button(self.user_frame,
                                                        (10, 950, 200, 100),
                                                        'Удалить',
                                                        ("Arial", 17),
                                                        'background-color:rgb(125, 125, 255); border-radius:10px; color: white;')
        self.add_row_button = CreateWidgets.get_button(self.user_frame,
                                                        (15, 750, 300, 50),
                                                        'Добавить строку',
                                                        ("Arial", 17),
                                                        'background-color:rgb(125, 125, 255); border-radius:10px; color: white;')

        self.delete_user_button.clicked.connect(del_user_inBD)
        self.add_user_button.clicked.connect(add_user_inBD)
        self.add_row_button.clicked.connect(add_row_to_table)

        users = requestsSQL.read_users(self.BD)
        self.user_table = QTableWidget(self.user_frame)
        self.user_table.setGeometry(15, 15, 1200, 700)
        self.user_table.setStyleSheet('background-color:rgb(100, 255, 150); color: green;border-radius:10px')
        self.user_table.setColumnCount(len(users[0]))
        self.user_table.setRowCount(len(users))
        self.user_table.setHorizontalHeaderLabels(['id', 'Логин', 'Пароль', 'Админ(1/0)'])
        for row in range(len(users)):
            for col in range(len(users[0])):
                self.user_table.setItem(row, col, QTableWidgetItem(users[row][col]))
        self.user_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.user_table.setVisible(True)
    
    
    def widgets_task(self):
        self.slide_index = 0
        self.slide = {}
        self.allSlides = []
        def clear_widgets():
            # self.titlestudy_textEdit.setText('')
            self.photo_name_label.setText('')
            self.desc_textEdit.setText('')
                
        def addInBD():
            text = self.variantsForTask_textEdit.toPlainText()
            # print(self.allSlides)
            requestsSQL.add_task(self.BD, self.allSlides, str(text))
            self.slide.clear()
            self.allSlides.clear()
            self.slide_index = 0
            clear_widgets()
            self.variantsForTask_textEdit.setText('')
            self.updateWorkedTables()
        
        def choice_image(): 
            self.file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image files (*.jpg *.jpeg *.png *.bmp)")
            if self.file_name:
                self.photo_name_label.setText(str(self.file_name.split('/')[-1]))
                
        def show_slide(index):
            if 0 <= index < len(self.slide):
                self.slide_index_label.setText(str(self.slide_index))
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
                clear_widgets()
        
        def add_slide():   
            self.slide['title'] = self.titlestudy_textEdit.toPlainText()
            self.slide['photo'] = self.file_name
            self.slide['desc'] = self.desc_textEdit.toPlainText()
            try:
                if (self.allSlides[self.slide_index]['title'] != self.slide['title'] or 
                    self.allSlides[self.slide_index]['photo'] != self.slide['photo'] or 
                    self.allSlides[self.slide_index]['desc'] != self.slide['desc']):
                    self.allSlides[self.slide_index] = self.slide.copy()
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
                    return  
            self.allSlides.append(self.slide.copy())
            self.slide_index = len(self.allSlides) - 1  
        self.task_panel_frame = QFrame(self.main_frame)
        self.task_panel_frame.setGeometry(500, 0, self.screen.width()-500, 1080)
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
                                                (10, 10, 150, 50),
                                                'Вопросы',
                                                ("Arial", 17),
                                                'border-radius: 10px;')
        self.variantsForTask_textEdit = CreateWidgets.get_textEdit(self.test_frame, 
                                                (10, 60, 500, 500),
                                                ("Arial", 12),
                                                'background-color: rgb(255, 255, 255);')

        self.addTexInDB = CreateWidgets.get_button(self.test_frame, 
                                                (10, 950, 200, 100),
                                                'Добавить в БД',
                                                ("Arial", 17),
                                                'background-color: rgb(125, 125, 255); border-radius: 10px; color: white;')

        self.slide_index_label = CreateWidgets.get_label(self.study_frame,
                                                (650, 10, 50, 50),
                                                '0',
                                                ("Arial", 14),
                                                'border-radius: 10px;')

        self.study_name_label = CreateWidgets.get_label(self.study_frame,
                                                (10, 10, 100, 50),
                                                'Тема',
                                                ("Arial", 17),
                                                'background-color: rgb(0, 200, 150);')

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
                                                (250, 150, 200, 50),
                                                '',
                                                ("Arial", 14),
                                                '')

        self.study_name_label = CreateWidgets.get_label(self.study_frame,
                                                (10, 210, 150, 50),
                                                'Описание',
                                                ("Arial", 17),
                                                'background-color: rgb(0, 200, 150);')

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
        
        
    def updateWorkedTables(self):
        self.editTask_table.clearContents()

        self.allData = []
        for data in requestsSQL.read_tasks(self.BD):
            self.testDict_worked_tables = {}
            for item in data[2].split(','):
                key, value = item.split(':')
                self.testDict_worked_tables[key.strip()] = int(value.strip())
            finalDict = json.loads(data[1])
            if isinstance(finalDict, dict):
                finalDict['task'] = self.testDict_worked_tables
            elif isinstance(finalDict, list):
                finalDict[0]['task'] = self.testDict_worked_tables
            self.allData.append(finalDict)

        num_rows = len(self.allData)
        self.editTask_table.setRowCount(num_rows)

        for row, data in enumerate(self.allData):
            if isinstance(data, dict):
                self.editTask_table.setItem(row, 0, QTableWidgetItem(data.get('title', '')))
                self.editTask_table.setItem(row, 1, QTableWidgetItem(data.get('photo', '')))
                self.editTask_table.setItem(row, 2, QTableWidgetItem(data.get('desc', '')))
                task_data = data.get('task', {})
                task_text = ', '.join([f'{key}: {value}' for key, value in task_data.items()])
                self.editTask_table.setItem(row, 3, QTableWidgetItem(task_text))
            elif isinstance(data, list):
                path = []
                descs = []
                for col, item in enumerate(data):
                    path.append(item.get('photo', ''))
                    descs.append(item.get('desc', '')) 
                for col, item in enumerate(data):
                    self.editTask_table.setItem(row, col * 4, QTableWidgetItem(item.get('title', '')))
                    self.editTask_table.setItem(row, col * 4 + 1, QTableWidgetItem(', '.join(path)))
                    self.editTask_table.setItem(row, col * 4 + 2, QTableWidgetItem(', '.join(descs)))
                    task_data = item.get('task', {})
                    task_text = ', '.join([f'{key}: {value}' for key, value in task_data.items()])
                    self.editTask_table.setItem(row, col * 4 + 3, QTableWidgetItem(task_text))

    def widgets_editTask(self):
        self.allData = []
        def edit_task(): 
            select_index = self.editTask_table.currentRow()
            if select_index != -1:
                title_item = self.editTask_table.item(select_index, 0)
                photo_item = self.editTask_table.item(select_index, 1)
                desc_item = self.editTask_table.item(select_index, 2)
                task_item = self.editTask_table.item(select_index, 3)
                
                title = title_item.text() if title_item is not None else None
                photo = photo_item.text() if photo_item is not None else None
                desc = desc_item.text() if desc_item is not None else None
                task = task_item.text() if task_item is not None else None
                
                study = {'title': title, 'photo': photo, 'desc': desc}
                
                requestsSQL.update_task(self.BD, id=select_index+1, study=study, task=task)
                self.updateWorkedTables()

        def delete_task():
            select_index = self.editTask_table.currentRow() + 1
            if select_index >= 0:
                requestsSQL.delete_task_by_id(self.BD, select_index)
                self.updateWorkedTables()

        
        self.editTask_panel_frame = QFrame(self.main_frame)
        self.editTask_panel_frame.setGeometry(500, 0, self.screen.width()-500, 1080)
        self.editTask_panel_frame.setStyleSheet('background-color: rgb(75, 75, 75);')

        editTask_panel_layout = QHBoxLayout(self.editTask_panel_frame)

        self.editTask_frame = QFrame()
        self.editTask_frame.setStyleSheet('background-color: rgb(0, 200, 150); border-radius: 10px;')
        editTask_frame_layout = QHBoxLayout(self.editTask_frame)

        for data in requestsSQL.read_tasks(self.BD):
            self.testDict_worked_tables = {}
            for item in data[2].split(','):
                key, value = item.split(':')
                self.testDict_worked_tables[key.strip()] = int(value.strip())
            finalDict = json.loads(data[1])
            if isinstance(finalDict, dict):
                finalDict['task'] = self.testDict_worked_tables
            elif isinstance(finalDict, list):
                finalDict[0]['task'] = self.testDict_worked_tables
            self.allData.append(finalDict)

        self.editTask_table = QTableWidget()
        self.editTask_table.setColumnCount(4)
        self.editTask_table.setHorizontalHeaderLabels(["Название", "Фото", "Описание", "Тестовые Данные"])
        self.editTask_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        editTask_frame_layout.addWidget(self.editTask_table)

        num_rows = len(self.allData)
        self.editTask_table.setRowCount(num_rows)

        for row, data in enumerate(self.allData):
            if isinstance(data, dict):
                self.editTask_table.setItem(row, 0, QTableWidgetItem(data.get('title', '')))
                self.editTask_table.setItem(row, 1, QTableWidgetItem(data.get('photo', '')))
                self.editTask_table.setItem(row, 2, QTableWidgetItem(data.get('desc', '')))
                task_data = data.get('task', {})
                task_text = ', '.join([f'{key}: {value}' for key, value in task_data.items()])
                self.editTask_table.setItem(row, 3, QTableWidgetItem(task_text))
            elif isinstance(data, list):
                path = []
                descs = []
                for col, item in enumerate(data):
                    path.append(item.get('photo', ''))
                    descs.append(item.get('desc', '')) 
                for col, item in enumerate(data):
                    self.editTask_table.setItem(row, col * 4, QTableWidgetItem(item.get('title', '')))
                    self.editTask_table.setItem(row, col * 4 + 1, QTableWidgetItem(', '.join(path)))
                    self.editTask_table.setItem(row, col * 4 + 2, QTableWidgetItem(', '.join(descs)))
                    task_data = item.get('task', {})
                    task_text = ', '.join([f'{key}: {value}' for key, value in task_data.items()])
                    self.editTask_table.setItem(row, col * 4 + 3, QTableWidgetItem(task_text))


        editTask_panel_layout.addWidget(self.editTask_frame)
        self.edit_button = CreateWidgets.get_button(self.editTask_frame,
                                                    (10, self.screen.height()-150, 200, 100),
                                                    'Редактировать',
                                                    ('Arrial', 12),
                                                    'background-color: rgb(100, 100, 150); border-radius: 10px;')
        self.del_button = CreateWidgets.get_button(self.editTask_frame,
                                                    (250, self.screen.height()-150, 200, 100),
                                                    'Удалить',
                                                    ('Arrial', 12),
                                                    'background-color: rgb(100, 100, 150); border-radius: 10px;')
        self.edit_button.clicked.connect(edit_task)
        self.del_button.clicked.connect(delete_task)



                    


        
        
    def close_program(self):
        exit()