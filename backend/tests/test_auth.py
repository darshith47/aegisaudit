def test_register_and_login_user(client):
    # Test Registration
    reg_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "auditor_sec",
            "email": "sec@aegisaudit.com",
            "password": "SecurePassword2026!",
            "role": "auditor"
        }
    )
    assert reg_response.status_code == 201
    assert reg_response.json()["username"] == "auditor_sec"

    # Test Login
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "auditor_sec", "password": "SecurePassword2026!"}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Test Me endpoint
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token_data['access_token']}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "auditor_sec"
