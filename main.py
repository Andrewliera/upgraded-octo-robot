import app_gui


if __name__ == '__main__':
    entry_file = 'my_entries.json'
    db_file = 'my_form_db.sqlite'
    app_gui.run_gui(db_file, entry_file)
