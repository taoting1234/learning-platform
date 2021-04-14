from flask import current_app, session

from app.models.invitation_code import InvitationCode
from app.models.user import User

from .base import client


def test_get(client):
    User.create(username="admin", password="admin", permission=1)
    User.create(username="user", password="user", permission=0)
    # 未登录
    assert client.get("/user/1").status_code == 401
    # 登录管理员
    client.post("/session", data={"username": "admin", "password": "admin"})
    assert client.get("/user/1").json["username"] == "admin"
    assert client.get("/user/2").json["username"] == "user"
    assert client.get("/user/3").status_code == 404
    # 登录普通用户
    client.post("/session", data={"username": "user", "password": "user"})
    assert client.get("/user/1").status_code == 403
    assert client.get("/user/2").json["username"] == "user"
    assert client.get("/user/3").status_code == 404


def test_create(client):
    User.create(username="user1", password="123")
    client.post("/session", data={"username": "user1", "password": "123"})
    code = InvitationCode.create().code
    current_app.config["TESTING"] = False
    # 验证码错误
    assert client.get("/captcha").status_code == 200
    assert (
        "Captcha wrong"
        in client.post(
            "/user",
            data={
                "username": "user1",
                "password": "123",
                "organization": "123",
                "captcha": "",
                "code": "",
            },
        ).json["message"]
    )
    # 用户已存在
    assert client.get("/captcha").status_code == 200
    assert (
        "User already exist"
        in client.post(
            "/user",
            data={
                "username": "user1",
                "password": "123",
                "organization": "123",
                "captcha": session["captcha"],
                "code": "",
            },
        ).json["message"]
    )
    # 邀请码错误
    assert client.get("/captcha").status_code == 200
    assert (
        "Invitation code wrong"
        in client.post(
            "/user",
            data={
                "username": "user",
                "password": "user",
                "organization": "123",
                "captcha": session["captcha"],
                "code": "",
            },
        ).json["message"]
    )
    # 创建用户成功
    assert client.get("/captcha").status_code == 200
    res = client.post(
        "/user",
        data={
            "username": "user",
            "password": "user",
            "organization": "123",
            "captcha": session["captcha"],
            "code": code,
        },
    )
    assert res.status_code == 201
    id_ = res.json["id"]
    current_app.config["TESTING"] = True
    # 登录
    assert client.post("/session", data={"username": "user", "password": "user"}).status_code == 201
    assert client.get("/user/{}".format(id_)).json["username"] == "user"


def test_modify(client):
    User.create(username="user1", password="123")
    User.create(username="user2", password="123")
    # 修改用户失败（未登录）
    assert client.delete("/session").status_code == 204
    assert client.put("/user/1", data={"password": "user", "old_password": "user"}).status_code == 401
    # 修改用户失败（登录其他人）
    assert client.post("/session", data={"username": "user2", "password": "123"}).status_code == 201
    assert client.put("/user/1", data={"password": "user", "old_password": "user"}).status_code == 403
    # 修改用户失败（密码错误）
    assert client.post("/session", data={"username": "user1", "password": "123"}).status_code == 201
    assert client.put("/user/1", data={"password": "user", "old_password": "user"}).status_code == 400
    assert client.put("/user/1", data={"password": "user", "old_password": ""}).status_code == 400
    # 修改成功
    assert client.put("/user/1", data={"password": "user", "old_password": "123"}).status_code == 200
    assert client.post("/session", data={"username": "user1", "password": "123"}).status_code == 400
    assert client.post("/session", data={"username": "user1", "password": "user"}).status_code == 201


def test_search(client):
    User.create(username="admin", password="admin", permission=1)
    User.create(username="user", password="user", permission=0)
    # 未登录
    assert client.get("/user", data={"permission": 1}).status_code == 401
    # 登录管理员
    client.post("/session", data={"username": "admin", "password": "admin"})
    assert len(client.get("/user", data={"permission": 1}).json["data"]) == 1
    # 登录普通用户
    client.post("/session", data={"username": "user", "password": "user"})
    assert client.get("/user", data={"permission": 1}).status_code == 403
