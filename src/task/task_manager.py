from typing import Tuple

from task.database import Database
from task.users_manager import UsersManager
from task.user import User


class TaskManager:
    def __init__(self):
        self.users_manager = UsersManager()
        self.database = Database()

    def register_new_user(self, user_id: int):
        new_user = User(user_id)
        self.users_manager.add_user(new_user)

    def set_subject(self, user_id: int, subject: str):
        # user_ind = self.users_manager.get_user_ind_by_id(user_id)
        self.users_manager.users[user_id].set_settings_subject(subject)

    def set_level(self, user_id: int, level: str):
        # user_ind = self.users_manager.get_user_ind_by_id(user_id)
        self.users_manager.users[user_id].set_settings_level(level)

    def get_settings(self, user_id: int):
        return self.users_manager.get_user_by_id(user_id).get_settings()

    def get_statement(self, user_id: int, task_id: int):
        return self.users_manager.get_user_by_id(user_id).get_task_by_id(task_id).get_statement()

    def get_hint(self, user_id: int, task_id: int):
        if not self.users_manager.get_user_by_id(user_id).get_given_tasks():  # At least one task has been given
            return "Attempted to get a hint before the problem was given"
        # user_ind = self.users_manager.get_user_ind_by_id(user_id)
        return self.users_manager.users[user_id].get_task_by_id(task_id).ask_for_hint()

    def get_solution(self, user_id: int, task_id: int):
        assert self.users_manager.get_user_by_id(user_id).get_given_tasks()  # At least one task has been given
        return self.users_manager.get_user_by_id(user_id).get_task_by_id(task_id).get_solution()

    def get_task(self, user_id: int) -> Tuple[str, str]:
        # Returns statement and task id. If there no relevant tasks, throws KeyError
        settings = self.users_manager.get_user_by_id(user_id).get_settings()
        relevant_tasks = [task for task in self.database.get_tasks(settings)
                          if not self.users_manager.get_user_by_id(user_id).is_given(task)]
        # now we have a list of tasks which meet all the criteria
        if not relevant_tasks:  # At least one task has been given
            raise KeyError('Больше нет задач, удовлетворяющих критериям. Выбери другую тему и/или сложность')
        task = relevant_tasks[0]
        # user_ind = self.users_manager.get_user_ind_by_id(user_id)
        self.users_manager.users[user_id].give_task(task)
        title = f'**{task.get_task_name()}**'
        statement = task.get_statement()
        return f'{title}\n\n{statement}', task.get_id()
