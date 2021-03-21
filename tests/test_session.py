from flask import session

from app.models.user import User

from .base import client


def test_session(client):
    # 创建用户
    User.create(username="123", password="123")
    User.create(username="1234", password="1234", block=True)
    # 未登录
    assert client.get("/session").status_code == 401
    # 获取验证码
    assert client.get("/captcha").status_code == 200
    # 验证码错误
    assert (
        "Captcha wrong"
        in client.post(
            "/session", data={"username": "123", "password": "123", "captcha": ""}
        ).json["message"]
    )
    # 获取验证码
    assert client.get("/captcha").status_code == 200
    # 密码错误
    assert (
        "Username or password wrong"
        in client.post(
            "/session",
            data={
                "username": "123",
                "password": "123456",
                "captcha": session["captcha"],
            },
        ).json["message"]
    )
    # 获取验证码
    assert client.get("/captcha").status_code == 200
    # 用户被封禁
    assert (
        "User is blocked"
        in client.post(
            "/session",
            data={
                "username": "1234",
                "password": "1234",
                "captcha": session["captcha"],
            },
        ).json["message"]
    )
    # 获取验证码
    assert client.get("/captcha").status_code == 200
    # 登录
    assert (
        client.post(
            "/session",
            data={"username": "123", "password": "123", "captcha": session["captcha"]},
        ).status_code
        == 201
    )
    assert client.get("/session").status_code == 200
    assert client.get("/session").json["username"] == "123"
    # 登出
    assert client.delete("/session").status_code == 204
    assert client.get("/session").status_code == 401
