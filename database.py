from typing import List, Tuple
from psycopg2.extras import execute_values



# creating queries------------------------------------------------------------------------------------------------------

CREATE_CPA_TABLE = """
CREATE TABLE IF NOT EXISTS cpa
(cpa_id SERIAL PRIMARY KEY,
name TEXT);
"""

CREATE_ASSISTANT_TABLE = """
CREATE TABLE IF NOT EXISTS assistants
(assistant_id SERIAL PRIMARY KEY,
name TEXT,
cpa_id INT references cpa(cpa_id));
"""

CREATE_CLIENT_TABLE = """
CREATE TABLE IF NOT EXISTS clients
(client_id SERIAL PRIMARY KEY,
client_name TEXT,
client_address TEXT,
client_income INT,
materials_provided TEXT,
cpa_id INT references cpa(cpa_id));
"""

CREATE_TAX_RETURN_TABLE = """
CREATE TABLE IF NOT EXISTS taxes
(tax_id SERIAL PRIMARY KEY,
status TEXT,
filed_timestamp BIGINT,
checked TEXT,
client_id INT references clients(client_id));
"""


# inserting queries ----------------------------------------------------------------------------------------------------
INSERT_CPA = """INSERT INTO cpa(name) VALUES (%s) RETURNING cpa_id;"""

INSERT_ASSISTANTS = """INSERT INTO assistants(name, cpa_id) VALUES (%s, %s) RETURNING assistant_id;"""

INSERT_CLIENTS = """INSERT INTO clients(client_name, client_address, client_income, materials_provided, cpa_id)
VALUES (%s, %s, %s, %s, %s) RETURNING client_id; """

INSERT_TAXES = """INSERT INTO taxes(status, filed_timestamp, checked, client_id) VALUES (%s, %s, %s, %s)
RETURNING tax_id;"""


# selecting queries ---------------------------------------------------------------------------------------------------
SELECT_MATERIAL_STATUS = """SELECT materials_provided FROM clients where client_id = %s;"""

SELECT_FILED_STATUS= """SELECT status FROM taxes WHERE tax_id = %s;"""

SELECT_CHECKED_STATUS = """SELECT checked FROM taxes WHERE tax_id = %s;"""

SELECT_CPA = """SELECT * FROM cpa WHERE name = %s;"""

SELECT_ASSISTANT = """SELECT * FROM assistants WHERE name = %s;"""

SELECT_CLIENT = """SELECT * FROM clients WHERE client_name = %s;"""

SELECT_CLIENT_BY_ID = """SELECT * FROM clients WHERE client_id = %s;"""

SELECT_TAXES_BY_ID = """SELECT * FROM taxes WHERE tax_id = %s;"""

# updating queries ----------------------------------------------------------------------------------------------------
UPDATE_MATERIAL_STATUS = """UPDATE clients SET materials_provided = 'TRUE' WHERE client_id = %s; """

UPDATE_FILED_STATUS = """UPDATE taxes SET status = 'TRUE' WHERE tax_id = %s;"""

UPDATE_CHECKED_STATUS = """UPDATE taxes SET checked = 'TRUE' WHERE tax_id = %s"""


def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CPA_TABLE)
            cursor.execute(CREATE_ASSISTANT_TABLE)
            cursor.execute(CREATE_CLIENT_TABLE)
            cursor.execute(CREATE_TAX_RETURN_TABLE)


# inserting functions

def add_cpa(connection, name: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CPA, (name, ))
            cpa_id = cursor.fetchone()[0]
            return cpa_id


def add_assistant(connection, name: str, cpa_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_ASSISTANTS, (name, cpa_id))
            assistant_id = cursor.fetchone()[0]
            return assistant_id


def add_clients(connection, client_name: str, client_address: str, client_income: int, materials_provided: str, cpa_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CLIENTS, (client_name, client_address, client_income, materials_provided, cpa_id))
            client_id = cursor.fetchone()[0]
            return client_id


def add_taxes(connection, status, filed_timestamp, checked, client_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_TAXES, (status, filed_timestamp, checked, client_id))
            tax_id = cursor.fetchone()[0]
            return tax_id


# updating functions
def update_material_status(connection, client_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_MATERIAL_STATUS, (client_id, ))


def update_filing_status(connection, tax_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_FILED_STATUS, (tax_id, ))


def update_checked_status(connection, tax_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CHECKED_STATUS, (tax_id, ))
            print(f"Rows affected: {cursor.rowcount}")


#selecting functions
def get_client(connection, client_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CLIENT_BY_ID, (client_id, ))
            client = cursor.fetchone()
            return client

def get_taxes(connection, tax_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_TAXES_BY_ID, (tax_id, ))
            taxes = cursor.fetchone()
            return taxes
def cpa_exists(connection, name: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CPA, (name,))
            cpa_name = cursor.fetchone()
            return cpa_name

def assistant_exists(connection, name: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ASSISTANT, (name,))
            assistant_name = cursor.fetchone()
            return assistant_name


def client_exists(connection, name: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CLIENT, (name,))
            client_name = cursor.fetchone()
            return client_name
