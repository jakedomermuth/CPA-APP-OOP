import database
from connections import get_connection

class Taxes:
    def __init__(self, status: str, current_timestamp: float, checked: str, client_id: int, tax_id = None):
        self.tax_id = tax_id
        self.status = status
        self.current_timestamp = current_timestamp
        self.checked = checked
        self.client_id = client_id

    def __str__(self):
        # status, timestamp, checked, client_id
        return f"Filling Status: {self.status} | Filing Start Date: {self.current_timestamp} | Checked By CPA: {self.checked} Client ID: {self.client_id}"

    def save(self):
        with get_connection() as connection:
            database.add_taxes(connection, self.status, self.current_timestamp, self.checked, self.client_id)

    def update(self):
        with get_connection() as connection:
            database.update_filing_status(connection, self.tax_id)

    def check(self):
        with get_connection() as connection:
            database.update_checked_status(connection, self.tax_id)

    @classmethod
    def get(cls, tax_id: int):
        with get_connection() as connection:
            taxes = database.get_taxes(connection, tax_id)
            if taxes is None:
                return None
            return cls(taxes[1], taxes[2], taxes[3], taxes[4])

    @staticmethod
    def normalize(string: str):
        return string.upper()

    @staticmethod
    def convert(_id: str) -> int:
        try:
            _id = int(_id)
            return _id
        except ValueError:
            print('The ID must be an integer!')
