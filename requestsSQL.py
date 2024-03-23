import sqlite3
import json  
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    create_table_users(conn)
    create_table_tasks(conn)
    create_table_task_completions(conn)
    
def create_table_users(conn):
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL UNIQUE,
                                    password TEXT NOT NULL,
                                    priv TEXT
                                );"""
    execute_sql(conn, sql_create_users_table)

def create_table_tasks(conn):
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id INTEGER PRIMARY KEY,
                                    study TEXT NOT NULL,
                                    task TEXT NOT NULL
                                );"""
    execute_sql(conn, sql_create_tasks_table)

def create_table_task_completions(conn):
    sql_create_task_completions_table = """CREATE TABLE IF NOT EXISTS task_completions (
                                                id INTEGER PRIMARY KEY,
                                                user_id INTEGER NOT NULL,
                                                task_id INTEGER NOT NULL,
                                                completion_time INTEGER,
                                                result TEXT,
                                                FOREIGN KEY (user_id) REFERENCES users (id),
                                                FOREIGN KEY (task_id) REFERENCES tasks (id)
                                            );"""
    execute_sql(conn, sql_create_task_completions_table)

def execute_sql(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
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
    study_json = json.dumps(study) 
    sql = ''' INSERT INTO tasks(study,task)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (study_json, task))
    conn.commit()
    return cur.lastrowid

def insert_task_completion(conn, user_id, task_id, result):
    sql_insert_task_completion = """INSERT INTO task_completions (user_id, task_id, result)
                                    VALUES (?, ?, ?);"""
    cur = conn.cursor()
    cur.execute(sql_insert_task_completion, (user_id, task_id, result))
    conn.commit()
    
def check_task_completion(conn, user_id, task_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM task_completions WHERE user_id = ? AND task_id = ?", (user_id, task_id))
    row = cur.fetchone()
    if row:
        return True
    else:
        return False

def update_task_completion(conn, user_id, task_id, completion_time, result):
    sql_update_task_completion = """UPDATE task_completions 
                                   SET completion_time = ?, result = ? 
                                   WHERE user_id = ? AND task_id = ?"""
    cur = conn.cursor()
    cur.execute(sql_update_task_completion, (completion_time, result, user_id, task_id))
    conn.commit()
  
def update_task(conn, id, study, task):
    study_json = json.dumps(study)
    print(id, study, task)
    
    sql = ''' UPDATE tasks
              SET study = ? ,
                  task = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (study_json, task, id))
    conn.commit()


def read_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return rows

def read_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    return rows

def len_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    rows = cur.fetchall()
    return str(rows[0][0])

def len_tasks(conn):
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
    
def delete_task_by_id(conn, task_id):
    query = "DELETE FROM tasks WHERE id = ?;"
    cur = conn.cursor()
    cur.execute(query, (task_id,))
    conn.commit()   
    query_update = "UPDATE tasks SET id = id - 1 WHERE id > ?;"
    cur.execute(query_update, (task_id,))
    conn.commit()


def main():
    database = "users.db"
    conn = create_connection(database)
    with conn:
        create_table_users(conn)
        create_table_tasks(conn)
        create_table_task_completions(conn)
