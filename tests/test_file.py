import os
import tempfile

from flask import current_app

from app.models.project import Project
from app.models.user import User

from .base import client


def test_get(client):
    User.create(username="user1", password="123")
    User.create(username="user2", password="123")
    Project.create(user_id=1, name="123")
    Project.create(user_id=2, name="123")
    file_path = "{}/1.test".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(os.urandom(128))
    client.post("/session", data={"username": "user1", "password": "123"})
    with open(file_path, "rb") as f:
        client.post("/file", data={"file": f, "project_id": 1, "dir": "/"})
    client.delete("/session")
    # 未登录
    assert client.get("/file", data={"project_id": 1}).status_code == 401
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    assert (
        len(client.get("/file", data={"project_id": 1, "dir": "/"}).json["data"]) == 1
    )
    assert (
        client.get("/file", data={"project_id": 1, "dir": "/abc"}).json["message"]
        == "Path not found"
    )
    assert (
        client.get("/file", data={"project_id": 1, "dir": "/1.test"}).json["message"]
        == "Path not a directory"
    )
    assert client.get("/file", data={"project_id": -1, "dir": "/"}).status_code == 404
    assert client.get("/file", data={"project_id": 2, "dir": "/"}).status_code == 403
    assert (
        client.get("/file", data={"project_id": 1, "dir": "/../"}).json["message"]
        == "Path not belong you"
    )


def test_create(client):
    User.create(username="user1", password="123")
    User.create(username="user2", password="123")
    Project.create(user_id=1, name="123")
    Project.create(user_id=2, name="123")
    file_path = "{}/1.a".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(bytes("123", encoding="utf8"))
    # 上传文件失败（未登录）
    with open(file_path, "rb") as f:
        assert (
            client.post("/file", data={"file": f, "project_id": 2}).status_code == 401
        )
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 上传文件失败（项目不存在）
    with open(file_path, "rb") as f:
        assert (
            client.post(
                "/file", data={"file": f, "project_id": -1, "dir": "/"}
            ).status_code
            == 404
        )
    # 上传文件失败（项目不属于你）
    with open(file_path, "rb") as f:
        assert (
            client.post(
                "/file", data={"file": f, "project_id": 2, "dir": "/"}
            ).status_code
            == 403
        )
    # 上传文件失败（文件路径错误）
    with open(file_path, "rb") as f:
        assert (
            client.post(
                "/file", data={"file": f, "project_id": 1, "dir": "/../"}
            ).status_code
            == 400
        )
    # 上传文件成功
    with open(file_path, "rb") as f:
        assert (
            client.post(
                "/file", data={"file": f, "project_id": 1, "dir": "/"}
            ).status_code
            == 201
        )
    assert (
        client.get("/file", data={"project_id": 1, "dir": "/"}).json["data"][0]["name"]
        == "1.a"
    )
    assert os.path.exists("{}/1/user/1.a".format(current_app.config["FILE_DIRECTORY"]))
    size = client.get("/file", data={"project_id": 1, "dir": "/"}).json["data"][0][
        "size"
    ]
    # 修改文件
    with open(file_path, "wb") as f:
        f.write(bytes("1234", encoding="utf8"))
    # 覆盖文件
    with open(file_path, "rb") as f:
        assert (
            client.post(
                "/file", data={"file": f, "project_id": 1, "dir": "/"}
            ).status_code
            == 201
        )
    assert (
        client.get("/file", data={"project_id": 1, "dir": "/"}).json["data"][0]["name"]
        == "1.a"
    )
    assert os.path.exists("{}/1/user/1.a".format(current_app.config["FILE_DIRECTORY"]))
    assert (
        client.get("/file", data={"project_id": 1, "dir": "/"}).json["data"][0]["size"]
        > size
    )


def test_modify(client):
    User.create(username="user1", password="123")
    User.create(username="user2", password="123")
    Project.create(user_id=1, name="123")
    Project.create(user_id=2, name="123")
    file_path = "{}/1.test".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(os.urandom(128))
    client.post("/session", data={"username": "user1", "password": "123"})
    with open(file_path, "rb") as f:
        client.post("/file", data={"file": f, "project_id": 1, "dir": "/"})
    client.delete("/session")
    file_path = "{}/1.test".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(os.urandom(128))
    client.post("/session", data={"username": "user2", "password": "123"})
    with open(file_path, "rb") as f:
        client.post("/file", data={"file": f, "project_id": 2})
    client.delete("/session")
    # 修改文件失败（未登录）
    assert (
        client.put(
            "/file",
            data={"old_filename": "1.a", "new_filename": "1.b", "project_id": 1},
        ).status_code
        == 401
    )
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 修改文件失败（项目不属于你）
    assert (
        client.put(
            "/file",
            data={"old_filename": "/1.a", "new_filename": "/1.b", "project_id": 2},
        ).status_code
        == 403
    )
    # 修改文件失败（文件不存在）
    assert (
        client.put(
            "/file",
            data={"old_filename": "/1.aaa", "new_filename": "/1.b", "project_id": 1},
        ).status_code
        == 404
    )
    # 修改文件失败（目标文件已存在）
    assert (
        client.put(
            "/file",
            data={
                "old_filename": "/1.test",
                "new_filename": "/1.test",
                "project_id": 1,
            },
        ).status_code
        == 400
    )
    # 修改文件失败（文件路径错误）
    assert (
        client.put(
            "/file",
            data={
                "old_filename": "/../1.test",
                "new_filename": "/1.a",
                "project_id": 1,
            },
        ).status_code
        == 400
    )
    # 修改文件成功
    assert (
        client.put(
            "/file",
            data={"old_filename": "/1.test", "new_filename": "/1.c", "project_id": 1},
        ).status_code
        == 200
    )
    assert (
        client.get("/file", data={"project_id": 1, "dir": "/"}).json["data"][0]["name"]
        == "1.c"
    )
    assert os.path.exists("{}/1/user/1.c".format(current_app.config["FILE_DIRECTORY"]))


