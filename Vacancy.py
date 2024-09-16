import sqlite3

from PyQt6.QtWidgets import QFileDialog, QMenu, QComboBox, QSpacerItem, QSizePolicy, QRadioButton, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from Candidat import Candidate
import sqlite3 as sq

class Update_vacancy_dialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        print('==')
        self.parent = parent
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        l_name = QHBoxLayout()
        l_name.addWidget(QLabel('Название:'))
        self.name_le = QLineEdit()
        l_name.addWidget(self.name_le)
        main_layout.addLayout(l_name)

        l_enddate = QHBoxLayout()
        l_enddate.addWidget(QLabel('Дата закрытия yyyy-mm-dd:'))
        self.enddate_le = QLineEdit()
        l_enddate.addWidget(self.enddate_le)
        main_layout.addLayout(l_enddate)

        l_salary = QHBoxLayout()
        l_salary.addWidget(QLabel('Зарплата:'))
        self.salary_le = QLineEdit()
        l_salary.addWidget(self.salary_le)
        main_layout.addLayout(l_salary)

        l_graphic = QHBoxLayout()
        l_graphic.addWidget(QLabel('График:'))
        self.graphic_le = QLineEdit()
        l_graphic.addWidget(self.graphic_le)
        main_layout.addLayout(l_graphic)

        l_location = QHBoxLayout()
        l_location.addWidget(QLabel('Локация:'))
        self.location_le = QLineEdit()
        l_location.addWidget(self.location_le)
        main_layout.addLayout(l_location)

        ok_but = QPushButton('Сохранить')
        ok_but.clicked.connect(self.save_changes)
        main_layout.addWidget(ok_but)

        self.load_data()


    def load_data(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print(f'''select name, end_date, salary, graphic, location from vacancy where id={self.parent.vacancy_parent.id}''')
            cur.execute(f'''select name, end_date, salary, graphic, location from vacancy where id={self.parent.vacancy_parent.id}''')
            print('==')
            name, end_date, salary, graphic, location = cur.fetchall()[0]
            print('33')
        self.name_le.setText(name)
        self.enddate_le.setText(end_date)
        self.salary_le.setText(str(salary))
        self.graphic_le.setText(graphic)
        self.location_le.setText(location)

    def save_changes(self):
        name, end_date, salary, graphic, location = self.name_le.text(), self.enddate_le.text(), self.salary_le.text(), \
            self.graphic_le.text(), self.location_le.text()

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'''update vacancy set name='{name}', end_date='{end_date}', salary={salary}, 
            graphic='{graphic}', location='{location}' where id={self.parent.vacancy_parent.id}''')
        self.close()

class New_candidate_dialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(QLabel('Новый кандидат'))

        # фамилия
        self.surname_lineedit = QLineEdit()
        surname = QHBoxLayout()
        surname.addWidget(QLabel('Фамилия:'))
        surname.addWidget(self.surname_lineedit)
        main_layout.addLayout(surname)

        #имя
        self.name_lineedit = QLineEdit()
        name = QHBoxLayout()
        name.addWidget(QLabel('Имя:'))
        name.addWidget(self.name_lineedit)
        main_layout.addLayout(name)

        #отчество
        self.otchestvo_lineedit = QLineEdit()
        otchestvo = QHBoxLayout()
        otchestvo.addWidget(QLabel('Отчество:'))
        otchestvo.addWidget(self.otchestvo_lineedit)
        main_layout.addLayout(otchestvo)

        #возраст
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

        #телефон
        self.tel_lineedit = QLineEdit()
        tel = QHBoxLayout()
        tel.addWidget(QLabel('Номер телефона:'))
        tel.addWidget(self.tel_lineedit)
        main_layout.addLayout(tel)

        #загрузить pdf файл
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
            print(fileNames)
        file_path = fileNames[0]
        with open(file_path) as file:
            print(0)
            self.doc = file.read()
            print(0)

    def create_candidate(self):
        doc = getattr(self, 'doc', None)
        name, surname, otchestvo, age, email, tel = self.name_lineedit.text(), self.surname_lineedit.text(), \
            self.otchestvo_lineedit.text(), self.age_lineedit.text(), self.email_lineedit.text(), \
            self.tel_lineedit.text()
        try:
            age = int(age)
        except:
            msgdlg = QDialog(self)
            layout = QVBoxLayout()
            layout.addWidget(QLabel('Некорректные входные данные'))
            msgdlg.setLayout(layout)
            msgdlg.exec()
            return

        #проверяет наличие кандидата в базе
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f'''select * from candidate where surname='{surname}' and name='{name}' and otchestvo='{otchestvo}'
                            and age={age} and email='{email}' ''')
            res = cur.fetchall()

        if len(res) == 0: #если такого кандидата нет
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(f'''insert into candidate (surname, name, otchestvo, age, doc, email, tel) 
                            values(?, ?, ?, ?, ?, ?, ?)''', (surname, name, otchestvo, age, doc, email, tel))

                cur.execute(
                    f'''select * from candidate where surname='{surname}' and name='{name}' and otchestvo='{otchestvo}'
                                            and age={age} and email='{email}' ''')
                res = cur.fetchall()

        cand_id = res[0][0]
        print(cand_id)
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print(self.parent, self.parent.vacancy_parent.id)
            cur.execute(f'''insert into zayavka (vacancy_id, candidate_id) 
                        values(?, ?)''', (self.parent.vacancy_parent.id, cand_id))

        self.close()


