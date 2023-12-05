import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QRadioButton, QMainWindow, QToolBar, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from Vacancy import Vacancy
import sqlite3 as sq
from PyQt6.QtGui import QAction


class NewVacancyDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Новая вакансия')

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel('Новая вакансия'))

        #название
        self.name_le = QLineEdit()
        self.main_layout.addWidget(QLabel('Название:'))
        self.main_layout.addWidget(self.name_le)

        #предполагаемая дата закрытия
        self.enddate_le = QLineEdit()
        self.main_layout.addWidget(QLabel('Предполагаемая дата закрытия в формате год-месяц-день:'))
        self.main_layout.addWidget(self.enddate_le)

        #зарплата
        self.main_layout.addWidget(QLabel('Зарплата:'))
        self.salary_le = QLineEdit()
        self.main_layout.addWidget(self.salary_le)

        #график
        self.main_layout.addWidget(QLabel('График работы:'))
        self.graphic_le = QLineEdit()
        self.main_layout.addWidget(self.graphic_le)

        #локация
        self.main_layout.addWidget(QLabel('Локация:'))
        self.location_le = QLineEdit()
        self.main_layout.addWidget(self.location_le)

        #кнопка Создать
        self.create_button = QPushButton('Создать')
        self.create_button.clicked.connect(self.create)
        self.main_layout.addWidget(self.create_button)

        self.setLayout(self.main_layout)

    @staticmethod
    def chech_date(date):
        if date == '':
            return False
        date_lst = date.split('-')
        if len(date_lst) != 3:
            return False
        if [len(x) for x in date_lst] != [4, 2, 2]:
            return False
        for x in date_lst:
            try:
                int(x)
            except:
                return False
        return True

    @staticmethod
    def check_int(num):
        try:
            a = int(num)
            return True
        except:
            return False

    def create(self):
        name, enddate = self.name_le.text(), self.enddate_le.text()
        salary, graphic, location = self.salary_le.text(), self.graphic_le.text(), self.location_le.text()

        if name != '' and self.chech_date(enddate) and self.check_int(salary) and graphic != '' and location != '': #корректность введенных данных
            self.close()
        else:
            msgdlg = QDialog(self)
            layout = QVBoxLayout()
            layout.addWidget(QLabel('Некорректные входные данные'))
            msgdlg.setLayout(layout)
            msgdlg.exec()
            return
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print((name, enddate, int(salary), graphic, location))
            cur.execute('''insert into vacancy(name, end_date, salary, graphic, location) values(?, ?, ?, ?, ?)''', (name, enddate, int(salary), graphic, location))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('HR помощник')
        self.setGeometry(100, 100, 1000, 550)

        #главный layout
        self.main_layout = QHBoxLayout()

        #КОЛОНКА ВАКАНСИИ СЛЕВА
        vacancies_column = QVBoxLayout()
        vacancies_column.addWidget(QLabel('Вакансии'))

        #вкладки открытые/архив
        open_arhiv = QHBoxLayout()
        self.open_button = QPushButton('Открытые')
        self.open_button.clicked.connect(self.load_open_vacancies)
        self.arhiv_button = QPushButton('Закрытые')
        self.arhiv_button.clicked.connect(self.load_close_vacancies)
        open_arhiv.addWidget(self.open_button)
        open_arhiv.addWidget(self.arhiv_button)
        vacancies_column.addLayout(open_arhiv)


        #таблица с вакансиями
        self.vacancies = QTableWidget()
        self.vacancies.setMaximumWidth(300)
        self.vacancies.verticalHeader().setVisible(False)
        self.vacancies.horizontalHeader().setVisible(False)
        self.vacancies.horizontalHeader().setStretchLastSection(True)
        vacancies_column.addWidget(self.vacancies)
        self.vacancies.setColumnCount(1)
        self.load_open_vacancies()

        #кнопка Новая вакансия
        self.new_vacancy_button = QPushButton('Новая вакансия')
        self.new_vacancy_button.clicked.connect(self.new_vacancy)
        vacancies_column.addWidget(self.new_vacancy_button)

        #установка main_layout
        self.main_layout.addLayout(vacancies_column)
        self.main_layout.addWidget(QLabel(''))
        #self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def new_vacancy(self):
        new_vacancy_dialog = NewVacancyDialog(self)
        new_vacancy_dialog.exec()

    def load_open_vacancies(self):
        """заполнение таблицы открытыми вакансиями"""
        self.load_vacancies(status='open')

    def load_close_vacancies(self):
        """заполнение таблицы закрытыми вакансиями"""
        self.load_vacancies(status='close')

    def load_vacancies(self, status):
        # выгрузка вакансий из бд в vacancy_lst (список из объектов Vacancy)
        with sq.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"select id, name, end_date, status from vacancy where status='{status}'")
            vacancy_lst = cur.fetchall()
            print(vacancy_lst)
        vacancy_lst = [Vacancy(*vac, self) for vac in vacancy_lst]
        self.vacancies.setRowCount(len(vacancy_lst))

        # загрузка вакансий в таблицу self.vacancies
        for i, v in enumerate(vacancy_lst):
            self.vacancies.setCellWidget(i, 0, v.menu_widget)
            self.vacancies.setRowHeight(i, 80)

