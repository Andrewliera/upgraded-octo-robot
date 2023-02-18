import json
import urllib.request
import wufoo_db


def test_internet():
    response = urllib.request.\
        urlopen('https://jsonplaceholder.typicode.com/todos/1')
    assert response is not None


def test_db():
    test_entry = \
        {"TestEntry": [
            {
                "EntryId": "1",
                "Field1": "Mr",
                "Field2": "John",
                "Field3": "Title",
                "Field7": "Org Name",
                "Field8": "Email@email.com",
                "Field9": "org-website.website",
                "Field10": "1234567890",
            }
        ]
        }
    with open('../my_entries/convert.json', 'w') as convert_file:
        convert_file.write(json.dumps(test_entry))
    f = 'test_db.sqlite'
    assert wufoo_db.configure_db(f, '../my_entries/convert.json')
