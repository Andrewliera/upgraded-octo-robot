import json
import os
import app_gui
import pytest
import wufoo_db
import get_wufuu_info


def test_retrieve_data():
    path = 'saved_entries/'
    test_file = 'test_entries.json'
    path_exist = os.path.exists(path)
    if not path_exist:
        os.makedirs(path)

    wufoo_test_response = get_wufuu_info.get_form_info()
    get_wufuu_info.save_response_as_file(wufoo_test_response, test_file)

    with open(f'{path}{test_file}', 'r') as response_file:
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


@pytest.fixture
def test_app(qtbot):
    filename = 'my_form_db.sqlite'
    test_gui = app_gui.MyGui(filename=filename)
    return test_gui


def test_populated_gui(test_app):
    test_data = ['Course Project',
                 'Guest Speaker',
                 'Site Visit',
                 'Job Shadow',
                 'Internships',
                 'Career Panel',
                 ]
    test_app.update_checkboxes(test_data)
    assert test_app.proj_checkbox.isChecked() \
           and test_app.guest_checkbox.isChecked() \
           and test_app.site_visit_checkbox.isChecked()


def remove_test_files(filename: str):
    try:
        os.remove(filename)
    except OSError as error:
        print(error)
        print("could not remove file")


def remove_test_folder(foldername: str):
    try:
        os.rmdir(foldername)
    except OSError as error:
        print(error)
        print("Could not remove directory")


def clean_up():
    test_file = 'test_entries.json'
    test_database = 'test_database.sqlite'
    path = 'saved_entries/'
    remove_test_files(f'{path}{test_file}')
    remove_test_files(test_database)
    remove_test_folder(path)


clean_up()
