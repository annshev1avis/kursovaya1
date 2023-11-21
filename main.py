import sys
from PyQt6.QtWidgets import QApplication, QRadioButton, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6.uic import loadUi
#from MainWindow import MainWindow

class Candidat_header(QWidget):
    def __init__(self, fio, age):
        super().__init__()
        loadUi("uis/Candidat_header.ui", self)
        self.fio_label.setText(fio)
        self.age_label.setText(str(age) + ' лет')


class Candidate(QWidget):
    def __init__(self, fio, info, file):
        super().__init__()
        loadUi("uis/Candidat.ui", self)
        self.fio_label.setText(fio)
        self.info_label.setText(info)
        self.document_label.setText(file)
        self.info_label.adjustSize()


class CV_viewer(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout()

        #колонка с именами кандидатов
        self.candidats_column = QVBoxLayout()
        self.candidats_column.addWidget(Candidat_header('Аски', 29))
        self.candidats_column.addWidget(Candidat_header('Ящерка', 12))

        #большое окно с выбранным кандидатом
        self.showing_candidat = Candidate('Аски', 'работает в сбербанке', 'резюме2.0')

        self.main_layout.addLayout(self.candidats_column)
        self.main_layout.addWidget(self.showing_candidat)
        self.setLayout(self.main_layout)

class Vacancy:
    def __init__(self, name):
        self.name = name
        self.radio_button = QRadioButton(name)

        self.big_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Большое окно вакансии'))
        main_layout.addWidget(QLabel('Здесь будут кандидаты'))
        main_layout.addWidget(QLabel('Здесь будет большое окно для выбранного кандидата'))
        self.big_widget.setLayout(main_layout)



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #loadUi("uis/MainWindow.ui", self)"""

        #ВАКАНСИИ
        designer = Vacancy('designer')

        main_layout = QHBoxLayout()

        #КОЛОНКА ВАКАНСИИ СЛЕВА
        vacancies_column = QVBoxLayout()
        vacancies_column.addWidget(QLabel('Вакансии'))

        #вкладки открытые/архив
        open_arhiv = QHBoxLayout()
        self.open_button = QPushButton('Открытые')
        self.arhiv_button = QPushButton('Архив')
        open_arhiv.addWidget(self.open_button)
        open_arhiv.addWidget(self.arhiv_button)
        vacancies_column.addLayout(open_arhiv)

        vacancies_column.addWidget(designer.radio_button)
        """#таблица с вакансиями
        self.vacancies = QTableWidget()
        vacancies_column.addWidget(self.vacancies)
        self.vacancies.setRowCount(1)
        self.vacancies.setColumnCount(1)
        self.vacancies.setCellWidget(0, 0, QPushButton('Дизайнер'))"""

        #кнопка Новая вакансия
        self.new_vacancy_button = QPushButton('Новая вакансия')
        vacancies_column.addWidget(self.new_vacancy_button)

        #установка main_layout
        main_layout.addLayout(vacancies_column)
        main_layout.addWidget(QLabel('ЗДЕСЬ БУДЕТ КАСТОМНЫЙ ВИДЖЕТ'))
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())