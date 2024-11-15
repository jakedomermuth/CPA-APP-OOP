import database
from connections import get_connection


class Assistant:
    def __init__(self, name: str, cpa_id: int, assistant_id=None):
        self.name = name
        self.cpa_id = cpa_id
        self.assistant_id = assistant_id


    def exists(self):
        with get_connection() as connection:
            assistant_name = database.assistant_exists(connection, self.name)
            return assistant_name is not None


    def save(self):
        with get_connection() as connection:
            self.assistant_id = database.add_assistant(connection, self.name, self.cpa_id)


    @staticmethod
    def normalize(name: str):
        return name.upper()

    @staticmethod
    def convert(cpa_id: str) -> int:
        try:
            cpa_id = int(cpa_id)
            return cpa_id
        except ValueError:
            print('The ID must be an integer!')
            return
