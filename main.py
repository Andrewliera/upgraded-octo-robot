import wufoo_db
import get_wufuu_info
import app_gui


class BadInput(Exception):
    """Exception raised in user input"""
    pass


def my_main():
    app_gui.run_gui()


if __name__ == '__main__':
    print("Welcome to a simple Wufoo form checker")
    try:
        db_file = 'my_form_db.sqlite'
        entry_file = 'my_entries.json'
        start_prog = input("To continue press c"
                           "\n other keys to exit"
                           "\nYour Input: ")
        while start_prog == 'c':
            user_input = input("Save your Wufoo Form entries?"
                               "\ny key to continue"
                               "\n other keys to exit"
                               "\nYour Input: ")
            if user_input == 'y':
                api_output = get_wufuu_info.get_form_info()
                get_wufuu_info.save_response_as_file(api_output, entry_file)
                wufoo_db.configure_db(db_file, entry_file)
                print("\nFile Entries Saved")
            else:
                start_prog = input("To continue press c"
                                   "\n other keys to exit"
                                   "\nYour Input: ")
        print("Exiting Program")
    except BadInput:
        raise BadInput()
