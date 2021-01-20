from app.models.user import User

from .base import client


def test_session(client):
    # 创建用户
    User.create(username="123", password="123")
    # 未登录
    assert client.get("/session").status_code == 401
    # 登录
    assert (
        client.post("/session", data={"username": "123", "password": "123"}).status_code
        == 201
    )
    assert client.get("/session").status_code == 200
    assert client.get("/session").json["username"] == "123"
    # 登出
    assert client.delete("/session").status_code == 204
    assert client.get("/session").status_code == 401
    # 失败的登录
    assert (
        client.post(
            "/session", data={"username": "123", "password": "123456"}
        ).status_code
        == 400
    )
    assert client.get("/session").status_code == 401
