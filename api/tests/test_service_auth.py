from service.auth import AuthService, verify_password, get_user_by_name

def test_get_user_by_name():
    user = get_user_by_name("alice")
    assert user is not None
    assert user.name == "alice"

def test_verify_password():
    user = get_user_by_name("alice")
    assert user is not None
    assert verify_password("wonderland", user.password) is True
    assert verify_password("wrongpassword", user.password) is False

def test_authenticate_user():
    assert AuthService.authenticate_user("alice", "wonderland") is True
    assert AuthService.authenticate_user("alice", "wrongpassword") is False
    assert AuthService.authenticate_user("unknown", "wonderland") is False

def test_is_admin():
    assert AuthService.is_admin("admin", "4dm1N") is True
    assert AuthService.is_admin("alice", "wonderland") is False
    assert AuthService.is_admin("admin", "wrongpassword") is False
