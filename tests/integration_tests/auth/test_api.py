import pytest

@pytest.mark.parametrize("email, password, reg_status, pwd_login, login_status, me_status", [
    ('user_one@gmail.com', '987', 200, '987', 200, 200),
    ('kot@pes.com', '1234', 400, '1234', 200, 200),
    ('user_two@ya.ru.com', '1234', 200, '569', 401, 401),
    ('user_three@mail.ru', '1234', 200, '1234', 200, 200),
])
async def test_flow_auth(
    email: str, password: str, reg_status: int, pwd_login: str, login_status: int, me_status: int,
    ac
):
    #/register
    response_reg = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_reg.status_code == reg_status
    if response_reg.status_code == 200:
        assert response_reg.json() == {"status": "ok"}

    #/login
    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": pwd_login,
        }
    )
    assert response_login.status_code == login_status
    if response_login.status_code == 200:
        assert response_login
        assert ac.cookies["access_token"]
        assert "access_token" in response_login.json()

    # /me
    response_me = await ac.get(
        "/auth/me"
    )
    user = response_me.json()
    assert response_me.status_code == me_status
    if response_me.status_code == 200:
        assert user["email"] == email
        assert "id" in user
        assert "password" not in user
        assert "hashed_password" not in user

    # /logout
    response_logout = await ac.put(
        "/auth/logout"
    )
    assert response_logout.status_code == 200

    # /me after logout
    response_me_after_logout = await ac.get(
        "/auth/me"
    )
    assert response_me_after_logout.status_code == 401
    assert "access_token" not in ac.cookies

