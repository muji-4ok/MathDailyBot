from task.level import Level


class Task:
    # Basic
    name = ''
    statement = ''
    solution = ''

    # Complexity
    level = Level()

    # Hints
    hint = ''
    is_hint = False  # True if user has asked for a hint

    # Subject
    subject = ''

    # Rating (in further updates)
    # num_ratings = 0  # number of users who have rated the problem
    # rating = 0.0

    def __init__(self, name, statement, solution, hint='', level=0, subject=''):
        self.name = name
        self.id = hash(name)

        self.level = Level()
        self.level.set_level(level)

        self.statement = statement
        self.solution = solution

        self.hint = hint
        self.is_hint = 0

        self.subject = subject

    # Basic
    def get_task_name(self):
        return self.name

    def get_statement(self):
        return self.statement

    def get_solution(self):
        return self.solution

    def get_id(self):
        return self.id

    def ask_for_hint(self):
        if not self.is_hint:
            self.is_hint = True
            return self.hint
        else:
            return "No more hints are available. Would you like to see the solution?"

    # Levels
    def set_level(self, lev):
        self.level.set_level(lev)

    def get_level_name(self):
        return self.level.get_level_name()

    @staticmethod
    def get_subjects_list():
        return ['Logic', 'Set theory', 'Combinatorics']

    def __str__(self) -> str:
        return f"('{self.name}', )"
        #         cur = self.conn.cursor()
        # cur.execute("""CREATE TABLE tasks (
        #         name varchar(255),
        #         statement varchar(1024),
        #         subject varchar(255),
        #         level int,
        #         hint varchar(255),
        #         solution varchar(1024)
        #     )
        # """)
