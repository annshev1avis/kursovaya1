from PyQt6.QtWidgets import QComboBox, QMessageBox, QMenu, QApplication, QRadioButton, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
import PyQt6.QtCore as QtCore
import sqlite3
import tempfile
from PyQt6.QtCore import QProcess
import os
import subprocess
from Candidate_window import Profile

class Make_sobes_dialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Собеседование')
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(QLabel('Назначить собеседование'))
        main_layout.addWidget(QLabel('Введите дату в формате YYYY-MM-DD HH:MM:SS:'))
        self.date_le = QLineEdit()
        main_layout.addWidget(self.date_le)
        self.commit_button = QPushButton('Сохранить')
        self.commit_button.clicked.connect(self.commit)
        main_layout.addWidget(self.commit_button)

    def commit(self):
        sobes_datetime = self.date_le.text()
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print(f'''update zayavka set sobes_datetime='{sobes_datetime}' where id={self.parent.candidate_parent.zayavka_id}''')
            cur.execute(f'''update zayavka set sobes_datetime='{sobes_datetime}' where id={self.parent.candidate_parent.zayavka_id}''')
        self.close()

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
        zayavka_id, text = self.parent.candidate_parent.zayavka_id, self.zametka_lineedit.text()
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'''insert into zametka(text, zayavka_id) values(?, ?)''', (text, zayavka_id))
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

    def __init__(self, candidate_parent):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.candidate_parent = candidate_parent

        #основная информация о кандидате
        #добавить отчество
        self.fio_label = QLabel(candidate_parent.surname + ' ' + candidate_parent.name + ' ')
        self.age_label = QLabel(str(candidate_parent.age))
        self.doc = candidate_parent.doc
        self.main_layout.addWidget(self.fio_label)
        self.main_layout.addWidget(self.age_label)
        self.main_layout.addWidget(QLabel(candidate_parent.email))
        self.main_layout.addWidget(QLabel(candidate_parent.tel))
        #self.main_layout.addStretch()

        self.resume_button = QPushButton('Открыть резюме в PDF')
        self.resume_button.clicked.connect(self.open_resume)
        self.main_layout.addWidget(self.resume_button)
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
        print('<', self.candidate_parent.status, '>')
        if self.candidate_parent.status == 'otkaz':
            self.return_button = QPushButton('Вернуть в статус Резюме')
            self.return_button.clicked.connect(self.return_to_resume)
            otkaz_next_buttons.addWidget(self.return_button)
        elif self.candidate_parent.status == 'offer':
            self.otkaz_button = QPushButton('Отказ')
            self.otkaz_button.clicked.connect(self.make_otkaz_status)
            otkaz_next_buttons.addWidget(self.otkaz_button)
        elif self.candidate_parent.status != 'offer':
            self.otkaz_button = QPushButton('Отказ')
            self.otkaz_button.clicked.connect(self.make_otkaz_status)
            otkaz_next_buttons.addWidget(self.otkaz_button)
            self.next_etap_button = QPushButton('На следующий этап')
            self.next_etap_button.clicked.connect(self.next_etap)
            otkaz_next_buttons.addWidget(self.next_etap_button)
        self.main_layout.addLayout(otkaz_next_buttons)

        """как оказалось ненужный функционал
        #перейти к кандидату
        self.go_to_candidat = QPushButton('Перейти к кандидату')
        self.main_layout.addWidget(self.go_to_candidat)"""

        self.setLayout(self.main_layout)
        print('bigwid created')

    def open_resume(self):
        #читается файл из бд
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""select doc from candidate where id={self.candidate_parent.id}""")
            doc = cur.fetchall()[0][0]

        if doc != None:
            #создается временный файл из байтовых данных doc
            temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
            temp_file.write(doc)
            temp_file.close()

            #файл открывается в акробате
            file_path = temp_file.name
            app_path = 'C:/Program Files/Adobe/Acrobat DC/Acrobat/Acrobat.exe'
            try:
                subprocess.Popen([app_path, file_path])
            except FileNotFoundError:
                QMessageBox.warning(self, 'Ошибка', 'Не удалось найти программу для открытия PDF.')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Нет файла')

    def make_otkaz_status(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'select status from zayavka where candidate_id={self.candidate_parent.id} '
                        f'and vacancy_id={self.candidate_parent.vacancy.id}')
            prev_status = cur.fetchall()[0][0]
            cur.execute(f"""update zayavka set status='otkaz', prev_status='{prev_status}' 
            where candidate_id={self.candidate_parent.id} and vacancy_id={self.candidate_parent.vacancy.id}""")

    def next_etap(self):
        cur_etap_index = self.etaps.index(self.candidate_parent.status)
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""update zayavka set status='{self.etaps[cur_etap_index+1]}', sobes_datetime=NULL 
            where candidate_id={self.candidate_parent.id} and vacancy_id={self.candidate_parent.vacancy.id}""")

    def return_to_resume(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""update zayavka set status='resume' where candidate_id={self.candidate_parent.id} and 
            vacancy_id={self.candidate_parent.vacancy.id}""")


    def load_zametki(self):
        print(self.candidate_parent.id)
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""select id, text from zametka where zayavka_id={self.candidate_parent.zayavka_id}""")
            zam_lst = cur.fetchall()

        self.zametki_table.setRowCount(len(zam_lst))
        for i, zam in enumerate(zam_lst):
            self.zametki_table.setCellWidget(i, 0, Zametka_widget(zam[0], zam[1]))

    def new_zametka(self):
        dlg = NewZametkaDialog(self)
        dlg.exec()
        self.load_zametki()


