import database
from connections import get_connection

class Taxes:
    def __init__(self, status: str, current_timestamp: float, checked: str, client_id: int, tax_id = None):
        self.tax_id = tax_id
        self.status = status
        self.current_timestamp = current_timestamp
        self.checked = checked
        self.client_id = client_id

    def save(self):
        with get_connection() as connection:
            print(f"status: {self.status}, filed_timestamp: {self.current_timestamp}, checked: {self.checked}, client_id: {self.client_id}")
            database.add_taxes(connection, self.status, self.current_timestamp, self.checked, self.client_id)

    @staticmethod
    def normalize(name: str):
        return name.upper()

    @staticmethod
    def convert(client_id: str) -> int:
        try:
            client_id = int(client_id)
            return client_id
        except ValueError:
            print('The ID must be an integer!')