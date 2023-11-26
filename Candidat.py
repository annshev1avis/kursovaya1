from PyQt6.QtWidgets import QComboBox, QMenu, QApplication, QRadioButton, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
import PyQt6.QtCore as QtCore
import sqlite3

class NewZametkaDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Новая заметка')
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Введите текст заметки:'))
        self.zametka_lineedit = QLineEdit()
        layout.addWidget(self.zametka_lineedit)
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.ok)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def ok(self):
        candidate_id, text = self.parent.candidate_parent.id, self.zametka_lineedit.text()
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'''insert into zametka(zametka_text, candidat_id) values(?, ?)''', (text, candidate_id))
        self.close()

class Zametka_widget(QWidget):
    def __init__(self, id, text):
        super().__init__()
        self.zametka_id = id
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel(str(text)))

    def contextMenuEvent(self, event):
        self.context_menu = QMenu(self)
        delete_action = self.context_menu.addAction('Удалить')
        delete_action.triggered.connect(self.delete_zametka)
        self.context_menu.exec(event.globalPos())

    def delete_zametka(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""delete from zametka where id={self.zametka_id}""")


class Candidat_big_widget(QWidget):
    etaps = ('resume', 'tel', 'sobes', 'offer', 'otkaz')
    def __init__(self, name, surname, age, job, doc, candidate_parent):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.candidate_parent = candidate_parent

        #основная информация о кандидате
        self.fio_label = QLabel(name + ' ' + surname)
        self.job_label = QLabel(job)
        self.age_label = QLabel(str(age))
        self.doc = doc
        self.main_layout.addWidget(self.fio_label)
        self.main_layout.addWidget(self.job_label)
        self.main_layout.addWidget(self.age_label)
        #self.main_layout.addStretch()

        #заметки
        zametki_label_button = QHBoxLayout()
        zametki_label_button.addWidget(QLabel('Заметки'))
        self.new_zametka_button = QPushButton('Новая заметка')
        self.new_zametka_button.clicked.connect(self.new_zametka)
        zametki_label_button.addWidget(self.new_zametka_button)
        self.main_layout.addLayout(zametki_label_button)

        self.zametki_table = QTableWidget()
        self.zametki_table.setColumnCount(1)
        self.zametki_table.verticalHeader().setVisible(False)
        self.zametki_table.horizontalHeader().setVisible(False)
        self.zametki_table.horizontalHeader().setStretchLastSection(True)
        self.main_layout.addWidget(self.zametki_table)
        self.load_zametki() #загрузка заметок

        #сменить этап
        otkaz_next_buttons = QHBoxLayout()
        if self.candidate_parent.status == 'otkaz':
            self.return_button = QPushButton('Вернуть в статус Резюме')
            self.return_button.clicked.connect(self.return_to_resume)
            otkaz_next_buttons.addWidget(self.return_button)
        elif self.candidate_parent.status == 'offer':
            self.otkaz_button = QPushButton('Отказ')
            self.otkaz_button.clicked.connect(self.make_otkaz_status)
            otkaz_next_buttons.addWidget(self.otkaz_button)
            if self.candidate_parent.status != 'offer':
                self.next_etap_button = QPushButton('На следующий этап')
                self.next_etap_button.clicked.connect(self.next_etap)
                otkaz_next_buttons.addWidget(self.next_etap_button)
        self.main_layout.addLayout(otkaz_next_buttons)


        #перейти к кандидату
        self.go_to_candidat = QPushButton('Перейти к кандидату')
        self.main_layout.addWidget(self.go_to_candidat)

        self.setLayout(self.main_layout)
        print('bigwid created')

    def make_otkaz_status(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""update candidat set status='otkaz' where id={self.candidate_parent.id}""")

    def next_etap(self):
        cur_etap_index = self.etaps.index(self.candidate_parent.status)
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""update candidat set status='{self.etaps[cur_etap_index+1]}' where id={self.candidate_parent.id}""")

    def return_to_resume(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""update candidat set status='resume' where id={self.candidate_parent.id}""")

    def load_zametki(self):
        print('=')
        print(self.candidate_parent.id)
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""select id, zametka_text from zametka where candidat_id={self.candidate_parent.id}""")
            zam_lst = cur.fetchall()

        print(zam_lst)

        self.zametki_table.setRowCount(len(zam_lst))
        for i, zam in enumerate(zam_lst):
            print(zam[0])
            self.zametki_table.setCellWidget(i, 0, Zametka_widget(zam[0], zam[1]))

    def new_zametka(self):
        dlg = NewZametkaDialog(self)
        dlg.exec()
        self.load_zametki()


class Candidate_menu_widget(QWidget):
    def __init__(self, name, surname, age, job, candidate_parent):
        super().__init__()
        self.candidate_parent = candidate_parent

        layout = QVBoxLayout()
        layout.addWidget(QLabel(surname+name))
        layout.addWidget(QLabel(job))
        layout.addWidget(QLabel(str(age)))
        watched = 'просмотрено' if self.candidate_parent.watched == 1 else 'непросмотрено'
        self.watched_label = QLabel(watched)
        layout.addWidget(self.watched_label)

        self.setLayout(layout)

    def mouseReleaseEvent(self, event):
        if self.candidate_parent.watched == 0:
            self.candidate_parent.watched = 1
            self.watched_label.setText('просмотрено')
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(f'update candidat set watched=1 where id={self.candidate_parent.id}')
        big_widget = self.candidate_parent.create_big_widget()
        self.candidate_parent.vacancy.window_part.insert_big_widget(big_widget)

    def contextMenuEvent(self, event):
        """срабатывает при пкм по self, предоставляет функционал для удаления пользователя"""
        self.context_menu = QMenu(self)
        delete_act = self.context_menu.addAction("Удалить")
        delete_act.triggered.connect(self.delete_candidate)
        self.context_menu.exec(event.globalPos())


    def delete_candidate(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'delete from candidat where id={self.candidate_parent.id}')

class Candidate:
    def __init__(self, id, name, surname, age, job, doc, status, watched, vacancy):
        self.id = id   #id кандидата в бд, для взаимодействия с бд
        self.name = name
        self.surname = surname
        self.age = age
        self.job = job
        self.doc = doc
        self.status = status
        self.watched = watched
        self.vacancy = vacancy #вакансия, в которой создается этот экземпляр Candidate (для того, чтобы менять Vacancy_window_part)

        self.menu_widget = Candidate_menu_widget(self.name, self.surname, self.age, self.job, self)
        print('can created')
    def create_big_widget(self):
        self.big_widget = Candidat_big_widget(self.name, self.surname, self.age, self.job, self.doc, self)
        return self.big_widget
