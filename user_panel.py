import ast
import json
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QLabel, QDesktopWidget, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QSizePolicy, QHBoxLayout, QFileDialog, QComboBox, QVBoxLayout)
import random
import time

import requestsSQL
from view.createWidgets import CreateWidgets


class UserPanel(QMainWindow):
    def __init__(self, parent, user_id, user_name, BD):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id
        self.user_name = user_name
        self.BD = BD
        self.screen = QDesktopWidget().availableGeometry()
        self.widgets()
        
    def widgets(self):
        self.main_frame = QFrame(self.parent)
        self.main_frame.setGeometry(0, 0, self.screen.width(), self.screen.height())
        self.main_frame.setStyleSheet('background-color: rgb(51, 51, 51)')
        self.main_frame.setVisible(True)
        
        
        self.widgets_task()
        self.widgets_info()
        self.left_panel()
            
        
    def show_info(self):
        for widget in self.main_frame.children():
            if widget.isWidgetType():
                widget.hide() 
        self.left_panel_frame.show()
        self.info_panel_frame.show()
        
        
    def show_task(self):
        for widget in self.main_frame.children():
            if widget.isWidgetType():
                widget.hide()    
        self.left_panel_frame.show()
        self.main_panel_frame.show()
        
        
    def left_panel(self):
        self.left_panel_frame = QFrame(self.main_frame)
        self.left_panel_frame.setGeometry(0, 0, 100, self.screen.height())
        self.left_panel_frame.setStyleSheet('background-color:rgb(50, 250, 200)')
        self.left_panel_frame.setVisible(True)
        
        self.mainInfo_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 10, 80, 80), 
                                                       '',
                                                       ("Arial", 17),
                                                       'background-color: rgb(41, 128, 185); border-radius: 10px;',
                                                       icon = r'.\icon\info.png')
        self.task_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, 100, 80, 80), 
                                                       '',
                                                       ("Arial", 17),
                                                       'background-color: rgb(41, 128, 185); border-radius: 10px;',
                                                       icon=r'.\icon\task.png')
        self.exit_button = CreateWidgets.get_button(self.left_panel_frame, 
                                                       (10, self.screen.height()-90, 80, 80), 
                                                       '',
                                                       ("Arial", 17),
                                                       'background-color: rgb(231, 76, 60); border-radius: 10px;',
                                                       icon=r'icon\exit.png')
        
        self.mainInfo_button.clicked.connect(self.show_info)
        self.task_button.clicked.connect(self.show_task)
        self.exit_button.clicked.connect(self.close_program)
        
        
    def widgets_info(self):
        self.info_panel_frame = QFrame(self.main_frame)
        self.info_panel_frame.setGeometry(100, 0, self.screen.width()-100, 1080)
        self.info_panel_frame.setStyleSheet('background-color:rgb(75, 75, 75)')
        self.info_panel_frame.setVisible(True)
        
        info_panel_layout = QHBoxLayout(self.info_panel_frame)
        
        self.info_frame = QFrame()
        self.info_frame.setStyleSheet('background-color: rgb(0, 200, 150); border-radius: 10px;')
        info_panel_layout.addWidget(self.info_frame)
        
        self.len_users_label = QLabel(self.info_frame)
        self.len_users_label.setGeometry(10, 10, 700, 100)
        self.len_users_label.setText(f'Вход: {self.user_name}')
        self.len_users_label.setFont(QFont("Arial", 17))
        self.len_users_label.setStyleSheet('background-color:rgb(0, 200, 150)')
        self.len_users_label.setVisible(True)
        
        
    def widgets_task(self):
        alltraining = []
        allTest = []
        def show_firstChoiceTheme():
            for widget in self.main_panel_frame.children():
                if widget.isWidgetType():
                    widget.hide()    
            self.firstChoiceTheme_frame.show()
            self.result_label.hide()
        
        def show_secondTrainingOrTestFrame():
            for widget in self.main_panel_frame.children():
                if widget.isWidgetType():
                    widget.hide()    
            self.secondTrainingOrTest_frame.show()
            widgets_second()
            
        def showTrainingFrame():
            for widget in self.main_panel_frame.children():
                if widget.isWidgetType():
                    widget.hide()    
            self.training_frame.show()
            widgets_training()
        
        def showTestFrame():
            for widget in self.main_panel_frame.children():
                if widget.isWidgetType():
                    widget.hide()    
            self.test_frame.show()
            widgets_test()
        
        
        def widgets_second():
            self.selected_theme = self.theme_combo.currentText()
            self.selected_index = int(self.theme_combo.currentIndex())
            
            self.theme_worked_label = CreateWidgets.get_label(self.secondTrainingOrTest_frame,
                                                    (self.screen.width()//2-400, 10, 800, 50),
                                                    self.selected_theme,
                                                    ("Arial", 14),
                                                    'background-color: rgb(255, 255, 255);border-radius: 10px;')
            self.traininng_button = CreateWidgets.get_button(self.secondTrainingOrTest_frame,
                                                    (10, 10, 200, 100),
                                                    'Презентация',
                                                    ('Arial', 14),
                                                    'background-color: rgb(255, 255, 255);border-radius: 10px;')
            self.test_button = CreateWidgets.get_button(self.secondTrainingOrTest_frame,
                                                    (250, 10, 200, 100),
                                                    'Тест',
                                                    ('Arial', 14),
                                                    'background-color: rgb(255, 255, 255);border-radius: 10px;')
            self.back_button = CreateWidgets.get_button(self.secondTrainingOrTest_frame,
                                                    (self.screen.width()-230, 10, 100, 50),
                                                    'Назад',
                                                    ('Arial', 14),
                                                    'background-color: rgb(231, 76, 60);border-radius: 10px;')
            self.traininng_button.clicked.connect(showTrainingFrame)
            self.test_button.clicked.connect(showTestFrame)
            self.back_button.clicked.connect(show_firstChoiceTheme)
            
            
        def widgets_training():
            self.slide_index = 0
            def back_slide():
                self.slide_index -= 1
                show_slide()
            
            def prev_slide():
                self.slide_index += 1
                show_slide()
                
            def show_slide():
                if type(alltraining[self.selected_index]) == list:
                    title = alltraining[self.selected_index][self.slide_index]['title']
                    photo = alltraining[self.selected_index][self.slide_index]['photo']
                    desc = alltraining[self.selected_index][self.slide_index]['desc']
                    num_slide = str(self.slide_index + 1)+'/'+str(len(alltraining[self.selected_index]))
                else:
                    title = alltraining[self.selected_index]['title']
                    photo = alltraining[self.selected_index]['photo']
                    desc = alltraining[self.selected_index]['desc']
                    num_slide = str(self.slide_index + 1)+'/'+str(len(alltraining[self.selected_index]))
                    
                self.theme_label.setText(title)
                self.numSlide.setText(num_slide)
                p = QPixmap(photo)
                print(photo)
                scaled_pixmap = p.scaled(self.photo_label.size(), aspectRatioMode=Qt.KeepAspectRatio)
                self.photo_label.setPixmap(scaled_pixmap)

                self.desc_label.setText(desc)
                
            
            self.numSlide = CreateWidgets.get_label(self.training_frame,
                                                    (self.screen.width()-175, self.screen.height()-80, 50, 50),
                                                    '0',
                                                    ("Arial", 14),
                                                    'background-color: rgb(255, 255, 255);border-radius: 10px;')
            
            self.theme_label = CreateWidgets.get_label(self.training_frame,
                                                    (10, 10, 800, 50),
                                                    self.selected_theme,
                                                    ("Arial", 14),
                                                    'background-color: rgb(255, 255, 255);border-radius: 10px;')
            self.theme_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.photo_label = CreateWidgets.get_label(self.training_frame,
                                                    (self.screen.width()//2+25, 10, 800, 800),
                                                    '',
                                                    ("Arial", 14),
                                                    'background-color: rgb(255, 255, 255);border-radius: 10px;')
            
            
            self.desc_label = CreateWidgets.get_label(self.training_frame,
                                                    (10, 100, 800, 500),
                                                    '',
                                                    ("Arial", 14),
                                                    'background-color: rgb(255, 255, 255);border-radius: 10px;')
            self.desc_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            
            self.back_slide_button = CreateWidgets.get_button(self.training_frame,
                                                     (10, 700, 100, 50),
                                                    'Назад',
                                                    ("Arial", 12),
                                                    'background-color: rgb(255, 255, 255);border-radius: 10px;')
            self.prev_slide_button = CreateWidgets.get_button(self.training_frame,
                                                     (200, 700, 100, 50),
                                                    'Вперед',
                                                    ("Arial", 12),
                                                    'background-color: rgb(255, 255, 255);border-radius: 10px;')

            self.goToTest_button = CreateWidgets.get_button(self.training_frame,
                                                     (self.screen.width()-300, self.screen.height()-80, 100, 50),
                                                    'Тест',
                                                    ("Arial", 12),
                                                    'background-color:#27ae60;border-radius: 10px;')

            self.exit_button = CreateWidgets.get_button(self.training_frame,
                                                     (10, self.screen.height()-80, 100, 50),
                                                    'Выйти',
                                                    ("Arial", 12),
                                                    'background-color:rgb(231, 76, 60);border-radius: 10px;')
            show_slide()                                       
            self.back_slide_button.clicked.connect(back_slide)                                         
            self.prev_slide_button.clicked.connect(prev_slide) 
            self.goToTest_button.clicked.connect(showTestFrame)
            self.exit_button.clicked.connect(show_firstChoiceTheme) 
            



        def widgets_test():
            start_time = None
            def show_result(result, elapsed_time):
                self.result_label.setText(f'Тест: {result}\nВремя: {elapsed_time} секунд')
                self.result_label.setVisible(True)
                
                user_id = int(self.user_id)
                task_id = int(self.selected_index + 1)
                completion_result = '1' if result == 'Сдан' else '0'
                
                if requestsSQL.check_task_completion(self.BD, user_id, task_id):
                    requestsSQL.update_task_completion(self.BD, user_id, task_id, elapsed_time, completion_result)
                else:
                    requestsSQL.insert_task_completion(self.BD, user_id, task_id, elapsed_time, completion_result)
            
            def check_results():
                nonlocal start_time
                end_time = time.time()
                elapsed_time = int(end_time - start_time)
                combo_box_values = {}
                for combo_box in self.combo_boxes:
                    combo_box_value = combo_box.currentText()
                    combo_box_values[combo_box_value] = combo_box.currentText()

                expected_positions = result
                incorrect_values = []
                for key, value in expected_positions.items():
                    print(combo_box_values.get(key), key)
                    if combo_box_values.get(key) != key:
                        incorrect_values.append(key)

                if incorrect_values:
                    show_result('Не сдан', elapsed_time)
                else:
                    show_result('Сдан', elapsed_time)

            def start_timer():
                nonlocal start_time
                start_time = time.time()

            pairs = allTest[self.selected_index].split(', ')
            result = {}
            for pair in pairs:
                key, value = pair.split(':')
                result[key.strip()] = int(value)

            self.combo_boxes = []
            y_position = 10
            for key, value in result.items():
                combo_box = QComboBox(self.test_frame)
                combo_box.setGeometry(10, y_position, 700, 50)
                combo_box.setFont(QFont("Arial", 12))
                combo_box.setVisible(True)
                combo_box.setStyleSheet(f'background-color:rgb(231, 76, 120)')
                random_data = list(result)
                random.shuffle(random_data)
                for option_key in random_data:
                    combo_box.addItem(option_key)
                combo_box.setCurrentIndex(-1)
                self.combo_boxes.append(combo_box)
                y_position += 55

            self.check_result_button = CreateWidgets.get_button(self.test_frame,
                                                                (self.screen.width()-250, self.screen.height() - 100, 100, 50),
                                                                'Проверить',
                                                                ("Arial", 12),
                                                                'background-color:rgb(0, 250, 60);border-radius: 10px;')
            self.result_label = CreateWidgets.get_label(self.test_frame,
                                                                (self.screen.width()-410, 10, 250, 100),
                                                                f'',
                                                                ("Arial", 14),
                                                                'background-color: rgb(255, 255, 255);border-radius: 10px;',
                                                                False)
            self.exitFromTest_button = CreateWidgets.get_button(self.test_frame,
                                                                (self.screen.width()-400, self.screen.height() - 100, 100, 50),
                                                                'Выйти',
                                                                ("Arial", 12),
                                                                'background-color:rgb(0, 250, 60);border-radius: 10px;')
            self.check_result_button.clicked.connect(check_results)
            self.exitFromTest_button.clicked.connect(show_firstChoiceTheme)
            start_timer()


        self.main_panel_frame = QFrame(self.main_frame)
        self.main_panel_frame.setGeometry(100, 0, self.screen.width()-100, self.screen.height())
        self.main_panel_frame.setStyleSheet('background-color:rgb(75, 75, 75)')
        self.main_panel_frame.setVisible(True)
        
        main_panel_layout = QHBoxLayout(self.main_panel_frame)
        
        self.firstChoiceTheme_frame = QFrame()
        self.firstChoiceTheme_frame.setStyleSheet('background-color: rgb(0, 200, 150); border-radius: 10px;')
        main_panel_layout.addWidget(self.firstChoiceTheme_frame)
        
        self.secondTrainingOrTest_frame = QFrame()
        self.secondTrainingOrTest_frame.setStyleSheet('background-color: rgb(0, 200, 150); border-radius: 10px;')
        main_panel_layout.addWidget(self.secondTrainingOrTest_frame)
        self.secondTrainingOrTest_frame.hide()
        
        self.training_frame = QFrame()
        self.training_frame.setStyleSheet('background-color: rgb(0, 200, 150); border-radius: 10px;')
        main_panel_layout.addWidget(self.training_frame)
        self.training_frame.hide()
        
        self.test_frame = QFrame()
        self.test_frame.setStyleSheet('background-color: rgb(0, 200, 150); border-radius: 10px;')
        main_panel_layout.addWidget(self.test_frame)
        self.test_frame.hide()
        
        self.theme_combo = QComboBox(self.firstChoiceTheme_frame)
        self.theme_combo.setGeometry(20, 20, 700, 50)
        self.theme_combo.setStyleSheet('background-color: rgb(255, 255, 255)')
        self.theme_combo.setFont(QFont('Arrial', 14))
        self.theme_combo.setVisible(True)
        for data in requestsSQL.read_tasks(self.BD):
            dict_data = json.loads(data[1])
            self.theme_combo.addItem(dict_data[0]['title']) if type(dict_data) == list else self.theme_combo.addItem(dict_data['title'])
            allTest.append(data[-1])
            alltraining.append(dict_data)
        self.theme_combo.setCurrentIndex(-1)
        
        self.choice_button = CreateWidgets.get_button(self.firstChoiceTheme_frame,
                                                     (850, 25, 200, 100),
                                                    'Выбрать',
                                                    ("Arial", 12),
                                                    'background-color: rgb(255, 255, 255);border-radius: 10px;')
        self.choice_button.clicked.connect(show_secondTrainingOrTestFrame)
        
 
        
    def close_program(self):
        exit()






