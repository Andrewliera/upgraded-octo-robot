import configparser
import os
import urllib.request
import json


class GetFormError(Exception):
    """Exception raised while getting form information"""
    pass


class BadConfig(Exception):
    """Exception raised in app configuration"""
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
    try:
        os.makedirs("saved_entries")
    except FileExistsError:
        pass
    f = f'saved_entries/{filename}'
    try:
        f = open(f, "w")
    except IOError:
        f = open(f, 'r+')
    json_data = json.load(response)
    json.dump(json_data, f, indent=4, sort_keys=False)
    f.write("\n")
