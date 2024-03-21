import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table_users(conn) -> None:
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL,
                                    password TEXT NOT NULL,
                                    priv TEXT
                                );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_users_table)
    except sqlite3.Error as e:
        print(e)


def create_table_tasks(conn) -> None:
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id INTEGER PRIMARY KEY,
                                    study TEXT NOT NULL,
                                    task TEXT NOT NULL
                                );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_tasks_table)
    except sqlite3.Error as e:
        print(e)
        

def add_user(conn, username, password, priv):
    sql = ''' INSERT INTO users(username,password,priv)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (username, password, priv))
    conn.commit()
    return cur.lastrowid


def add_task(conn, study, task):    
    sql = ''' INSERT INTO tasks(study,task)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (study, task))
    conn.commit()
    return cur.lastrowid


def read_users(conn) -> list:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()
    return rows


def read_tasks(conn) -> list:
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()
    return rows


def len_users(conn) -> str:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")

    rows = cur.fetchall()
    return str(rows[0][0])


def len_tasks(conn) -> str:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tasks")

    rows = cur.fetchall()
    return str(rows[0][0])

def delete_user(conn, user_id):
    query = f"DELETE FROM users WHERE id = {user_id};"
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()   
    query_update = "UPDATE users SET id = id - 1 WHERE id > ?;"
    cur.execute(query_update, (user_id,))
    conn.commit()
           


def main():
    database = "users.db"
    conn = create_connection(database)
    with conn:
        create_table(conn)

if __name__ == '__main__':
    main()