#правая часть окна
class Vacancy_window_part(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.vacancy_parent = parent

        # верхняя полоска с статусами
        statuses = QHBoxLayout()
        self.resumes_button = QPushButton('Резюме')
        self.resumes_button.clicked.connect(self.resume)
        self.telephone_button = QPushButton('Интервью по телефону')
        self.telephone_button.clicked.connect(self.tel_interview)
        self.sobes_button = QPushButton('Собеседовние')
        self.sobes_button.clicked.connect(self.sobes)
        self.offer_button = QPushButton('Оффер')
        self.offer_button.clicked.connect(self.offer)
        self.otkaz_button = QPushButton('Отказ')
        self.otkaz_button.clicked.connect(self.otkaz)

        statuses.addWidget(self.resumes_button)
        statuses.addWidget(self.telephone_button)
        statuses.addWidget(self.sobes_button)
        statuses.addWidget(self.offer_button)
        statuses.addWidget(self.otkaz_button)


        self.candidates_part = QHBoxLayout()
        # комбобокс сортировки и список кандидатов и кнопка новый кандидат
        candidates_newcandidatebutton = QVBoxLayout()
        self.sorting_combobox = QComboBox()
        self.sorting_combobox.addItem('Сначала просмотренные')
        self.sorting_combobox.addItem('Сначала непросмотренные')
        self.sorting_combobox.addItem('По алфавиту')
        self.sorting_combobox.activated.connect(self.sort_update)
        candidates_newcandidatebutton.addWidget(self.sorting_combobox)
        self.candidates = QTableWidget()
        self.candidates.setColumnCount(1)
        self.candidates.setMaximumWidth(300)
        self.candidates.verticalHeader().setVisible(False)
        self.candidates.horizontalHeader().setVisible(False)
        self.candidates.horizontalHeader().setStretchLastSection(True)
        self.new_candidate_button = QPushButton('Новый кандидат')
        self.new_candidate_button.clicked.connect(self.create_new_candidate)
        candidates_newcandidatebutton.addWidget(self.candidates)
        candidates_newcandidatebutton.addWidget(self.new_candidate_button)
        self.candidates_part.addLayout(candidates_newcandidatebutton)

        #большой виджет
        self.candidates_part.addWidget(QLabel(''))

        # главный layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(statuses)
        self.main_layout.addLayout(self.candidates_part)

        self.setLayout(self.main_layout)
        self.load_candidates('resume')

    """3 метода с сортировкой: принимает - list; возвращает - list
    используется исключительно в self.load_candidates"""
    @staticmethod
    def unwatched_first_sorting(can_lst):
        """can_lst - список объектов типа Candidate"""
        for i in range(len(can_lst) - 1):
            for j in range(len(can_lst) - i - 1):
                if can_lst[j].watched > can_lst[j+1].watched:
                    can_lst[j], can_lst[j+1] = can_lst[j+1], can_lst[j]
        return can_lst

    @staticmethod
    def watched_first_sorting(can_lst):
        """can_lst - список объектов типа Candidate"""
        for i in range(len(can_lst) - 1):
            for j in range(len(can_lst) - i - 1):
                if can_lst[j].watched < can_lst[j+1].watched:
                    can_lst[j], can_lst[j+1] = can_lst[j+1], can_lst[j]
        return can_lst

    @staticmethod
    def abc_sorting(can_lst):
        """can_lst - список объектов типа Candidate"""
        for i in range(len(can_lst) - 1):
            for j in range(len(can_lst) - i - 1):
                print(can_lst[j].surname[0].lower(), can_lst[j+1].surname[0].lower())
                if can_lst[j].surname[0].lower() > can_lst[j+1].surname[0].lower():
                    can_lst[j], can_lst[j+1] = can_lst[j+1], can_lst[j]
        return can_lst

    def sort_update(self):
        """при изменении self.sorting_combobox вызывает load_candidates"""
        try:
            status = self.candidates.cellWidget(0, 0).candidate_parent.status
            print(status)
        except:
            return
        sorting = self.sorting_combobox.currentText()
        if sorting == 'Сначала непросмотренные':
            self.load_candidates(status, 'unwatched_first_sorting')
            pass
        elif sorting == 'Сначала просмотренные':
            self.load_candidates(status, 'watched_first_sorting')
            pass
        elif sorting == 'По алфавиту':
            self.load_candidates(status, 'abc_sorting')
            pass

    def create_new_candidate(self):
        dlg = New_candidate_dialog(self)
        dlg.exec()

    def insert_big_widget(self, bigwidget):
        """вставляет любой виджет на место для big_widget"""
        self.candidates_part.itemAt(1).widget().deleteLater()
        self.candidates_part.removeWidget(self.candidates_part.itemAt(1).widget())
        self.candidates_part.addWidget(bigwidget)

    def resume(self):
        # загружает в Vacancy_window_part кандидатов со статусом рассмотрение_резюме
        self.insert_big_widget(QLabel(''))
        self.load_candidates(status='resume')

    def tel_interview(self):
        self.insert_big_widget(QLabel(''))
        self.load_candidates(status='tel')

    def sobes(self):
        self.insert_big_widget(QLabel(''))
        self.load_candidates(status='sobes')

    def offer(self):
        self.insert_big_widget(QLabel(''))
        self.load_candidates(status='offer')

    def otkaz(self):
        self.insert_big_widget(QLabel(''))
        self.load_candidates(status='otkaz')

    def load_candidates(self, status, sorting='unwatched_first_sorting'):
        """загружает кандидатов в таблицу candidates и очищает big_widget
        - ОБНОВЛЯЕТ SELF.CANDIDATES_PART"""
        sorting = getattr(self, sorting)

        with sq.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"select candidate_id, watched, status, id from zayavka where status='{status}' "
                        f"and vacancy_id={self.vacancy_parent.id}")
            candidates_lst = cur.fetchall()

        candidates_lst = [Candidate(can[0], can[1], can[2], can[3], self.vacancy_parent) for can in candidates_lst]
        candidates_lst = sorting(candidates_lst)

        self.candidates.setRowCount(len(candidates_lst))
        for i, c in enumerate(candidates_lst):
            self.candidates.setCellWidget(i, 0, c.menu_widget)
            self.candidates.setRowHeight(i, 90)


