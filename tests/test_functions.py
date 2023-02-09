import main


def test_config():
    foo = "[secrets]\n"
    f = open("./config/app.config", "r")
    lines = f.readlines()
    assert foo in lines


def test_1():
    f = "./saved_entries/my_entries.json"
    test_response = \
        {"TestEntry": [
            {
                "EntryId": "1",
                "Field1": "Mr",
                "Field2": "John",
                "Field3": "Title",
                "Field7": "Org Name",
                "Field8": "Email@email.com",
                "Field9": "orgwebsite.website",
                "Field10": "1234567890",
            }
        ]
        }
    main.save_response_as_file(test_response)
    test_read = open(f, "r")
    lines = test_read.readlines()
    assert test_response in lines

