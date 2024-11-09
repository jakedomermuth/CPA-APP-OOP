import database
from connections import get_connection


class Cpa:
    def __init__(self, name: str, cpa_id=None):
        self.name = name
        self.cpa_id = cpa_id

    def exists(self):
        with get_connection() as connection:
            cpa_name = database.cpa_exists(connection, self.name)
            return cpa_name is not None

    def save(self):
        with get_connection() as connection:
            self.cpa_id = database.add_cpa(connection, self.name)

    @staticmethod
    def normalize(name: str):
        return name.upper()





