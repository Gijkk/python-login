from app import app
import pytest

# Fixture tạo Flask test client để tái sử dụng trong các test
@pytest.fixture
def client():
    # Bật chế độ TESTING để Flask xử lý phù hợp trong môi trường test
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Kiểm tra trang login trả về HTML đúng khi truy cập bằng GET
def test_get_login_page(client):
    # Gửi GET tới route gốc
    res = client.get("/")
    # Kiểm tra mã trạng thái HTTP là 200 OK
    assert res.status_code == 200
    # Kiểm tra nội dung HTML có form và các label Username/Password
    assert b"<form" in res.data
    assert b"Username" in res.data
    assert b"Password" in res.data

# Kiểm tra trường hợp đăng nhập thành công với thông tin hợp lệ
def test_login_success(client):
    # Gửi POST với username/password đúng (theo fake DB trong app.py)
    res = client.post("/", data={
        "username": "admin",
        "password": "123456"
    })
    # Server trả về trang (200) và có thông báo thành công trong HTML
    assert res.status_code == 200
    assert b"Login successful!" in res.data

# Kiểm tra trường hợp đăng nhập thất bại với thông tin sai
def test_login_fail(client):
    # Gửi POST với username/password không đúng
    res = client.post("/", data={
        "username": "wrong",
        "password": "wrong"
    })
    # Server vẫn trả về trang (không redirect) nhưng hiển thị thông báo lỗi
    assert res.status_code == 200
    assert b"Invalid username or password!" in res.data

# Kiểm tra khi gửi các trường rỗng — ứng dụng hiện tại coi là đăng nhập thất bại
def test_empty_fields(client):
    # Gửi POST với cả username và password rỗng
    res = client.post("/", data={
        "username": "",
        "password": ""
    })
    # Mong đợi thông báo lỗi tương tự như khi thông tin không hợp lệ
    assert res.status_code == 200
    assert b"Invalid username or password!" in res.data

# Dùng parametrize để kiểm tra các trường hợp thiếu trường username/password hoặc cả hai
@pytest.mark.parametrize("form_data", [
    ({"username": "admin"}),          # thiếu password
    ({"password": "123456"}),         # thiếu username
    ({})                              # thiếu cả hai
])
def test_missing_fields(client, form_data):
    # Gửi POST với dữ liệu biến đổi từ parametrize
    res = client.post("/", data=form_data)
    # Ứng dụng hiện tại trả về thông báo lỗi khi thiếu trường
    assert res.status_code == 200
    assert b"Invalid username or password!" in res.data
