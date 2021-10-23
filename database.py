import sqlite3, datetime
from random import randint
global conn
global cursor
"""mydb = mysql.connector.connect(
  host="localhost",
  user="myusername",
  password="mypassword"
)"""
def create_table(path):
    conn = sqlite3.connect(path)
    #conn = psycopg2.connect( host="192.168.0.1", user="Mihail", password="", dbname="first_database", port="5432")
    cursor = conn.cursor()
    #cursor.execute("""DROP TABLE IF EXISTS vag_operations""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS vag_operations(
    number BIGINT,
    operation TEXT,
    time TEXT,
    track TEXT,
    park TEXT,
    client TEXT,
    time_input TEXT
    )""")
    conn.close()

"""number, operation, time, track, park, client, time_input = 1258968, "Погрузка", datetime.datetime(2020, 7, 2, 17, 22),\
                                                           "65", "Парк отстоя", "Азимут", datetime.datetime.now()"""

def read_vagon(number, path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM vag_operations WHERE number = '{number}'")
    operations = cursor.fetchall()
    #print(operations)
    vagon = []
    for i in range (len(operations)):
        operation = operations[i][1]
        dt = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(operations[i][2]))
        track = operations[i][3]
        park = operations[i][4]
        client = operations[i][5]
        dt_input = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(operations[i][6]))
        vagon.append([operation, dt, track, park, client, dt_input])
    #print(vagon)
    conn.close()
    return vagon

def read_vagon_sec(number, path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM vag_operations WHERE number = '{number}'")
    operations = cursor.fetchall()
    #print(operations)
    vagon = []
    for i in range (len(operations)):
        operation = operations[i][1]
        dt = operations[i][2]
        track = operations[i][3]
        park = operations[i][4]
        client = operations[i][5]
        vagon.append([operation, dt, track, park, client])
    #print(vagon)
    conn.close()
    return vagon

def add_note(path, number, operation, time, track, park, client, time_input):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM vag_operations WHERE number = '{number}' AND operation = '{operation}' AND"
                   f" time = '{time}' AND track = '{track}' AND park = '{park}' AND client = '{client}'")
    input_data = cursor.fetchall()
    if len(input_data) == 0:
        #print("!", input_data)
        cursor.execute(f"INSERT INTO vag_operations VALUES (?, ?, ?, ?, ?, ?, ?)", (
            number, operation, time, track, park, client, time_input))
    conn.commit()
    conn.close()

def change_note(path, number, operation, time, track, park, client, time_input, operation_0, time_0, track_0, park_0, client_0):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    #print(number, operation, time, track, park, client, time_input, operation_0, time_0, track_0, park_0, client_0)
    cursor.execute(f"SELECT * FROM vag_operations WHERE number = '{number}' AND operation = '{operation}' AND"
                   f" time = '{time}' AND track = '{track}' AND park = '{park}' AND client = '{client}'")
    input_data = cursor.fetchall()
    if len(input_data) == 0:
        cursor.execute(f"UPDATE vag_operations SET operation = '{operation}', time = '{time}', track = '{track}', "
                       f"park = '{park}', client = '{client}', time_input = '{time_input}' WHERE number = '{number}' AND "
                       f"operation = '{operation_0}' AND time = '{time_0}' AND track = '{track_0}' AND park = '{park_0}'"
                       f" AND client = '{client_0}'")
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def delete_note(path, number, operation, time, track, park, client):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM vag_operations WHERE number = '{number}' AND operation = '{operation}' AND"
                   f" time = '{time}' AND track = '{track}' AND park = '{park}' AND client = '{client}'")
    input_data = cursor.fetchall()
    if len(input_data) != 0:
        #print("!", input_data)
        cursor.execute(f"DELETE FROM vag_operations WHERE number = '{number}' AND operation = '{operation}' AND"
                       f" time = '{time}' AND track = '{track}' AND park = '{park}' AND client = '{client}'")
    conn.commit()
    conn.close()

def read_numbers(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    numbers = []
    for i in cursor.execute("SELECT number FROM vag_operations"):
        if numbers.count(i[0]) == 0:
            numbers.append(i[0])
    conn.close()
    #print(numbers)
    return numbers

def find_statistical(path, time_0, time_1):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    operations = ['Прибытие', 'Отправление', 'Погрузка', 'Выгрузка', 'Проведение ТО', 'Взвешивание', 'ВУ-36']
    clients = ['ООО «Азимут»', "Почта России", 'ООО «БТК»', 'АО «Трансмобильность»', 'АО «Глобал Транс»', 'ООО «ПЛК»',
               'ООО «ТК Союз»', 'ГУФСИН', 'ЦБРФ', 'АО «ФПК»', 'ООО «Атранс Логистика»']
    clients_op = []
    operations_op = []
    all_operations = []
    for client in range(len(clients)):
        operations_op.append([])
        for op in range (len(operations)):
            cursor.execute(f"SELECT operation FROM vag_operations WHERE time > '{time_0}' AND time < '{time_1}' "
                           f"AND operation = '{operations[op]}' AND client = '{clients[client]}'")
            operation = cursor.fetchall()
            operations_op[client].append(len(operation))
        clients_op.append(operations_op[client])
    for op in range(len(operations)):
        cursor.execute(f"SELECT operation FROM vag_operations WHERE time > '{time_0}' AND time < '{time_1}' "
                       f"AND operation = '{operations[op]}'")
        operation = cursor.fetchall()
        all_operations.append(len(operation))
    clients_op.append(all_operations)

    conn.close()
    return clients_op #operations

def reg():
    conn.commit()
    user_login = input('Login: ')
    user_password = input('Password: ')

    cursor.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
    #cursor.execute("SELECT password FROM users")

    if cursor.fetchone() is None:
        print("!")
        cursor.execute(f"INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, 0))
        conn.commit()


    else:
        print("False")
        for value in cursor.execute("SELECT * FROM users"):
            print(value)

def deleted_all(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    ii = []
    for i in cursor.execute("SELECT number FROM vag_operations"):
        ii.append(i[0])
    print(ii)
    for i in ii:
        cursor.execute(f"DELETE FROM vag_operations WHERE number = '{i}'")
        conn.commit()

def deleted_vagon(number, path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM vag_operations WHERE number = '{number}'")
    conn.commit()

def casino():
    user_login = input('Log in: ')
    number = randint(1, 2)
    cursor.execute(f'SELECT login FROM users WHERE login = "{user_login}"')
    if cursor.fetchone() is None:
        print("Registr")
        reg()
    else:
        if number == 1:
            cursor.execute(f'UPDATE users SET cash = {1000} WHERE login = "{user_login}"')
            conn.commit()
        else:
            print("Fail")
            delete_db(user_login)
            deleted_all()

def show_data(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    for i in cursor.execute('SELECT * FROM vag_operations'):
        print(i)
    value = len(cursor.execute("SELECT * FROM vag_operations").fetchall())
    #value = cursor.fetchall()
    #print(value)
    conn.close()

def cal_date():
    for i in cursor.execute("SELECT time FROM vag_operations"):
        print(i)
    cursor.execute(f"SELECT strftime('%s','now', 'localtime') - strftime('%s', '{i[0]}')")
    t = cursor.fetchone()
    print(t)
    cursor.execute(f"SELECT strftime('%s','now') - strftime('%s', '{i[0]}')")
    cursor.execute("SELECT datetime('now', 'localtime')")
    t = cursor.fetchone()
    print(t)


#add_note(number, operation, time, track, park, client)
#casino()
#deleted_all()
#reg()
#cal_date()
print("Database opened successfully")











#conn.close()