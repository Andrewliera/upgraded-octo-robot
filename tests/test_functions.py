def test_config():
    foo = "[secrets]\n"
    f = open("./config/app.config", "r")
    lines = f.readlines()
    assert foo in lines


def test_1():
    pass

