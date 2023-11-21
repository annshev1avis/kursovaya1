import sys
from PyQt6.QtWidgets import QApplication, QRadioButton, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from Vacancy import Vacancy
import sqlite3 as sq


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        #выгрузка вакансий из бд в vacancy_lst (список из объектов Vacancy)
        with sq.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("select name, end_date, status from vacancy")
            vacancy_lst = cur.fetchall()
        vacancy_lst = [Vacancy(*vac, self) for vac in vacancy_lst]

        #главный layout
        self.main_layout = QHBoxLayout()

        #КОЛОНКА ВАКАНСИИ СЛЕВА
        vacancies_column = QVBoxLayout()
        vacancies_column.addWidget(QLabel('Вакансии'))

        #вкладки открытые/архив
        open_arhiv = QHBoxLayout()
        self.open_button = QPushButton('Открытые')
        self.arhiv_button = QPushButton('Закрытые')
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
        self.vacancies.setRowCount(len(vacancy_lst))
        for i, v in enumerate(vacancy_lst):
            self.vacancies.setCellWidget(i, 0, v.menu_widget)
            self.vacancies.setRowHeight(i, 80)

        #кнопка Новая вакансия
        self.new_vacancy_button = QPushButton('Новая вакансия')
        vacancies_column.addWidget(self.new_vacancy_button)

        #часть окна справа
        right_part = QVBoxLayout()
        statuses = QHBoxLayout()

        #установка main_layout
        self.main_layout.addLayout(vacancies_column)
        #self.main_layout.addWidget(QLabel('ЗДЕСЬ БУДЕТ КАСТОМНЫЙ ВИДЖЕТ'))
        self.setLayout(self.main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
