from sqlite3 import Error
from connect import create_connection, database

def sql_select(conn, sql):
    rows = None
    c = conn.cursor()
    try:
        c.execute(sql)
        rows = c.fetchall()
    except Error as e:
        print(e)
    finally:
        c.close()
    return rows

def sql_update(conn, sql):
    c = conn.cursor()
    try:
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        c.close()

if __name__ == '__main__':
    with create_connection(database) as conn:
        task_1 = "SELECT * FROM tasks WHERE user_id = 5;"
        print(sql_select(conn, task_1))
        print()

        task_2 = "SELECT * FROM tasks WHERE status_id = 1;"
        print(sql_select(conn, task_2))
        print()
        
        task_3 = "UPDATE tasks SET status_id = 3 WHERE id = 13;"
        sql_update(conn, task_3)
        print("Query is executed")
        print()
        
        task_4 = """SELECT users.fullname, users.email
        FROM users
        LEFT JOIN tasks ON users.id = tasks.user_id
        WHERE tasks.user_id IS NULL;"""
        print(sql_select(conn, task_4))
        print()
        
        task_5 = "SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);"
        print(sql_select(conn, task_5))
        print()
        
        task_6 = """INSERT INTO tasks (title, description, user_id, status_id)
        VALUES("prepare report", "gather data from sales department for the last month.", 5, 1);"""
        sql_update(conn, task_6)
        print("Query is executed")
        print()
        
        task_7 = "SELECT * FROM tasks WHERE NOT status_id = 3"
        print(sql_select(conn, task_7))
        print()
        # same query in other way
        task_7_1 = """SELECT tasks.*
        FROM tasks
        JOIN status ON tasks.status_id = status.id
        WHERE status.name != 'completed';"""
        print(sql_select(conn, task_7_1))
        print()

        task_8 = "DELETE FROM tasks WHERE id = 15;"
        sql_update(conn, task_8)
        print("Query is executed")
        print()

        task_9 = 'SELECT * FROM users WHERE email LIKE "wil%";'
        print(sql_select(conn, task_9))
        print()

        task_10 = 'UPDATE users SET fullname = "Petro Petrov" WHERE id = 3;'
        sql_update(conn, task_10)
        print("Query is executed")
        print()

        task_11 = """SELECT COUNT(status_id) as total_tasks, status_id 
        FROM tasks 
        GROUP BY status_id;"""
        print(sql_select(conn, task_11))
        print()

        task_12 = """SELECT tasks.*
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE users.email LIKE '%@example.com';"""
        print(sql_select(conn, task_12))
        print()

        task_13 = "SELECT * FROM tasks WHERE description IS NULL;"
        print(sql_select(conn, task_13))
        print()

        task_14 = """SELECT users.fullname, users.email, tasks.title, tasks.description, tasks.status_id 
        FROM users
        INNER JOIN tasks ON users.id = tasks.user_id
        INNER JOIN status ON tasks.status_id = status.id
        WHERE status.name = 'in progress';"""
        print(sql_select(conn, task_14))
        print()

        task_15 = """SELECT users.fullname, COUNT(tasks.id) AS task_count
        FROM users
        LEFT JOIN tasks ON users.id = tasks.user_id
        GROUP BY users.fullname;"""
        print(sql_select(conn, task_15))
        print()


