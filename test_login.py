from app import app

def test_login_success():
    client = app.test_client()
    response = client.post("/", data={
        "username": "admin",
        "password": "123456"
    })
    assert b"Login successful!" in response.data

def test_login_fail():
    client = app.test_client()
    response = client.post("/", data={
        "username": "wrong",
        "password": "wrong"
    })
    assert b"Invalid username or password!" in response.data
