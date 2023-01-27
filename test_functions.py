from main import get_form_info
from main import TempKey


def test_config():
    key_configured = TempKey.apikey
    assert key_configured is not None


def test_auth():
    pass


def test_connection():
    pass


def test_response():
    response = get_form_info()
    assert response is not None
