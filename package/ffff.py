import sqlite3

db = sqlite3.connect('server.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
    login TEXT,
    pass TEXT,
    cookie TEXT
)""")

db.commit()

user_login = input('l')
user_passwd = input('p')
cook = input()

sql.execute('SELECT login FROM users')
if sql.fetchone() is None:
    sql.execute(f'INSERT INTO users VALUES (?,?,?)', (user_login, user_passwd,cook))
    db.commit()
    print('+')
else:
    print('1')
    for v in sql.execute('SELECT * FROM users'):
        print(v)