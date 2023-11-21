from PyQt6.QtWidgets import QApplication, QRadioButton, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout

class Candidate_menu_widget(QWidget):
    def __init__(self, name, surname, age, main_window=None):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.addWidget(QLabel(name+surname))
        layout.addWidget(QLabel(age))
        self.setLayout(layout)
        self.mouseReleaseEvent = self.open_vacancy

    def open_vacancy(self, event):
        print(self.main_window)
        v = Vacancy_window_part()
        self.main_window.main_layout.addWidget(v)

class Candidate:
    def __init__(self, name, surname, age, job, doc):
        self.name = name
        self.surname = surname
        self.age = age
        self.job = job

        self.menu_widget = Candidate_menu_widget(self.name, self.surname, self.age)


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


#правая часть окна
class Vacancy_window_part(QWidget):
    def __init__(self):

        super().__init__()

        #верхняя полоска с статусами
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

        #главный layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(statuses)
        self.main_layout.addLayout(candidates_part)
        self.setLayout(self.main_layout)

    #загружает в Vacancy_window_part вакансии со статусом рассмотрение_резюме
    def resumes(self):
        ann = Candidate('Ann', 'Sokolnikova', '18', 'разраб', 'doc')
        katy = Candidate('Katy', 'Sokolnikova', '18', 'разраб', 'doc')
        angi = Candidate('Angi', 'Sokolnikova', '18', 'разраб', 'doc')
        candidates = [ann, katy, angi]
        print('+')
        self.candidates.setRowCount(len(candidates))
        for i, c in enumerate(candidates):
            print(i)
            self.candidates.setCellWidget(i, 0, c.menu_widget)


class Vacancy:
    def __init__(self, name, end_date, status, parent):
        self.name = name
        self.end_date = end_date
        self.status = status

        self.menu_widget = Vacancy_menu_widget(name, end_date, parent)


