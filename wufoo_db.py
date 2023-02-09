import json
import sqlite3
from typing import Tuple


def format_data_to_db(cursor: sqlite3.Cursor, filename: str):
    try:
        bar = open(f'./saved_entries/{filename}')
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
        cursor.execute('''INSERT INTO entries VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT do nothing;''',
                       (e_id, suffix, l_name, f_name, title,
                        org_name, email, org_site, phone, proj,
                        guest_speaker, site_visit, job_shadow,
                        internship, career_panel, networking_event,
                        summer, fall, spring, summer_2, other, discussion))


def delete_entry(cursor: sqlite3.Cursor, entry: str):
    cursor.execute('''DELETE FROM entries 
    WHERE e_id like ?;''', entry)


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


def configure_db(dbname: str, entry_filename: str):
    conn, cursor = open_db(dbname)
    setup_db(cursor)
    format_data_to_db(cursor, entry_filename)
    close_db(conn)


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()
