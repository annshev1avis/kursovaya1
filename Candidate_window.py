import sqlite3
import sys
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QApplication, QTableWidgetItem, QRadioButton, QMainWindow, QToolBar, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt6.QtGui import QAction
import subprocess
import tempfile

#отображается в окне кандидата, в доступных вакансиях
class User_vacancy_card(QWidget):
    def __init__(self, candidate_id, vacancy_id, name, salary, graphic, location, parent):
        super().__init__()
        print(vacancy_id, name, salary, graphic, location)
        self.vacancy_id = vacancy_id
        self.candidate_id = candidate_id
        self.name = name
        self.salary = salary
        self.graphic = graphic
        self.location = location
        self.parent = parent
        self.init_UI()

    def init_UI(self):
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

        print(res)
        if len(res) == 0:
            print('ok')
            self.ok_button = QPushButton('Откликнуться')
            self.ok_button.clicked.connect(self.accept)
            self.main_layout.addWidget(self.ok_button)
            print('ok')
        else:
            print('not ok')
            self.not_ok_button = QPushButton('Отозвать резюме')
            self.not_ok_button.clicked.connect(self.cancel)
            self.main_layout.addWidget(self.not_ok_button)
            print('not ok')

    def accept(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('''insert into zayavka(vacancy_id, candidate_id) values(?, ?)''', (self.vacancy_id, self.candidate_id))
            print('ok')
        self.parent.update_all_data()

    def cancel(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print(f'''delete from zayavka where vacancy_id={self.vacancy_id} and candidate_id={self.candidate_id}''')
            cur.execute(f'''delete from zayavka where vacancy_id={self.vacancy_id} and candidate_id={self.candidate_id}''')
        self.parent.update_all_data()

# часть окна с информацией о кандидате
class Profile(QWidget):
    def __init__(self, candidate_id):
        super().__init__()

        self.candidate_id = candidate_id

        profile = QVBoxLayout()
        profile.addWidget(QLabel('Мой профиль'))
        self.setLayout(profile)
        self.setFixedWidth(350)

        # фамилия
        surname_l = QHBoxLayout()
        surname_l.addWidget(QLabel('Фамилия:'))
        self.surname_le = QLineEdit()
        self.surname_le.setEnabled(False)
        surname_l.addWidget(self.surname_le)
        profile.addLayout(surname_l)

        # имя
        name_l = QHBoxLayout()
        name_l.addWidget(QLabel('Имя:'))
        self.name_le = QLineEdit()
        self.name_le.setEnabled(False)
        name_l.addWidget(self.name_le)
        profile.addLayout(name_l)

        # отчество
        otchestvo_l = QHBoxLayout()
        otchestvo_l.addWidget(QLabel('Отчество:'))
        self.otchestvo_le = QLineEdit()
        self.otchestvo_le.setEnabled(False)
        otchestvo_l.addWidget(self.otchestvo_le)
        profile.addLayout(otchestvo_l)

        # возраст
        age_l = QHBoxLayout()
        age_l.addWidget(QLabel('Возраст:'))
        self.age_le = QLineEdit()
        self.age_le.setEnabled(False)
        age_l.addWidget(self.age_le)
        profile.addLayout(age_l)

        # email
        email_l = QHBoxLayout()
        email_l.addWidget(QLabel('Email:'))
        self.email_le = QLineEdit()
        self.email_le.setEnabled(False)
        email_l.addWidget(self.email_le)
        profile.addLayout(email_l)

        # телефон
        tel_l = QHBoxLayout()
        tel_l.addWidget(QLabel('Телефон:'))
        self.tel_le = QLineEdit()
        self.tel_le.setEnabled(False)
        tel_l.addWidget(self.tel_le)
        profile.addLayout(tel_l)

        # кнопки про документ
        but_l = QHBoxLayout()
        self.view_CV_but = QPushButton('Посмотреть текущее резюме')
        self.view_CV_but.clicked.connect(self.view_CV)
        self.upload_CV_but = QPushButton('Загрузить новое резюме')
        self.upload_CV_but.clicked.connect(self.upload_CV)
        but_l.addWidget(self.view_CV_but)
        but_l.addWidget(self.upload_CV_but)
        profile.addLayout(but_l)

        # кнопка изменить
        self.just_layout = QHBoxLayout()
        self.update_can_but = QPushButton('Редактировать профиль')
        self.update_can_but.clicked.connect(self.update_can)
        self.just_layout.addWidget(self.update_can_but)
        self.commit_but = QPushButton('Сохранить')
        self.commit_but.clicked.connect(self.commit)
        self.just_layout.addWidget(self.commit_but)
        profile.addLayout(self.just_layout)

        profile.addStretch()
        self.load_candidate_data()

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

    def view_CV(self):
        print('VIEW CV')
        # читается файл из бд
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print('bef doc')
            cur.execute(f"""select doc from candidate where id={self.candidate_id}""")
            print('af doc')
            doc = cur.fetchall()[0][0]

        if doc != None:
            print(1)
            # создается временный файл из байтовых данных doc
            temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
            temp_file.write(doc)
            temp_file.close()
            print(1)
            # файл открывается в акробате
            file_path = temp_file.name
            app_path = 'C:/Program Files/Adobe/Acrobat DC/Acrobat/Acrobat.exe'
            print(file_path)
            try:
                subprocess.Popen([app_path, file_path])
            except FileNotFoundError:
                QMessageBox.warning(self, 'Ошибка', 'Не удалось найти программу для открытия PDF.')
        else:
            print('error')
            QMessageBox.warning(self, 'Ошибка', 'Нет файла')

    def upload_CV(self):
        print('UPLOAD CV')
        filedialog = QFileDialog(self)
        print(0)
        filedialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        print(0)
        if filedialog.exec():
            print('here1')
            fileNames = filedialog.selectedFiles()
            print('here2')
        file_path = fileNames[0]
        print(file_path)
        with open(file_path, 'rb') as file:
            doc = file.read()
        print(type(doc))
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'''update candidate set doc=? where id={self.candidate_id}''', (doc, ))


#окно для роли Кандидат
class Candidate_window(QWidget):
    def __init__(self, candidate_id):
        super().__init__()
        self.candidate_id = candidate_id
        self.setGeometry(200, 200, 800, 350)
        self.setWindowTitle('Мой профиль')
        self.mainlayout = QHBoxLayout()
        self.setLayout(self.mainlayout)
        self.profile_part = Profile(candidate_id)
        self.mainlayout.addWidget(self.profile_part)

        #часть окна с вакансиями
        vacancies = QVBoxLayout()
        vacancies.addWidget(QLabel('Доступные вакансии'))
        self.vacancies_table = QTableWidget()
        self.vacancies_table.setColumnCount(1)
        self.vacancies_table.verticalHeader().setVisible(False)
        self.vacancies_table.horizontalHeader().setVisible(False)
        self.vacancies_table.horizontalHeader().setStretchLastSection(True)
        vacancies.addWidget(self.vacancies_table)
        self.mainlayout.addLayout(vacancies)

        self.update_but = QPushButton('Обновить')
        self.update_but.clicked.connect(self.update_all_data)
        self.update_but.setFixedWidth(75)
        self.mainlayout.addWidget(self.update_but)

        #загрузка инфы
        self.update_all_data()

    def update_all_data(self):
        self.load_vacancies()
        self.profile_part.load_candidate_data()


    def load_vacancies(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('''select * from vacancy where status='open' ''')
            res = cur.fetchall()

        vacancies_lst = [User_vacancy_card(self.candidate_id, vac[0], vac[1], vac[4], vac[5], vac[6], self)
                         for vac in res]
        self.vacancies_table.setRowCount(len(vacancies_lst))
        for i, vac in enumerate(vacancies_lst):
            self.vacancies_table.setCellWidget(i, 0, vac)
            self.vacancies_table.setRowHeight(i, 190)

