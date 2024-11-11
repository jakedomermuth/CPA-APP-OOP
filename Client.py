import database
from connections import get_connection


class Client:
    def __init__(self, client_name: str, client_address: str, client_income: int, materials_provided: str, cpa_id: int, client_id=None):
        self.client_name = client_name
        self.client_address = client_address
        self.client_income = client_income
        self.materials_provided = materials_provided
        self.cpa_id = cpa_id
        self.client_id = client_id


    def save(self):
        with get_connection() as connection:
            self.client_id = database.add_clients(connection, self.client_name, self.client_address, self.client_income, self.materials_provided, self.cpa_id)

    def exists(self):
        with get_connection() as connection:
            client_name = database.client_exists(connection, self.client_name)
            return client_name is not None

    def update(self):
        with get_connection() as connection:
            database.update_material_status(connection, self.client_id)

    @staticmethod
    def normalize(name: str, address: str, materials_provided: str):
        return name.upper(), address.upper(), materials_provided.upper()

    @staticmethod
    def convert(num_input: str) -> int:
        try:
            num = int(num_input)
            return num
        except ValueError:
            print('The number must be an integer!')
