import database, connections
from Cpa import Cpa
from Assistant import Assistant
from Client import Client
from Taxes import Taxes
import datetime
import pytz as pytz

MENU_PROMPT = """
    1: ADD CPAs
    2: Add Assistants
    3: Add Clients
    4: Update Provided Material Status
    5: Check Provided Material Status
    6: Change filing status
    7: Check filing status
    8: Update CPA checked Return
    9: Check if CPA checked return
    Select an Option: """


def new_cpa_prompt():
    input_name = input("What is the CPA's name? ")

    name = Cpa.normalize(input_name)
    cpa_instance = Cpa(name)

    if cpa_instance.exists():
        print('This CPA already exists')
    else:
        cpa_instance.save()
        print(f"New CPA added with ID: {cpa_instance.cpa_id}, Name: {cpa_instance.name}")


def new_assistants_prompt():
    input_name = input("What is the Assistants name? ")
    _id = input("What is their CPAs ID? ")

    name = Assistant.normalize(input_name)
    cpa_id = Assistant.convert(_id)
    assistant_instance = Assistant(name, cpa_id)

    if assistant_instance.exists():
        print("This Assistant already exists")
    else:
        assistant_instance.save()
        print(f"New Assistant added with ID: {assistant_instance.assistant_id}, Name: {assistant_instance.name}")


def new_client_prompt():
    client_name = input('What is the Clients name? ')
    client_address = input('What is the clients Address (ex: Street Number, Street Name): ')
    client_income = input('What is the Clients income? ')
    materials_provided = input('Has the Client Provided Tax Materials?(True/False) ')
    cpa_id = input('What is the ID of the Clients CPA? ')

    client_name, client_address, materials_provided = Client.normalize(client_name, client_address, materials_provided)
    client_income = Client.convert(client_income)
    cpa_id = Client.convert(cpa_id)
    client_instance = Client(client_name, client_address, client_income, materials_provided, cpa_id)

    if client_instance.exists():
        print("This Client already exists")
    else:
        client_instance.save()
        if materials_provided == 'TRUE':
            status, current_timestamp, checked = new_tax_prompt()
            print(f"status={status}, timestamp={current_timestamp}, checked={checked}, client_id={client_instance.client_id}")

            tax_instance = Taxes(status, current_timestamp, checked, client_instance.client_id)
            tax_instance.save()



def new_tax_prompt():
    input_status = input('Has the tax return been filed? (True/False)')
    status = Taxes.normalize(input_status)
    current_datetime_utc = datetime.datetime.now(tz=pytz.utc)
    current_timestamp = current_datetime_utc.timestamp()
    if status == 'TRUE':
        checked_input = input('Has the tax return been checked by a CPA?(True/False) ')
        checked = Taxes.normalize(checked_input)
    else:
        checked = 'FALSE'
    return status, current_timestamp, checked


def update_client_prompt():
    input_id = input("What is the client's ID?" )
    client_id = Client.normalize(input_id)
    client_instance = Client(client_id)
    if client_instance.exists():
        update_choice = input('Has the client provided all necessary tax material?(True/False) ')
        choice = Client.convert(update_choice)
        if choice == 'True':
            client_instance.update()
            print('Client Updated')
    else:
        print('Client does not exist')



MENU_OPTIONS = {
    '1': new_cpa_prompt,
    '2': new_assistants_prompt,
    '3': new_client_prompt,
    '4': update_client_prompt,
    '5': 'Check Provided Material Status',
    '6': 'Change filing status',
    '7': 'Check filing status',
    '8': 'Update CPA checked Return',
    '9': 'Check if CPA checked return'
}

def menu():
    with connections.get_connection() as connection:
        database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != '10':
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print('Invalid selection. Please try again!')


if __name__ == '__main__':
    menu()