class Candidate_menu_widget(QWidget):
    def __init__(self, name, surname, age, candidate_parent):
        super().__init__()
        self.candidate_parent = candidate_parent

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)


        layout = QVBoxLayout()
        layout.addWidget(QLabel(surname + ' ' + name))
        layout.addWidget(QLabel(str(age)))
        watched = 'просмотрено' if self.candidate_parent.watched == 1 else 'непросмотрено'
        self.watched_label = QLabel(watched)
        layout.addWidget(self.watched_label)
        self.main_layout.addLayout(layout)
        print('mmm')

        if self.candidate_parent.status == 'sobes':
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                print(f'''select sobes_datetime from zayavka where id={self.candidate_parent.zayavka_id}''')
                cur.execute(f'''select sobes_datetime from zayavka where id={self.candidate_parent.zayavka_id}''')
                #print(cur.fetchall()[0][0])
                sobes_datetime = cur.fetchall()[0][0]
                print(sobes_datetime)
            if sobes_datetime != None:
                self.main_layout.addWidget(QLabel('Собеседование \n'+sobes_datetime))
            else:
                self.make_sobes_but = QPushButton('Назначить собеседование')
                self.make_sobes_but.clicked.connect(self.make_sobes)
                self.main_layout.addWidget(self.make_sobes_but)

    def make_sobes(self):
        msd = Make_sobes_dialog(self)
        msd.exec()

    def mouseReleaseEvent(self, event):
        if self.candidate_parent.watched == 0:
            self.candidate_parent.watched = 1
            self.watched_label.setText('просмотрено')
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(f'update zayavka set watched=1 where candidate_id={self.candidate_parent.id} and '
                            f'vacancy_id={self.candidate_parent.vacancy.id}')
        big_widget = self.candidate_parent.create_big_widget()
        self.candidate_parent.vacancy.window_part.insert_big_widget(big_widget)

    def contextMenuEvent(self, event):
        """срабатывает при пкм по self, предоставляет функционал для удаления пользователя"""
        self.context_menu = QMenu(self)
        delete_act = self.context_menu.addAction("Удалить")
        change_act = self.context_menu.addAction("Редактировать")
        delete_act.triggered.connect(self.delete_candidate)
        change_act.triggered.connect(self.change_candidate)
        self.context_menu.exec(event.globalPos())

    def delete_candidate(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'delete from zayavka where id={self.candidate_parent.zayavka_id}')

    def change_candidate(self):
        self.prof = Profile(self.candidate_parent.id)
        self.prof.show()

#теперь это заявка
class Candidate:
    def __init__(self, candidate_id, watched, status, zayavka_id, vacancy):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'''select surname, name, otchestvo, age, doc, email, tel from candidate where 
            id={candidate_id}''')
            res = cur.fetchall()[0]

        self.id = candidate_id   #id кандидата в бд, для взаимодействия с бд
        self.surname = res[0]
        self.name = res[1]
        self.otchestvo = res[2]
        self.age = res[3]
        self.doc = res[4]
        self.email = res[5]
        self.tel = res[6]
        self.watched = watched
        self.status = status
        self.zayavka_id = zayavka_id
        # вакансия, в которой создается этот экземпляр Candidate (для того, чтобы менять Vacancy_window_part)
        self.vacancy = vacancy
        print(self.__dict__)
        self.menu_widget = Candidate_menu_widget(self.name, self.surname, self.age, self)


    def create_big_widget(self):
        #self.big_widget = Candidat_big_widget(self.name, self.surname, self.otchestvo, self.age, self.email, self.tel, self.doc, self)
        self.big_widget = Candidat_big_widget(self)
        return self.big_widget