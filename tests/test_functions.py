import json
import os
import wufoo_db
import get_wufuu_info


def test_retrieve_data():
    wufoo_test_response = get_wufuu_info.get_form_info()
    test_file = 'test_entries.json'
    get_wufuu_info.save_response_as_file(wufoo_test_response, test_file)

    with open(f'saved_entries/{test_file}', 'r') as response_file:
        response_data = json.load(response_file)
    assert len(response_data['Entries']) > 1


def test_db_contains_entry():
    test_file = 'test_entries.json'
    test_database = 'test_database.sqlite'
    wufoo_db.configure_db(test_database, test_file)

    conn, cursor = wufoo_db.open_db(test_database)
    test_query = wufoo_db.select_all(cursor)
    wufoo_db.close_db(conn)
    assert test_query is not None
    remove_test_files(f'saved_entries/{test_file}')
    remove_test_files(test_database)


def test_populated_gui():
    pass


def remove_test_files(filename: str):
    if os.path.exists(filename):
        os.remove(filename)
