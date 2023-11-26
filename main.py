import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QRadioButton, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from Vacancy import Vacancy
import sqlite3 as sq


class NewVacancyDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Новая вакансия')

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel('Новая вакансия'))

        #название
        name_label_lineedit = QHBoxLayout()
        self.name_le = QLineEdit()
        name_label_lineedit.addWidget(QLabel('Название:'))
        name_label_lineedit.addWidget(self.name_le)
        self.main_layout.addLayout(name_label_lineedit)

        #предполагаемая дата закрытия
        enddate_label_lineedit = QHBoxLayout()
        self.enddate_le = QLineEdit()
        enddate_label_lineedit.addWidget(QLabel('Предполагаемая дата закрытия в формате год-месяц-день:'))
        enddate_label_lineedit.addWidget(self.enddate_le)
        self.main_layout.addLayout(enddate_label_lineedit)

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

    def create(self):
        name, enddate = self.name_le.text(), self.enddate_le.text()
        if name != '' and self.chech_date(enddate): #корректность введенных данных
            print(name, enddate)
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
            cur.execute('''insert into vacancy(name, end_date, status) values(?, ?, ?)''', (name, enddate, 'open'))


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
        vacancy_lst = [Vacancy(*vac, self) for vac in vacancy_lst]
        self.vacancies.setRowCount(len(vacancy_lst))

        # загрузка вакансий в таблицу self.vacancies
        for i, v in enumerate(vacancy_lst):
            self.vacancies.setCellWidget(i, 0, v.menu_widget)
            self.vacancies.setRowHeight(i, 80)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
