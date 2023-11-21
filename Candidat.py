from PyQt6.QtWidgets import QApplication, QRadioButton, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout


class Candidate_menu_widget(QWidget):
    def __init__(self, name, surname, age, job, main_window=None):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.addWidget(QLabel(name+surname))
        layout.addWidget(QLabel(job))
        layout.addWidget(QLabel(age))
        self.setLayout(layout)
        self.mouseReleaseEvent = self.open_vacancy

    def open_vacancy(self, event):
        print(self.main_window)

class Candidate:
    def __init__(self, name, surname, age, job, doc):
        self.name = name
        self.surname = surname
        self.age = age
        self.job = job
        self.doc = doc

        self.menu_widget = Candidate_menu_widget(self.name, self.surname, self.age, self.job)
