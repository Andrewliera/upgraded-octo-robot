import configparser
import os
import urllib.request
import json
import wufoo_db


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


def get_form_info():  # comment for workflow
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


def save_response_as_file(response, filename: str):
    f = f'saved_entries/{filename}'
    try:
        os.makedirs("saved_entries")
    except FileExistsError:
        pass
    try:
        f = open(f, "w")
    except IOError:
        f = open(f, 'r+')
    json_data = json.load(response)
    json.dump(json_data, f, indent=4, sort_keys=False)
    f.write("\n")


if __name__ == '__main__':
    print("Welcome to a simple Wufoo form checker")
    try:
        db_file = 'my_form_db.sqlite'
        entry_file = 'my_entries.json'
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
                save_response_as_file(api_output, entry_file)
                wufoo_db.configure_db(db_file, entry_file)
                print("\nFile Entries Saved")
            else:
                start_prog = input("To continue press c"
                                   "\n other keys to exit"
                                   "\nYour Input: ")
        print("Exiting Program")
    except BadInput:
        raise BadInput()
