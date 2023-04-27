from typing import List
from task.task import Task
import psycopg2
import os

class Database:
    def __init__(self):
        db_host = os.environ['DB_HOST']
        print(f"db_host: {db_host}")
        self.conn = psycopg2.connect(f"host={db_host} dbname=postgres user=postgres password=password")
        self.create_table()

    def create_table(self) -> None:
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
                name varchar(255),
                statement varchar(4096),
                subject varchar(255),
                level int,
                hint varchar(4096),
                solution varchar(4096)
            );
        """)
        self.conn.commit()

    # TODO
    # def export_from_csv()
    # https://www.postgresqltutorial.com/postgresql-tutorial/import-csv-file-into-posgresql-table/
    
    def insert_tasks(self, tasks: List[Task]) -> None:
        cur = self.conn.cursor()
        for task in tasks:
            cur.execute(f"INSERT INTO tasks VALUES {task};")
        self.conn.commit()

    def get_tasks(self, user_task_settings) -> List[Task]:
        # Task settings is a dictionary {Subject: {}, Level: {}}
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks;")

        tasks = []
        for task in cur:
            data = {
                'Name': task[0],
                'Statement': task[1],
                'Subject': task[2],
                'Level': task[3],
                'Подсказка': task[4],
                'Решение': task[5],
            }
            if data == {}:
                continue
            if 'Level' in user_task_settings and not data['Level'] == user_task_settings['Level']:
                continue
            if 'Subject' in user_task_settings and not data['Subject'] == user_task_settings['Subject']:
                continue
            if 'Statement' in data and 'Решение' in data and 'Subject' in data and \
                    'Name' in data and 'Level' in data and 'Подсказка' in data:
                tasks.append(Task(data['Name'], data['Statement'], data['Решение'],
                                  data['Подсказка'], data['Level'], data['Subject']))
        return tasks