def init_db():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("""create table if not exists vacancy(
                        id integer primary key autoincrement, 
                        name text,
                        end_date text,
                        status text default 'open',
                        salary int,
                        graphic text,
                        location text
                        )""")

        cur.execute("""create table if not exists candidate(
                        id integer primary key autoincrement,
                        surname text,
                        name text,
                        otchestvo text,
                        password text,
                        age integer,
                        doc blob,
                        email text,
                        tel text
                        )""")

        cur.execute("""create table if not exists zayavka(
                        candidate_id integer,
                        vacancy_id integer,
                        watched integer default 0,
                        status text default 'resume',
                        id integer primary key autoincrement,
                        foreign key(candidate_id) references candidate(id),
                        foreign key(vacancy_id) references vacancy(id))""")

        cur.execute("""create table if not exists zametka(
                    id integer primary key autoincrement,
                    text text,
                    zayavka_id integer,
                    foreign key(zayavka_id) references zayavka(id)
                    )""")

#обёртка для класса MainWindow
class RealMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #добавдение виджета MainWindow
        self.main_window_widget = MainWindow()
        self.setWindowTitle('HR помощник')
        self.setGeometry(100, 100, 1000, 550)
        self.setCentralWidget(self.main_window_widget)

        #добавление меню сверху
        button_statistic = QAction('Показать статистику', self)
        button_statistic.triggered.connect(self.statistic_win)
        button_settings = QAction('Настройки', self)
        button_settings.triggered.connect(self.settings_win)
        toolbar = QToolBar('Статистика')
        toolbar.addAction(button_statistic)
        self.addToolBar(toolbar)

    def statistic_win(self):
        print('ok')

    def settings_win(self):
        pass


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


#окно для роли Кандидат
class Candidate_window(QWidget):
    def __init__(self, candidate_id):
        super().__init__()
        #получение данных о кандидате из БД
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print(f'select * from candidat where id={candidate_id}')
            cur.execute(f'select * from candidate where id={candidate_id}')
            res = cur.fetchall()[0]
            surname, name, otchestvo, age, email, tel = res[1], res[2], res[3], res[5], res[7], res[8]
            print(res)
        self.candidate_id = candidate_id
        #часть окна с информацией о кандидате
        self.mainlayout = QHBoxLayout()
        self.setLayout(self.mainlayout)
        profile = QVBoxLayout()
        profile.addWidget(QLabel('Мой профиль'))
        profile.addWidget(QLabel('Имя: ' + name))
        profile.addWidget(QLabel('Фамилия: ' + surname))
        profile.addWidget(QLabel('Возраст: ' + str(age)))
        profile.addWidget(QLabel('Email: ' + email))
        profile.addWidget(QLabel('Телефон: ' + tel))

        #часть окна с вакансиями
        vacancies = QVBoxLayout()
        vacancies.addWidget(QLabel('Доступные вакансии'))
        self.vacancies_table = QTableWidget()
        self.vacancies_table.setColumnCount(1)
        self.vacancies_table.verticalHeader().setVisible(False)
        self.vacancies_table.horizontalHeader().setVisible(False)
        self.vacancies_table.horizontalHeader().setStretchLastSection(True)
        vacancies.addWidget(self.vacancies_table)
        self.load_vacancies()

        self.mainlayout.addLayout(profile)
        self.mainlayout.addLayout(vacancies)

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
        print('upload_resume')
        filedialog = QFileDialog(self)
        print(0)
        filedialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        print(0)
        if filedialog.exec():
            fileNames = filedialog.selectedFiles()
        file_path = fileNames[0]
        with open(file_path) as file:
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
                                    values(?, ?, ?, ?, ?, ?, ?)''', (surname, name, otchestvo, password, age, doc, email, tel))
        else:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(f'''update candidate set password='{password}' ''')

        self.close()


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
        layout.addWidget(QLabel('чтобы войти как кандидат: Маус, Микки, qwerty'))

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
        elif surname=='hr' and name=='hr' and password=='hr':
            self.main_window = RealMainWindow()
            self.main_window.show()
            self.close()

    def reg(self):
        self.reg = Registration()
        self.reg.show()

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    auth = Authorithation()
    auth.show()
    sys.exit(app.exec())
