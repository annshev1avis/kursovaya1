from PyQt6.QtWidgets import QApplication, QRadioButton, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from Candidat import Candidate
import sqlite3 as sq


#правая часть окна
class Vacancy_window_part(QWidget):
    def __init__(self):
        super().__init__()

        # верхняя полоска с статусами
        statuses = QHBoxLayout()
        self.resumes_button = QPushButton('Резюме')
        self.resumes_button.clicked.connect(self.resumes)
        self.telephone_button = QPushButton('Интервью по телефону')
        self.sobes_button = QPushButton('Собеседовние')
        self.offer_button = QPushButton('Оффер')

        statuses.addWidget(self.resumes_button)
        statuses.addWidget(self.telephone_button)
        statuses.addWidget(self.sobes_button)
        statuses.addWidget(self.offer_button)

        # список кандидатов и окно кандидата
        candidates_part = QHBoxLayout()
        self.candidates = QTableWidget()
        self.candidates.setColumnCount(1)
        self.candidate_square = QLabel('окно для кандидата')
        candidates_part.addWidget(self.candidates)
        candidates_part.addWidget(self.candidate_square)

        # главный layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(statuses)
        self.main_layout.addLayout(candidates_part)
        self.setLayout(self.main_layout)

    # загружает в Vacancy_window_part вакансии со статусом рассмотрение_резюме
    def resumes(self):
        print('+')
        with sq.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("select name, surname, age, job, doc from candidat")
            candidates_lst = cur.fetchall()

        candidates_lst = [Candidate(can[0], can[1], str(can[2]), can[3], can[4]) for can in candidates_lst]

        print('+')
        self.candidates.setRowCount(len(candidates_lst))
        self.candidates.verticalHeader().setVisible(False)
        self.candidates.horizontalHeader().setVisible(False)
        self.candidates.horizontalHeader().setStretchLastSection(True)
        for i, c in enumerate(candidates_lst):
            self.candidates.setCellWidget(i, 0, c.menu_widget)
            self.candidates.setRowHeight(i, 80)


#маленькая кнопка в панели слева
class Vacancy_menu_widget(QWidget):
    def __init__(self, name, end_date, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.addWidget(QLabel(name))
        layout.addWidget(QLabel(end_date))
        self.setLayout(layout)
        self.mouseReleaseEvent = self.open_vacancy

    def open_vacancy(self, event):
        print(self.main_window)
        v = Vacancy_window_part()
        self.main_window.main_layout.addWidget(v)


class Vacancy:
    def __init__(self, name, end_date, status, parent):
        self.name = name
        self.end_date = end_date
        self.status = status

        self.menu_widget = Vacancy_menu_widget(name, end_date, parent)

