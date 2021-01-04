import json
import random

import pkg_resources
from flask import current_app

from .base import client


def test_get(client):
    assert client.get("/project/1").status_code == 401
    assert client.get("/project").status_code == 401
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    assert client.get("/project/1").json["name"] == "project1"
    assert client.get("/project/2").json["name"] == "project2"
    assert client.get("/project/3").status_code == 403
    assert client.get("/project/4").status_code == 404
    assert len(client.get("/project").json["projects"]) == 2


def test_create(client):
    # 创建失败（未登录）
    assert (
        client.post("/project", data={"name": "project", "tag": "123"}).status_code
        == 401
    )
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
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
    # 修改失败（未登录）
    assert (
        client.put("/project/1", data={"name": "project3", "tag": "123"}).status_code
        == 401
    )
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    # 修改失败（项目不存在）
    assert (
        client.put("/project/10", data={"name": "project3", "tag": "123"}).status_code
        == 404
    )
    # 修改失败（项目不属于你）
    assert (
        client.put("/project/3", data={"name": "project3", "tag": "123"}).status_code
        == 403
    )
    # 修改失败（项目重名）
    assert (
        client.put("/project/1", data={"name": "project1", "tag": "123"}).status_code
        == 400
    )
    # 修改成功
    assert (
        client.put("/project/1", data={"name": "project3", "tag": "123"}).status_code
        == 200
    )
    assert client.get("/project/1").json["name"] == "project3"


def test_delete(client):
    # 删除失败（未登录）
    assert (
        client.delete("/project/1", data={"name": "project3", "tag": "123"}).status_code
        == 401
    )
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    # 删除失败（项目不存在）
    assert (
        client.delete(
            "/project/10", data={"name": "project3", "tag": "123"}
        ).status_code
        == 404
    )
    # 删除失败（项目不属于你）
    assert (
        client.delete("/project/3", data={"name": "project3", "tag": "123"}).status_code
        == 403
    )
    # 删除成功
    assert client.delete("/project/1").status_code == 204
    assert client.get("/project/1").status_code == 404


def test_run(client):
    # 运行失败（未登录）
    assert client.post("/project/2/run").status_code == 401
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    # 运行失败（项目不属于你）
    assert client.post("/project/3/run").status_code == 403
    # 运行失败（项目有多个部分）
    res = client.post("/project", data={"name": str(random.random()), "tag": "test"})
    assert res.status_code == 201
    project_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "input_node"}
    )
    assert res.status_code == 201
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "input_node"}
    )
    assert res.status_code == 201
    assert (
        "Project has multiple graph"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
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
    assert (
        "Graph have cycle"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
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
    assert (
        "Graph have cycle"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
    assert (
        "Graph have cycle"
        in client.post("/node/{}/run".format(node3_id)).json["message"]
    )
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
    assert (
        "not support"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
    assert "not support" in client.post("/node/{}/run".format(node_id)).json["message"]
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
    assert (
        client.put(
            "/node/{}".format(node1_id),
            data={
                "extra": json.dumps(
                    {"has_header": False, "x_input_file": 1, "y_input_file": 2}
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
    assert (
        "not support input"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
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
                    {"has_header": False, "x_input_file": 1, "y_input_file": 2}
                )
            },
        ).status_code
        == 200
    )
    assert (
        client.put(
            "/node/{}".format(node2_id),
            data={
                "extra": json.dumps(
                    {"has_header": False, "x_input_file": 1, "y_input_file": 2}
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
    assert (
        "only allow"
        in client.post("/project/{}/run".format(project_id)).json["message"]
    )
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
    assert client.post("/project/{}/run".format(project_id)).status_code == 400
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
        res = client.post("/file", data={"file": f, "project_id": project_id})
        assert res.status_code == 201
        file1_id = res.json["id"]
    with open(pkg_resources.resource_filename("tests.files", "y1.csv"), "rb") as f:
        res = client.post("/file", data={"file": f, "project_id": project_id})
        assert res.status_code == 201
        file2_id = res.json["id"]
    assert (
        client.put(
            "/node/{}".format(node_id),
            data={
                "extra": json.dumps(
                    {
                        "has_header": False,
                        "x_input_file": file1_id,
                        "y_input_file": file2_id,
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
