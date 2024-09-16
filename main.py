import sqlite3
import sys
from PyQt6.QtWidgets import QFileDialog, QApplication, QTableWidgetItem, QRadioButton, QMainWindow, QToolBar, QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QHBoxLayout
from Vacancy import Vacancy
import sqlite3 as sq
from PyQt6.QtGui import QAction
from Authorithation import Authorithation

def init_db():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("""create table if not exists vacancy(
                        id integer primary key autoincrement, 
                        name text,
                        end_date text,
                        status text default 'open',
                        salary int,
                        graphic text,
                        location text
                        )""")

        cur.execute("""create table if not exists candidate(
                        id integer primary key autoincrement,
                        surname text,
                        name text,
                        otchestvo text,
                        password text,
                        age integer,
                        doc blob,
                        email text,
                        tel text
                        )""")

        cur.execute("""create table if not exists zayavka(
                        candidate_id integer,
                        vacancy_id integer,
                        watched integer default 0,
                        status text default 'resume',
                        prev_status text,
                        id integer primary key autoincrement,
                        sobes_datetime text,
                        foreign key(candidate_id) references candidate(id),
                        foreign key(vacancy_id) references vacancy(id))""")

        cur.execute("""create table if not exists zametka(
                    id integer primary key autoincrement,
                    text text,
                    zayavka_id integer,
                    foreign key(zayavka_id) references zayavka(id)
                    )""")

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    auth = Authorithation()
    auth.show()
    sys.exit(app.exec())
