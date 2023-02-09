import configparser
import os
import urllib.request
import json
import sqlite3
from typing import Tuple


class BadInput(Exception):
    """Exception raised in user input"""
    pass


class BadConfig(Exception):
    """Exception raised in app configuration"""
    pass


class GetFormError(Exception):
    """Exception raised while getting form information"""
    pass


class TempKey:
    try:
        config = configparser.ConfigParser()
        config.read('config/app.config')
        config.sections()
        baseurl = config['secrets']['baseurl']
        apikey = config['secrets']['apikey']
        identifier = config['secrets']['identifier']
        passwd = config['secrets']['passwd']
    except BadConfig:
        raise BadConfig


def get_form_info():
    try:
        password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(
            None, TempKey.baseurl, TempKey.apikey, TempKey.passwd
        )
        handler = urllib.request.HTTPBasicAuthHandler(password_manager)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(
            TempKey.baseurl + TempKey.identifier + '/entries.json'
        )
        return response
    except GetFormError:
        raise GetFormError


def save_response_as_file(response):
    f = 'saved_entries/my_entries.json'
    try:
        os.makedirs("saved_entries")
    except FileExistsError:
        pass
    try:
        f = open(f, "w")
        print("Files Exists!")
    except IOError:
        f = open(f, 'w+')
        print("File Created!")

    json_data = json.load(response)
    json.dump(json_data, f, indent=4, sort_keys=False)
    f.write("\n")


def format_data_to_db(cursor: sqlite3.Cursor):
    try:
        bar = open('./saved_entries/my_entries.json')
        foo = json.load(bar)
    except IOError:
        raise IOError

    for entry in foo['Entries']:
        e_id = entry['EntryId']
        suffix = entry['Field1']
        f_name = entry['Field2']
        l_name = entry['Field3']
        title = entry['Field6']
        org_name = entry['Field7']
        email = entry['Field8']
        org_site = entry['Field9']
        phone = entry['Field10']
        proj = entry['Field11']
        guest_speaker = entry['Field12']
        site_visit = entry['Field13']
        job_shadow = entry['Field14']
        internship = entry['Field15']
        career_panel = entry['Field16']
        networking_event = entry['Field17']
        summer = entry['Field111']
        fall = entry['Field112']
        spring = entry['Field113']
        summer_2 = entry['Field114']
        other = entry['Field115']
        discussion = entry['Field211']
        print(e_id)
        cursor.execute('''INSERT INTO entries VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT do nothing;''',
                       (e_id, suffix, l_name, f_name, title,
                        org_name, email, org_site, phone, proj,
                        guest_speaker, site_visit, job_shadow,
                        internship, career_panel, networking_event,
                        summer, fall, spring, summer_2, other, discussion))


def setup_db(cursor: sqlite3.Cursor):

    cursor.execute('''CREATE TABLE IF NOT EXISTS entries(
    e_id INTEGER PRIMARY KEY,
    suffix TEXT,
    f_name TEXT NOT NULL,
    l_name TEXT NOT NULL,
    title TEXT NOT NULL,
    org_name TEXT NOT NULL,
    email TEXT NOT NULL,
    org_site TEXT,
    phone TEXT,
    proj TEXT,
    guest_speaker TEXT,
    site_visit TEXT,
    job_shadow TEXT,
    internship TEXT,
    career_panel TEXT,
    networking_event TEXT,
    summer TEXT,
    fall TEXT,
    spring TEXT,
    summer_2 TEXT,
    other TEXT,
    discussion TEXT default 'No');''')


def configure_db():
    conn, cursor = open_db("test_db.sqlite")
    setup_db(cursor)
    print(type(conn))
    format_data_to_db(cursor)
    close_db(conn)


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()


if __name__ == '__main__':
    print("Welcome to a simple Wufoo form checker")
    try:
        start_prog = input("To continue press c"
                           "\nother keys to exit"
                           "\nYour Input: ")
        while start_prog == 'c':
            user_input = input("Save your Wufoo Form entries?"
                               "\ny key to continue"
                               "\n other keys to exit"
                               "\nYour Input: ")
            if user_input == 'y':
                api_output = get_form_info()
                save_response_as_file(api_output)
                configure_db()
                print("\nFile Entries Saved")
            else:
                start_prog = input("To continue press c"
                                   "\n other keys to exit"
                                   "\nYour Input: ")

        print("Exiting Program")

    except BadInput:
        raise BadInput()
