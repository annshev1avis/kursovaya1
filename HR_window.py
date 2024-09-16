import sqlite3
import sys
from PyQt6.QtWidgets import QFileDialog, QApplication, QTableWidgetItem, QRadioButton, QMainWindow, QToolBar, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from Vacancy import Vacancy
import sqlite3 as sq
from PyQt6.QtGui import QAction

class Statistic_win(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(100, 100, 900, 450)
        self.setWindowTitle('Статистика')
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(QLabel('Анализ воронки рекрутмента'))

        layout = QHBoxLayout()
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('''select name from vacancy''')
            vacs = [x[0] for x in cur.fetchall()]
            print(vacs)

        # таблица с выбором вакансии
        self.vacs_table = QTableWidget()
        self.vacs_table.setColumnCount(1)
        self.vacs_table.setRowCount(len(vacs))
        self.vacs_table.setFixedWidth(200)
        for i, vac in enumerate(vacs):
            self.vacs_table.setItem(i, 0, QTableWidgetItem(vac))
        self.vacs_table.cellClicked.connect(self.choose_vac)
        layout.addWidget(self.vacs_table)

        # таблица с результатами
        self.res_table = QTableWidget()
        self.res_table.setColumnCount(3)
        self.res_table.setRowCount(4)
        self.res_table.setColumnWidth(0, 150)
        self.res_table.setColumnWidth(1, 150)
        self.res_table.setColumnWidth(2, 150)

        self.res_table.setHorizontalHeaderLabels(["Всего кандидатов", "На рассмотрении", "Отказано"])
        self.res_table.setVerticalHeaderLabels(["Просмотр резюме", "Разговор по телефону", "Собеседование", "Оффер"])
        layout.addWidget(self.res_table)

        main_layout.addLayout(layout)


    def choose_vac(self, i, j):
        vac_name = self.vacs_table.item(i, j).text()
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'''select id from vacancy where name='{vac_name}' ''')
            vac_id = cur.fetchall()[0][0]
            print(vac_id)

            # резюме
            cur.execute(
                f'''select count(*) from zayavka where (status='resume' or prev_status='resume') and vacancy_id={vac_id}''')
            self.res_table.setItem(0, 0, QTableWidgetItem(str(cur.fetchall()[0][0])))
            cur.execute(f'''select count(*) from zayavka where status='resume' and vacancy_id={vac_id}''')
            self.res_table.setItem(0, 1, QTableWidgetItem(str(cur.fetchall()[0][0])))
            cur.execute(f'''select count(*) from zayavka where prev_status='resume' and vacancy_id={vac_id}''')
            self.res_table.setItem(0, 2, QTableWidgetItem(str(cur.fetchall()[0][0])))

            # телефон
            cur.execute(
                f'''select count(*) from zayavka where (status='tel' or prev_status='tel') and vacancy_id={vac_id}''')
            self.res_table.setItem(1, 0, QTableWidgetItem(str(cur.fetchall()[0][0])))
            cur.execute(f'''select count(*) from zayavka where status='tel' and vacancy_id={vac_id}''')
            self.res_table.setItem(1, 1, QTableWidgetItem(str(cur.fetchall()[0][0])))
            cur.execute(f'''select count(*) from zayavka where prev_status='tel' and vacancy_id={vac_id}''')
            self.res_table.setItem(1, 2, QTableWidgetItem(str(cur.fetchall()[0][0])))

            # собес
            cur.execute(
                f'''select count(*) from zayavka where (status='sobes' or prev_status='sobes') and vacancy_id={vac_id}''')
            self.res_table.setItem(2, 0, QTableWidgetItem(str(cur.fetchall()[0][0])))
            cur.execute(f'''select count(*) from zayavka where status='sobes' and vacancy_id={vac_id}''')
            self.res_table.setItem(2, 1, QTableWidgetItem(str(cur.fetchall()[0][0])))
            cur.execute(f'''select count(*) from zayavka where prev_status='sobes' and vacancy_id={vac_id}''')
            self.res_table.setItem(2, 2, QTableWidgetItem(str(cur.fetchall()[0][0])))

            # оффер
            cur.execute(
                f'''select count(*) from zayavka where (status='offer' or prev_status='offer') and vacancy_id={vac_id}''')
            self.res_table.setItem(3, 0, QTableWidgetItem(str(cur.fetchall()[0][0])))
            cur.execute(f'''select count(*) from zayavka where status='offer' and vacancy_id={vac_id}''')
            self.res_table.setItem(3, 1, QTableWidgetItem(str(cur.fetchall()[0][0])))
            cur.execute(f'''select count(*) from zayavka where prev_status='offer' and vacancy_id={vac_id}''')
            self.res_table.setItem(3, 2, QTableWidgetItem(str(cur.fetchall()[0][0])))

class Sobes_win(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Собеседования')
        self.setGeometry(200, 200, 750, 350)
        #загрузка собеседований из БД
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'''select surname, candidate.name, vacancy.name, sobes_datetime from 
                                zayavka inner join candidate on zayavka.candidate_id=candidate.id
                                inner join vacancy on zayavka.vacancy_id=vacancy.id
                                where not sobes_datetime is NULL and sobes_datetime>datetime('now')''')
            res = cur.fetchall()
            print(res)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setRowCount(len(res))
        self.table.setColumnWidth(0, 400)
        layout.addWidget(self.table)
        for i in range(len(res)):
            self.table.setItem(i, 0, QTableWidgetItem(' '.join(res[i])))




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

        button_sobes = QAction('Показать собеседования', self)
        button_sobes.triggered.connect(self.sobes_win)

        toolbar = QToolBar('Статистика')
        toolbar.addAction(button_statistic)
        toolbar.addAction(button_sobes)
        toolbar.addAction(button_settings)

        self.addToolBar(toolbar)

    def statistic_win(self):
        self.stat = Statistic_win(self)
        self.stat.show()

    def settings_win(self):
        pass

    def sobes_win(self):
        dlg = Sobes_win(self)
        dlg.exec()
