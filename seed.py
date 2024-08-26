import faker
from random import randint
from sqlite3 import Error
from connect import create_connection, database

NUMBER_USERS = 7
NUMBER_TASKS= 30
NUMBER_STATUSES = 3

#generating tuples for filling each field in our tables
def generate_data(number_users, number_tasks):
    users_names = []
    users_emails = []
    statuses = ["new", "in progress", "completed"]
    tasks_titles = []
    tasks_descriptions = []
    fake_data = faker.Faker()
    for i in range(number_users):
        users_names.append(fake_data.name())
        users_emails.append(fake_data.email())
    for i in range(number_tasks):
        tasks_titles.append(fake_data.sentence(nb_words=4))
        tasks_descriptions.append(fake_data.text(max_nb_chars=200))
    return users_names, users_emails, statuses, tasks_titles, tasks_descriptions

# preparing tuples for our 3 tables
def prepare_data(users_names, users_emails, statuses, tasks_titles, tasks_descriptions):
    for_users = []
    for name, email in zip(users_names, users_emails):  # Pair each name with its email
        for_users.append((name, email))
    
    for_status = []
    for status in statuses:
        for_status.append((status, ))
    
    for_tasks = []
    for title, description in zip(tasks_titles, tasks_descriptions): # Pair each title with its description
        for_tasks.append((title, description, randint(1, NUMBER_STATUSES), randint(1, NUMBER_USERS)))
    
    return for_users, for_status, for_tasks

def insert_data_to_db(users, status, tasks) -> None:
    with create_connection(database) as conn:
        if conn is not None:
            try:         
                c = conn.cursor()
                sql_to_users = "INSERT INTO users(fullname, email) VALUES(?,?)"
                c.executemany(sql_to_users, users)
                sql_to_status = "INSERT INTO status(name) VALUES(?)"
                c.executemany(sql_to_status, status)
                sql_to_tasks = "INSERT INTO tasks(title, description, status_id, user_id) VALUES(?,?,?,?)"
                c.executemany(sql_to_tasks, tasks)
                conn.commit()
            except Error as e:
                print(e)
        else:
            print("Error! cannot create the database connection.")

if __name__ == "__main__":
    users, status, tasks = prepare_data(*generate_data(NUMBER_USERS, NUMBER_TASKS))
    insert_data_to_db(users, status, tasks)

