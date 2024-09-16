import sqlite3


with sqlite3.connect('database.db') as con:
    cur = con.cursor()
    cur.execute("""create table if not exists zametka(
                    id integer primary key autoincrement, 
                    zametka_text text,
                    candidat_id int,
                    foreign key (candidat_id) references candidat(id)
                    )""")

    sample_resume = None
    candidats = [('Чип', 'Бурундук', 19, 'Фитнес-тренер', sample_resume, 1, 'tel'),
                 ('Дейл', 'Бурундук', 18, 'Фитнес-тренер', sample_resume, 1, 'tel'),
                 ('Гаечка', 'Мышь', 18, 'Фитнес-тренер', sample_resume, 1, 'sobes'),
                 ('Рокфор', 'Мышь', 38, 'Фитнес-тренер', sample_resume, 1, 'offer')
                ]

    for can in candidats:
        cur.execute(
            """INSERT INTO candidat(name, surname, age, job, doc, vacancy_id, status) VALUES (?, ?, ?, ?, ?, ?, ?)""", can)

    zametki = [('знает команды гулять, кушать', 6),
               ('ему можно платить едой', 6),
               ('забавный, будет поднимать нам настроение', 1),
               ('ответственная', 2),
               ('ох уж эти утки', 8)
    ]

    for zam in zametki:
        cur.execute("""INSERT INTO zametka(zametka_text, candidat_id) VALUES (?, ?)""", zam)