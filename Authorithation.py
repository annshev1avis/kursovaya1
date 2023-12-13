import sqlite3
import sys
from PyQt6.QtWidgets import QFileDialog, QApplication, QTableWidgetItem, QRadioButton, QMainWindow, QToolBar, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt6.QtGui import QAction
from HR_window import RealMainWindow
from Candidate_window import Candidate_window
from Registration import Registration

class Authorithation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')

        self.surname = QLineEdit()
        self.name = QLineEdit()
        self.password = QLineEdit()
        self.enter_button = QPushButton('Войти')
        self.enter_button.clicked.connect(self.enter)
        self.reg_button = QPushButton('Зарегистрироваться как кандидат')
        self.reg_button.clicked.connect(self.reg)

        #расположение на layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Фамилия:'))
        layout.addWidget(self.surname)
        layout.addWidget(QLabel('Имя:'))
        layout.addWidget(self.name)
        layout.addWidget(QLabel('Пароль:'))
        layout.addWidget(self.password)
        layout.addWidget(self.enter_button)
        layout.addWidget(self.reg_button)
        layout.addWidget(QLabel('чтобы войти как hr: hr, hr, hr'))
        layout.addWidget(QLabel('чтобы войти как кандидат: Маус, Микки, 1'))

        self.setLayout(layout)

    def enter(self):
        surname, name, password = self.surname.text(), self.name.text(), self.password.text()
        print(surname, name, password)

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'''select * from candidate where surname='{surname}' and name='{name}' and password='{password}' ''')
            res = cur.fetchall()
            print(res)

        if len(res) > 0:
            print('id', res[0][0])
            self.candidate_window = Candidate_window(res[0][0])
            self.candidate_window.show()
            self.close()
        elif surname=='' and name=='' and password=='':
            self.main_window = RealMainWindow()
            self.main_window.show()
            self.close()

    def reg(self):
        self.reg = Registration()
        self.reg.show()