import sqlite3
import sys
from PyQt6.QtWidgets import QFileDialog, QApplication, QTableWidgetItem, QRadioButton, QMainWindow, QToolBar, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt6.QtGui import QAction

class Registration(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(QLabel('Регистрация'))

        # фамилия
        self.surname_lineedit = QLineEdit()
        surname = QHBoxLayout()
        surname.addWidget(QLabel('Фамилия:'))
        surname.addWidget(self.surname_lineedit)
        main_layout.addLayout(surname)

        # имя
        self.name_lineedit = QLineEdit()
        name = QHBoxLayout()
        name.addWidget(QLabel('Имя:'))
        name.addWidget(self.name_lineedit)
        main_layout.addLayout(name)

        # отчество
        self.otchestvo_lineedit = QLineEdit()
        otchestvo = QHBoxLayout()
        otchestvo.addWidget(QLabel('Отчество:'))
        otchestvo.addWidget(self.otchestvo_lineedit)
        main_layout.addLayout(otchestvo)

        # возраст
        self.age_lineedit = QLineEdit()
        age = QHBoxLayout()
        age.addWidget(QLabel('Возраст:'))
        age.addWidget(self.age_lineedit)
        main_layout.addLayout(age)

        # email
        self.email_lineedit = QLineEdit()
        email = QHBoxLayout()
        email.addWidget(QLabel('Email:'))
        email.addWidget(self.email_lineedit)
        main_layout.addLayout(email)

        # телефон
        self.tel_lineedit = QLineEdit()
        tel = QHBoxLayout()
        tel.addWidget(QLabel('Номер телефона:'))
        tel.addWidget(self.tel_lineedit)
        main_layout.addLayout(tel)

        # пароль
        self.password_lineedit = QLineEdit()
        password = QHBoxLayout()
        password.addWidget(QLabel('Пароль:'))
        password.addWidget(self.password_lineedit)
        main_layout.addLayout(password)

        # загрузить pdf файл
        self.upload_resume_button = QPushButton('Загрузить резюме')
        self.upload_resume_button.clicked.connect(self.upload_resume)
        main_layout.addWidget(self.upload_resume_button)

        self.ok_button = QPushButton('ОК')
        self.ok_button.clicked.connect(self.create_candidate)
        main_layout.addWidget(self.ok_button)

    def upload_resume(self):
        filedialog = QFileDialog(self)
        filedialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        if filedialog.exec():
            fileNames = filedialog.selectedFiles()
        file_path = fileNames[0]
        with open(file_path, 'rb') as file:
            self.doc = file.read()


    def create_candidate(self):
        doc = getattr(self, 'doc', None)
        name, surname, otchestvo, age, email, tel, password = self.name_lineedit.text(), self.surname_lineedit.text(), \
            self.otchestvo_lineedit.text(), self.age_lineedit.text(), self.email_lineedit.text(), \
            self.tel_lineedit.text(), self.password_lineedit.text()
        try:
            age = int(age)
        except:
            msgdlg = QDialog(self)
            layout = QVBoxLayout()
            layout.addWidget(QLabel('Некорректные входные данные'))
            msgdlg.setLayout(layout)
            msgdlg.exec()
            return

        # проверяет наличие кандидата в базе
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(
                f'''select * from candidate where surname='{surname}' and name='{name}' and otchestvo='{otchestvo}'
                                    and age={age} and email='{email}' ''')
            res = cur.fetchall()

        if len(res) == 0:  # если такого кандидата нет
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                print((surname, name, otchestvo, password, age, doc, email, tel))
                cur.execute(f'''insert into candidate (surname, name, otchestvo, password, age, doc, email, tel) 
                                    values(?, ?, ?, ?, ?, ?, ?, ?)''', (surname, name, otchestvo, password, age,
                                                                        doc, email, tel))
        else:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(f'''update candidate set password='{password}' where id={res[0][0]}''')

        self.close()
