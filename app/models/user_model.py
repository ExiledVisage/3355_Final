import sqlite3

def connectionUser():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,            
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        country TEXT NOT NULL,
        city TEXT NOT NULL                       
    )
''')
    print("merhaba user!")
    connection.commit()
    connection.close()


#Create User
def RegisterUser(email,name,surname,password,country,city):
    connection =sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (name,surname,email,password,country,city) VALUES (?,?,?,?,?,?)",(name,surname,email,password,country,city,))

    connection.commit()
    connection.close()


#validate user
def validateUser(email,password):
    connection =sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    cursor.execute("SELECT username FROM user WHERE email = ? AND password = ?", (email, password,))
    user = cursor.fetchone()
    
    connection.commit()
    connection.close()

    if user == None:
        return False, None
    else:
        return True,user
    
def insert_users():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    user_list = [
    ('Kerem', 'Irmak', 'kerem12irmak@hotmail.com', 'kerem2404', 'Turkey', 'Izmir'),
    ('Akin', 'Aydin', 'akinaydin_0@hotmail.com', 'akin234', 'Turkey', 'Izmir'),
    ]

    try:
        cursor.executemany('''
            INSERT INTO users (name, surname, email, password, country, city)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', user_list)
        connection.commit()
        print("Users inserted successfully!")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    finally:
        connection.close()
        
def drop_table_users():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    try:
        cursor.execute('DROP TABLE IF EXISTS users')
        connection.commit()
        print("Table 'users' dropped successfully!")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def is_valid_password(password):
    # Check if the password meets the criteria (at least 8 characters, 1 number, 1 non-alphanumeric character)
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(not char.isalnum() for char in password):
        return False
    return True        