def test_delete(client):
    User.create(username="user1", password="123")
    User.create(username="user2", password="123")
    Project.create(user_id=1, name="123")
    Project.create(user_id=2, name="123")
    file_path = "{}/1.test".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(os.urandom(128))
    client.post("/session", data={"username": "user1", "password": "123"})
    with open(file_path, "rb") as f:
        client.post("/file", data={"file": f, "project_id": 1, "dir": "/"})
    client.delete("/session")
    file_path = "{}/1.test".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(os.urandom(128))
    client.post("/session", data={"username": "user2", "password": "123"})
    with open(file_path, "rb") as f:
        client.post("/file", data={"file": f, "project_id": 2, "dir": "/"})
    client.delete("/session")
    # 删除文件失败（用户未登录）
    assert (
        client.delete("/file", data={"filename": "1.a", "project_id": 1}).status_code
        == 401
    )
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 删除文件失败（文件不存在）
    assert (
        client.delete("/file", data={"filename": "/1.aaa", "project_id": 1}).status_code
        == 404
    )
    # 删除文件失败（项目不属于你）
    assert (
        client.delete("/file", data={"filename": "/1.a", "project_id": 2}).status_code
        == 403
    )
    # 删除文件失败（文件路径错误）
    assert (
        client.delete(
            "/file", data={"filename": "/../1.test", "project_id": 1}
        ).status_code
        == 400
    )
    # 删除文件失败（路径不是文件）
    assert (
        client.delete("/file", data={"filename": "/", "project_id": 1}).status_code
        == 400
    )
    # 删除文件成功
    assert (
        client.delete(
            "/file", data={"filename": "/1.test", "project_id": 1}
        ).status_code
        == 204
    )
    assert (
        len(client.get("/file", data={"project_id": 1, "dir": "/"}).json["data"]) == 0
    )
    assert (
        os.path.exists("{}/1/user/1.test".format(current_app.config["FILE_DIRECTORY"]))
        is False
    )


def test_directory_create(client):
    User.create(username="123", password="123")
    Project.create(user_id=1, name="123")
    # 未登录
    assert (
        client.post(
            "/file/directory", data={"project_id": 1, "dir": "/abc"}
        ).status_code
        == 401
    )
    # 登录
    client.post("/session", data={"username": "123", "password": "123"})
    # 创建失败（路径错误）
    assert (
        client.post("/file/directory", data={"project_id": 1, "dir": "/../abc"}).json[
            "message"
        ]
        == "Path not belong you"
    )
    # 创建失败（路径已存在）
    assert (
        client.post("/file/directory", data={"project_id": 1, "dir": "/"}).json[
            "message"
        ]
        == "Path already exist"
    )
    # 创建成功
    assert (
        client.post(
            "/file/directory", data={"project_id": 1, "dir": "/abc"}
        ).status_code
        == 201
    )
    assert os.path.exists("{}/1/user/abc".format(current_app.config["FILE_DIRECTORY"]))


def test_directory_delete(client):
    User.create(username="123", password="123")
    Project.create(user_id=1, name="123")
    # 未登录
    assert (
        client.delete(
            "/file/directory", data={"project_id": 1, "dir": "/abc"}
        ).status_code
        == 401
    )
    # 登录
    client.post("/session", data={"username": "123", "password": "123"})
    # 删除失败（删除根目录）
    assert (
        client.delete("/file/directory", data={"project_id": 1, "dir": "/"}).json[
            "message"
        ]
        == "Path is root directory"
    )
    # 删除失败（路径错误）
    assert (
        client.delete("/file/directory", data={"project_id": 1, "dir": "/../"}).json[
            "message"
        ]
        == "Path not belong you"
    )
    # 删除失败（路径不存在）
    assert (
        client.delete("/file/directory", data={"project_id": 1, "dir": "/abc"}).json[
            "message"
        ]
        == "Path not found"
    )
    # 删除失败（路径非文件夹）
    file_path = "{}/1.test".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(os.urandom(128))
    with open(file_path, "rb") as f:
        client.post("/file", data={"file": f, "project_id": 1, "dir": "/"})
    assert (
        client.delete("/file/directory", data={"project_id": 1, "dir": "/1.test"}).json[
            "message"
        ]
        == "Path not directory"
    )
    # 删除成功
    assert (
        client.post(
            "/file/directory", data={"project_id": 1, "dir": "/abc"}
        ).status_code
        == 201
    )
    assert (
        client.delete(
            "/file/directory", data={"project_id": 1, "dir": "/abc"}
        ).status_code
        == 204
    )
    assert (
        os.path.exists("{}/1/user/abc".format(current_app.config["FILE_DIRECTORY"]))
        is False
    )
