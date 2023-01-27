import configparser
import urllib.request
import json


class BadInput(Exception):
    print("Bad input used in program")


class BadConfig(Exception):
    print("Bad Key Configured")


class GetFormError(Exception):
    print("New Error raised getting form")


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
        f = open(f, "w")
        print("Files Exists!")
    except IOError:
        f = open(f, 'w+')
        print("File Created!")

    json_data = json.load(response)
    json.dump(json_data, f, indent=4, sort_keys=True)
    f.write("\n")


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
                print("\nFile Entries Saved")
            else:
                start_prog = input("To continue press c"
                                   "\n other keys to exit"
                                   "\nYour Input: ")

        print("Exiting Program")

    except BadInput:
        raise BadInput()
