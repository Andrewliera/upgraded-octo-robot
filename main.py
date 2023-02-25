import get_wufuu_info
import wufoo_db
import app_gui

if __name__ == '__name__':
    entry_file = 'my_entries.json'
    db_file = 'my_form_db.sqlite'
    call_api = get_wufuu_info.get_form_info()
    get_wufuu_info.save_response_as_file(call_api, entry_file)
    wufoo_db.configure_db(db_file, entry_file)
    app_gui.run_gui()
