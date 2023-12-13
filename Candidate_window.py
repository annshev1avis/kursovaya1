import sqlite3
import sys
from PyQt6.QtWidgets import QFileDialog, QApplication, QTableWidgetItem, QRadioButton, QMainWindow, QToolBar, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt6.QtGui import QAction

#отображается в окне кандидата, в доступных вакансиях
class User_vacancy_card(QWidget):
    def __init__(self, candidate_id, vacancy_id, name, salary, graphic, location):
        super().__init__()
        print(vacancy_id, name, salary, graphic, location)
        self.vacancy_id = vacancy_id
        self.candidate_id = candidate_id
        self.name = name
        self.salary = salary
        self.graphic = graphic
        self.location = location

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        info = QVBoxLayout()
        info.addWidget(QLabel(self.name))
        info.addWidget(QLabel(str(self.salary)))
        info.addWidget(QLabel(self.graphic))
        info.addWidget(QLabel(self.location))
        self.main_layout.addLayout(info)

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print(f'''select * from zayavka where vacancy_id={self.vacancy_id} and candidate_id={self.candidate_id}''')
            cur.execute(f'''select * from zayavka where vacancy_id={self.vacancy_id} and candidate_id={self.candidate_id}''')
            res = cur.fetchall()

        if len(res) == 0:
            self.ok_button = QPushButton('Откликнуться')
            self.ok_button.clicked.connect(self.accept)
            self.main_layout.addWidget(self.ok_button)

    def accept(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('''insert into zayavka(vacancy_id, candidate_id) values(?, ?)''', (self.vacancy_id, self.candidate_id))
            print('ok')

"""class Profile(QWidget):
    def __init__(self):"""


#окно для роли Кандидат
class Candidate_window(QWidget):
    def __init__(self, candidate_id):
        super().__init__()
        self.candidate_id = candidate_id
        self.setGeometry(200, 200, 700, 350)

        self.mainlayout = QHBoxLayout()
        self.setLayout(self.mainlayout)


        # часть окна с информацией о кандидате
        profile = QVBoxLayout()
        profile.addWidget(QLabel('Мой профиль'))

        # фамилия
        surname_l = QHBoxLayout()
        surname_l.addWidget(QLabel('Фамилия:'))
        self.surname_le = QLineEdit()
        self.surname_le.setEnabled(False)
        surname_l.addWidget(self.surname_le)
        profile.addLayout(surname_l)

        #имя
        name_l = QHBoxLayout()
        name_l.addWidget(QLabel('Имя:'))
        self.name_le = QLineEdit()
        self.name_le.setEnabled(False)
        name_l.addWidget(self.name_le)
        profile.addLayout(name_l)

        #отчество
        otchestvo_l = QHBoxLayout()
        otchestvo_l.addWidget(QLabel('Отчество:'))
        self.otchestvo_le = QLineEdit()
        self.otchestvo_le.setEnabled(False)
        otchestvo_l.addWidget(self.otchestvo_le)
        profile.addLayout(otchestvo_l)

        #возраст
        age_l = QHBoxLayout()
        age_l.addWidget(QLabel('Возраст:'))
        self.age_le = QLineEdit()
        self.age_le.setEnabled(False)
        age_l.addWidget(self.age_le)
        profile.addLayout(age_l)

        #email
        email_l = QHBoxLayout()
        email_l.addWidget(QLabel('Email:'))
        self.email_le = QLineEdit()
        self.email_le.setEnabled(False)
        email_l.addWidget(self.email_le)
        profile.addLayout(email_l)

        #телефон
        tel_l = QHBoxLayout()
        tel_l.addWidget(QLabel('Телефон:'))
        self.tel_le = QLineEdit()
        self.tel_le.setEnabled(False)
        tel_l.addWidget(self.tel_le)
        profile.addLayout(tel_l)

        #кнопки про документ
        but_l = QHBoxLayout()
        self.view_CV_but = QPushButton('Посмотреть текцщее резюме')
        self.view_CV_but.clicked.connect(self.view_CV)
        self.upload_CV_but = QPushButton('Загрузить новое резюме')
        self.upload_CV_but.clicked.connect(self.upload_CV)
        but_l.addWidget(self.view_CV_but)
        but_l.addWidget(self.upload_CV_but)
        profile.addLayout(but_l)

        #кнопка изменить
        self.just_layout = QHBoxLayout()
        self.update_can_but = QPushButton('Редактировать профиль')
        self.update_can_but.clicked.connect(self.update_can)
        self.just_layout.addWidget(self.update_can_but)
        self.commit_but = QPushButton('Сохранить')
        self.commit_but.clicked.connect(self.commit)
        self.just_layout.addWidget(self.commit_but)
        profile.addLayout(self.just_layout)

        profile.addStretch()

        #часть окна с вакансиями
        vacancies = QVBoxLayout()
        vacancies.addWidget(QLabel('Доступные вакансии'))
        self.vacancies_table = QTableWidget()
        self.vacancies_table.setColumnCount(1)
        self.vacancies_table.verticalHeader().setVisible(False)
        self.vacancies_table.horizontalHeader().setVisible(False)
        self.vacancies_table.horizontalHeader().setStretchLastSection(True)
        vacancies.addWidget(self.vacancies_table)

        self.mainlayout.addLayout(profile)
        self.mainlayout.addLayout(vacancies)

        self.update_but = QPushButton('Обновить')
        self.update_but.clicked.connect(self.update_all_data)
        self.update_but.setFixedWidth(75)
        self.mainlayout.addWidget(self.update_but)

        #загрузка инфы
        self.load_vacancies()
        self.load_candidate_data()

    def view_CV(self):
        pass

    def upload_CV(self):
        pass

    def update_all_data(self):
        self.load_vacancies()
        self.load_candidate_data()

    def update_can(self):
        #делает редактируемыми поля с инфой
        self.surname_le.setEnabled(True)
        self.name_le.setEnabled(True)
        self.otchestvo_le.setEnabled(True)
        self.age_le.setEnabled(True)
        self.email_le.setEnabled(True)
        self.tel_le.setEnabled(True)

    def commit(self):
        #записывает изменения о кандидате
        self.surname_le.setEnabled(False)
        self.name_le.setEnabled(False)
        self.otchestvo_le.setEnabled(False)
        self.age_le.setEnabled(False)
        self.email_le.setEnabled(False)
        self.tel_le.setEnabled(False)

        surname, name, otchestvo, age, email, tel = self.surname_le.text(), self.name_le.text(), self.otchestvo_le.text(), \
            self.age_le.text(), self.email_le.text(), self.tel_le.text()

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'''update candidate set surname='{surname}', name='{name}', otchestvo='{otchestvo}', 
                        age={age}, email='{email}', tel='{tel}'
                        where id={self.candidate_id}''')

        print('hhh')

    def load_candidate_data(self):
        # получение данных о кандидате из БД
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print(f'select * from candidat where id={self.candidate_id}')
            cur.execute(f'select * from candidate where id={self.candidate_id}')
            res = cur.fetchall()[0]
            surname, name, otchestvo, age, email, tel = res[1], res[2], res[3], res[5], res[7], res[8]
            print(res)

        self.surname_le.setText(surname)
        self.name_le.setText(name)
        self.otchestvo_le.setText(otchestvo)
        self.age_le.setText(str(age))
        self.email_le.setText(email)
        self.tel_le.setText(tel)

    def load_vacancies(self):
        print('*')
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('''select * from vacancy where status='open' ''')
            print('*')
            res = cur.fetchall()

        for vac in res:
            print((self.candidate_id, vac[0], vac[1], vac[4], vac[5], vac[6]))
        vacancies_lst = [User_vacancy_card(self.candidate_id, vac[0], vac[1], vac[4], vac[5], vac[6]) for vac in res]
        print('*')
        self.vacancies_table.setRowCount(len(vacancies_lst))
        for i, vac in enumerate(vacancies_lst):
            print('*')
            self.vacancies_table.setCellWidget(i, 0, vac)
            self.vacancies_table.setRowHeight(i, 190)