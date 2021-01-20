import json
import os
import random
import tempfile

import pkg_resources
from flask import current_app

from app.libs.global_varible import g
from app.models.project import Project
from app.models.user import User

from .base import client


def test_get(client):
    User.create(username="admin", password="admin", permission=1)
    User.create(username="user", password="user", permission=0)
    Project.create(user_id=1, name="test")
    Project.create(user_id=2, name="test")
    # 未登录
    assert client.get("/project/1").status_code == 401
    # 登录管理员
    client.post("/session", data={"username": "admin", "password": "admin"})
    assert client.get("/project/1").json["name"] == "test"
    assert client.get("/project/2").json["name"] == "test"
    assert client.get("/project/3").status_code == 404
    # 登录普通用户
    client.post("/session", data={"username": "user", "password": "user"})
    assert client.get("/project/1").status_code == 403
    assert client.get("/project/2").json["name"] == "test"
    assert client.get("/project/3").status_code == 404


def test_create(client):
    User.create(username="user1", password="123")
    Project.create(user_id=1, name="project1")
    # 创建失败（未登录）
    assert (
        client.post("/project", data={"name": "project", "tag": "123"}).status_code
        == 401
    )
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 创建失败（重名）
    assert (
        client.post("/project", data={"name": "project1", "tag": "123"}).status_code
        == 400
    )
    # 创建成功
    res = client.post("/project", data={"name": "project", "tag": "123"})
    assert res.status_code == 201
    id_ = res.json["id"]
    assert client.get("/project/{}".format(id_)).json["name"] == "project"


def test_modify(client):
    User.create(username="user1", password="123")
    User.create(username="user2", password="123")
    Project.create(user_id=1, name="project1")
    Project.create(user_id=1, name="project2")
    Project.create(user_id=2, name="project3")
    # 修改失败（未登录）
    assert (
        client.put("/project/1", data={"name": "project3", "tag": "123"}).status_code
        == 401
    )
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 修改失败（项目不存在）
    assert (
        client.put("/project/-1", data={"name": "project3", "tag": "123"}).status_code
        == 404
    )
    # 修改失败（项目不属于你）
    assert (
        client.put("/project/3", data={"name": "project3", "tag": "123"}).status_code
        == 403
    )
    # 修改失败（项目重名）
    assert (
        client.put("/project/1", data={"name": "project2", "tag": "123"}).status_code
        == 400
    )
    # 修改成功
    assert (
        client.put("/project/1", data={"name": "project3", "tag": "123"}).status_code
        == 200
    )
    assert client.get("/project/1").json["name"] == "project3"


def test_delete(client):
    User.create(username="user1", password="123")
    User.create(username="user2", password="123")
    Project.create(user_id=1, name="project1")
    Project.create(user_id=2, name="project2")
    # 删除失败（未登录）
    assert (
        client.delete("/project/1", data={"name": "project3", "tag": "123"}).status_code
        == 401
    )
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 删除失败（项目不存在）
    assert (
        client.delete(
            "/project/10", data={"name": "project3", "tag": "123"}
        ).status_code
        == 404
    )
    # 删除失败（项目不属于你）
    assert (
        client.delete("/project/2", data={"name": "project3", "tag": "123"}).status_code
        == 403
    )
    # 删除成功
    assert client.delete("/project/1").status_code == 204
    assert client.get("/project/1").status_code == 404


