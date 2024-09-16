import sqlite3

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
                    id integer primary key autoincrement,
                    foreign key(candidate_id) references candidate(id),
                    foreign key(vacancy_id) references vacancy(id))""")

    cur.execute("""create table if not exists zametka(
                id integer primary key autoincrement,
                text text,
                zayavka_id integer,
                foreign key(zayavka_id) references zayavka(id)
                )""")

    sample_resume = None
    vacancies = [('Фитнес-тренер', '2023-12-01', 'open', 90000, 'полная занятость', 'Москва, Текстильщики'),
                 ('Администратор', '2023-12-25', 'open', 70000, '4 дня в неделю', 'Москва, Текстильщики'),
                 ('Бухгалтер', '2023-12-12', 'open', 90000, 'полная занятость', 'Москва, Пролетарская'),
                 ('Уборщик', '2023-12-05', 'open', 53000, 'полная занятость', 'Москва, Текстильщики'),
                 ('Программист на pyqt', '2023-09-01', 'close', 120000, 'удаленка', '---')]

    for vac in vacancies:
        cur.execute("""INSERT INTO vacancy(name, end_date, status, salary, graphic, location) VALUES (?, ?, ?, ?, ?, ?)""", vac)

    candidats = [('Микки', 'Маус', 20, sample_resume, 'sample_mail@mail.ru', '+123'),
                 ('Минни', 'Маус', 20, sample_resume, 'sample_mail@mail.ru', '+123'),
                 ('Винни', 'Пух', 30, sample_resume, 'sample_mail@mail.ru', '+123'),
                 ('Гуфи', 'Старший', 40, sample_resume, 'sample_mail@mail.ru', '+123'),
                 ('Гуфи', 'Младший', 15, sample_resume, 'sample_mail@mail.ru', '+123'),
                 ('Плуто', 'песик', 15, sample_resume, 'sample_mail@mail.ru', '+123'),
                 ('Скрудж', 'МакДак', 50, sample_resume, 'sample_mail@mail.ru', '+123'),
                 ('Дональд', 'Дак', 23, sample_resume, 'sample_mail@mail.ru', '+123')]

    for can in candidats:
        cur.execute("""INSERT INTO candidate(name, surname, age, doc, email, tel) VALUES (?, ?, ?, ?, ?, ?)""", can)
