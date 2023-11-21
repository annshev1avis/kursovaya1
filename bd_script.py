import sqlite3

with sqlite3.connect('database.db') as con:
    cur = con.cursor()
    cur.execute("""create table if not exists vacancy(
                    id integer primary key autoincrement, 
                    name text,
                    end_date text,
                    status text
                    )""")

    cur.execute("""create table if not exists candidat(
                    id integer primary key,
                    name text,
                    surname text,
                    age integer,
                    job text,
                    doc blob,
                    vacancy_id integer,
                    status text,
                    foreign key (vacancy_id) references vacancy(id)
                    )""")


with open('C:/Users/Anna/Downloads/sample_resume.pdf', 'rb') as file:
    sample_resume = file.read()

    vacancies = [('Фитнес-тренер', '2023-12-01', 'open'),
                 ('Администратор', '2023-12-25', 'open'),
                 ('Бухгалтер', '2023-12-12', 'open'),
                 ('Уборщик', '2023-12-05', 'open'),
                 ('Программист на pyqt', '2023-09-01', 'close')]

    for vac in vacancies:
        cur.execute("""INSERT INTO vacancy(name, end_date, status) VALUES (?, ?, ?)""", vac)

    candidats = [('Микки', 'Маус', 20, 'Фитнес-тренер', sample_resume, 1, 'resume'),
                 ('Минни', 'Маус', 20, 'Организатор мероприятий', sample_resume, 2, 'resume'),
                 ('Винни', 'Пух', 30, 'Фитнес-тренер', sample_resume, 1, 'resume'),
                 ('Гуфи', 'Старший', 40, 'Бухгалтер', sample_resume, 3, 'resume'),
                 ('Гуфи', 'Младший', 15, 'Фитнес-тренер по йоге', sample_resume, 1, 'resume'),
                 ('Плуто', 'песик', 15, 'является собакой', sample_resume, 4, 'resume'),
                 ('Скрудж', 'МакДак', 50, 'Миллионер', sample_resume, 3, 'resume'),
                 ('Дональд', 'Дак', 23, 'Администратор', sample_resume, 2, 'resume')]

    for can in candidats:
        cur.execute("""INSERT INTO candidat(name, surname, age, job, doc, vacancy_id, status) VALUES (?, ?, ?, ?, ?, ?, ?)""", can)