def test_run(client):
    User.create(username="user1", password="123")
    User.create(username="user2", password="123")
    Project.create(user_id=2, name="project2")
    # 运行失败（未登录）
    assert client.post("/project/1/run").status_code == 401
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 运行失败（项目不属于你）
    assert client.post("/project/1/run").status_code == 403
    # 运行失败（项目有多个部分）
    project = Project.create(user_id=1, name="123")
    client.post("/node", data={"project_id": project.id, "node_type": "input_node"})
    client.post("/node", data={"project_id": project.id, "node_type": "input_node"})
    current_app.config["TESTING"] = False
    assert (
        "Project has multiple graph"
        in client.post("/project/{}/run".format(project.id)).json["message"]
    )
    current_app.config["TESTING"] = True
    # 运行失败（项目有环）
    res = client.post("/project", data={"name": str(random.random()), "tag": "test"})
    assert res.status_code == 201
    project_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "input_node"}
    )
    assert res.status_code == 201
    node1_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "input_node"}
    )
    assert res.status_code == 201
    node2_id = res.json["id"]
    assert (
        client.post(
            "/node/edge",
            data={"project_id": project_id, "node1_id": node1_id, "node2_id": node2_id},
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/node/edge",
            data={"project_id": project_id, "node1_id": node2_id, "node2_id": node1_id},
        ).status_code
        == 201
    )
    current_app.config["TESTING"] = False
    assert (
        "Graph have cycle"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
    current_app.config["TESTING"] = True
    # 运行失败（项目部分有环）
    res = client.post("/project", data={"name": str(random.random()), "tag": "test"})
    assert res.status_code == 201
    project_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "input_node"}
    )
    assert res.status_code == 201
    node1_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "input_node"}
    )
    assert res.status_code == 201
    node2_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "input_node"}
    )
    assert res.status_code == 201
    node3_id = res.json["id"]
    assert (
        client.post(
            "/node/edge",
            data={"project_id": project_id, "node1_id": node1_id, "node2_id": node2_id},
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/node/edge",
            data={"project_id": project_id, "node1_id": node2_id, "node2_id": node1_id},
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/node/edge",
            data={"project_id": project_id, "node1_id": node2_id, "node2_id": node3_id},
        ).status_code
        == 201
    )
    current_app.config["TESTING"] = False
    assert (
        "Graph have cycle"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
    assert (
        "Graph have cycle"
        in client.post("/node/{}/run".format(node3_id)).json["message"]
    )
    current_app.config["TESTING"] = True
    # 运行失败（项目有无效节点）
    res = client.post("/project", data={"name": str(random.random()), "tag": "test"})
    assert res.status_code == 201
    project_id = res.json["id"]
    res = client.post("/node", data={"project_id": project_id, "node_type": "123"})
    assert res.status_code == 201
    node_id = res.json["id"]
    assert (
        client.put(
            "/node/{}".format(node_id),
            data={"extra": '{"x_input_file":1, "y_input_file":1}'},
        ).status_code
        == 200
    )
    current_app.config["TESTING"] = False
    assert (
        "not support"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
    assert "not support" in client.post("/node/{}/run".format(node_id)).json["message"]
    current_app.config["TESTING"] = True
    # 运行失败（输入数量错误）
    res = client.post("/project", data={"name": str(random.random()), "tag": "test"})
    assert res.status_code == 201
    project_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "split_input_node"}
    )
    assert res.status_code == 201
    node1_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "regressor_node"}
    )
    assert res.status_code == 201
    node2_id = res.json["id"]
    assert client.post(
        "/node/edge",
        data={"project_id": project_id, "node1_id": node1_id, "node2_id": node2_id},
    )
    file_path = "{}/1.test".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(os.urandom(128))
    with open(file_path, "rb") as f:
        client.post("/file", data={"file": f, "project_id": project_id})
    assert (
        client.put(
            "/node/{}".format(node1_id),
            data={
                "extra": json.dumps(
                    {
                        "has_header": False,
                        "x_input_file": "1.test",
                        "y_input_file": "1.test",
                    }
                )
            },
        ).status_code
        == 200
    )
    assert (
        client.put(
            "/node/{}".format(node2_id),
            data={"extra": json.dumps({"model": "LinearRegression"})},
        ).status_code
        == 200
    )
    current_app.config["TESTING"] = False
    assert (
        "not support input"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
    current_app.config["TESTING"] = True
    # 运行失败（输入节点错误）
    res = client.post("/project", data={"name": str(random.random()), "tag": "test"})
    assert res.status_code == 201
    project_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "split_input_node"}
    )
    assert res.status_code == 201
    node1_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "split_input_node"}
    )
    assert res.status_code == 201
    node2_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "regressor_node"}
    )
    assert res.status_code == 201
    node3_id = res.json["id"]
    assert client.post(
        "/node/edge",
        data={"project_id": project_id, "node1_id": node1_id, "node2_id": node3_id},
    )
    assert client.post(
        "/node/edge",
        data={"project_id": project_id, "node1_id": node2_id, "node2_id": node3_id},
    )
    assert (
        client.put(
            "/node/{}".format(node1_id),
            data={
                "extra": json.dumps(
                    {
                        "has_header": False,
                        "x_input_file": "1.test",
                        "y_input_file": "1.test",
                    }
                )
            },
        ).status_code
        == 200
    )
    file_path = "{}/1.test".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(os.urandom(128))
    with open(file_path, "rb") as f:
        client.post("/file", data={"file": f, "project_id": project_id})
    assert (
        client.put(
            "/node/{}".format(node2_id),
            data={
                "extra": json.dumps(
                    {
                        "has_header": False,
                        "x_input_file": "1.test",
                        "y_input_file": "1.test",
                    }
                )
            },
        ).status_code
        == 200
    )
    assert (
        client.put(
            "/node/{}".format(node3_id),
            data={"extra": json.dumps({"model": "LinearRegression"})},
        ).status_code
        == 200
    )
    current_app.config["TESTING"] = False
    assert (
        "only allow"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
    current_app.config["TESTING"] = True
    # 运行成功（运行节点报错）
    res = client.post("/project", data={"name": str(random.random()), "tag": "test"})
    assert res.status_code == 201
    project_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "input_node"}
    )
    assert res.status_code == 201
    node_id = res.json["id"]
    assert (
        client.put(
            "/node/{}".format(node_id),
            data={"extra": json.dumps({"x_input_file": 1, "y_input_file": 1})},
        ).status_code
        == 200
    )
    current_app.config["TESTING"] = False
    assert client.post("/project/{}/run".format(project_id)).status_code == 400
    current_app.config["TESTING"] = True
    # 运行成功
    res = client.post("/project", data={"name": str(random.random()), "tag": "test"})
    assert res.status_code == 201
    project_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "split_input_node"}
    )
    assert res.status_code == 201
    node_id = res.json["id"]
    with open(pkg_resources.resource_filename("tests.files", "x1.csv"), "rb") as f:
        client.post("/file", data={"file": f, "project_id": project_id})
    with open(pkg_resources.resource_filename("tests.files", "y1.csv"), "rb") as f:
        client.post("/file", data={"file": f, "project_id": project_id})
    assert (
        client.put(
            "/node/{}".format(node_id),
            data={
                "extra": json.dumps(
                    {
                        "has_header": False,
                        "x_input_file": "x1.csv",
                        "y_input_file": "y1.csv",
                    }
                )
            },
        ).status_code
        == 200
    )
    assert client.post("/project/{}/run".format(project_id)).status_code == 201
    assert client.post("/node/{}/run".format(node_id)).status_code == 201
    # 运行成功（线程）
    current_app.config["THREAD"] = True
    assert client.post("/project/{}/run".format(project_id)).status_code == 201
    # 等待线程结束
    if getattr(g, "thread_list", None):
        for thread in g.thread_list:
            thread.join()
        g.thread_list = None


def test_search(client):
    User.create(username="admin", password="admin", permission=1)
    User.create(username="user", password="user", permission=0)
    # 未登录
    assert client.get("/project", data={"user_id": 1}).status_code == 401
    # 登录管理员
    client.post("/session", data={"username": "admin", "password": "admin"})
    assert len(client.get("/project", data={"user_id": 2}).json["data"]) == 0
    # 登录普通用户
    client.post("/session", data={"username": "user", "password": "user"})
    assert client.get("/project", data={"user_id": 1}).status_code == 403
    assert len(client.get("/project", data={"user_id": 2}).json["data"]) == 0