#маленькая кнопка в панели слева
class Vacancy_menu_widget(QWidget):
    def __init__(self, name, end_date, parent):
        super().__init__()
        #ссылка на главное окно, чтобы была возможность его изменять
        self.vacancy_parent = parent

        #внешний вид
        layout = QVBoxLayout()
        layout.addWidget(QLabel(name))
        layout.addWidget(QLabel(end_date))

        self.setLayout(layout)

    def mouseReleaseEvent(self, event):
        #возможно надо подредактировать, но пусть так пока работает
        self.vacancy_parent.window_part = self.vacancy_parent.create_window_part()
        if self.vacancy_parent.main_window.main_layout.count() > 1:
            self.vacancy_parent.main_window.main_layout.itemAt(1).widget().deleteLater()
            self.vacancy_parent.main_window.main_layout.removeWidget(self.vacancy_parent.main_window.main_layout.itemAt(1).widget())
        self.vacancy_parent.main_window.main_layout.addWidget(self.vacancy_parent.window_part)

    def contextMenuEvent(self, event):
        self.context_menu = QMenu(self)

        update_act = self.context_menu.addAction('Изменить')
        update_act.triggered.connect(self.update_vacancy)

        if self.vacancy_parent.status == 'open':
            change_status_act = self.context_menu.addAction('Закрыть')
            change_status_act.triggered.connect(self.close_vacancy)
        elif self.vacancy_parent.status == 'close':
            change_status_act = self.context_menu.addAction('Открыть')
            change_status_act.triggered.connect(self.open_vacancy)

        delete_act = self.context_menu.addAction('Удалить')
        delete_act.triggered.connect(self.delete_vacancy)
        self.context_menu.exec(event.globalPos())

    def update_vacancy(self):
        dlg = Update_vacancy_dialog(self)
        dlg.exec()

    def close_vacancy(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""update vacancy set status='close' where id={self.vacancy_parent.id}""")

    def open_vacancy(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""update vacancy set status='open' where id={self.vacancy_parent.id}""")

    def delete_vacancy(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(f"""delete from vacancy where id={self.vacancy_parent.id}""")

class Vacancy:
    """представляет собой вакансию с названием, дедлайном, статусом и ссылкой на главное окно
    помимо основных атрибутов (name, end_date, status)
    хранит виджеты по смыслу связанные с данной вакансией

    -menu_widget - виджет который отображается в левой части главного окна
    -window_part - большой виджет, который отображается в правой части окна и предоставляет весь интерфейс для работы с вакансией"""
    def __init__(self, id, name, end_date, status, main_window):
        self.id = id
        self.name = name
        self.end_date = end_date
        self.status = status
        self.main_window = main_window

        self.menu_widget = Vacancy_menu_widget(name, end_date, self)

    def create_window_part(self):
        """создает часть окна и возвращает её"""
        self.window_part = Vacancy_window_part(self) #если атрибута нет, то он создается; если есть, то перезаписывается
        return self.window_part
