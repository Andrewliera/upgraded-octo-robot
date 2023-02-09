import urllib.request


def test_internet():
    response = urllib.request.\
        urlopen('https://jsonplaceholder.typicode.com/todos/1')
    assert response is not None
