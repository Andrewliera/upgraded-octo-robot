import requests
import configparser


class BadInput(Exception):
    print("Bad input used in program")


class BadKeyConfig(Exception):
    print("Bad Key Configured")


class NewError(Exception):
    print("New Error raised")


class TempKey:
    try:
        config = configparser.ConfigParser()
        config.read('app.config')
        config.sections()
        key = config['secrets']['apikey']
    except BadKeyConfig:
        raise BadKeyConfig


def get_form_info():
    try:
        response = requests.get('http://agonz.wufoo.com/api/v3/forms/{}/entries.json'.format(TempKey.key))
        print(response)
    except NewError:
        raise NewError


if __name__ == '__main__':
    print("Welcome to a simple Wufoo form checker")
    try:
        start_prog = input("To continue press c\nother keys to exit\nYour Input: ")

        while start_prog == 'c':
            user_input = input("Would you like to Check your Wufoo Form?\ny key to continue\n other keys to exit\nYour Input: ")
            if user_input == 'y':
                get_form_info()
            else:
                start_prog = input("To continue press c\n other keys to exit\nYour Input: ")

        print("Exiting Program")

    except BadInput:
        raise BadInput()
        pass



