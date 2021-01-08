import random

import pkg_resources
from flask import current_app

from app.libs.global_varible import g
from app.models.node import Node
from app.models.project import Project

from .base import client


def test_get(client):
    assert client.get("/node/1").status_code == 401
    assert client.get("/node", data={"project_id": 1}).status_code == 401
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    assert client.get("/node/1").json["node_type"] == "123"
    assert client.get("/node/2").status_code == 403
    assert client.get("/node/-1").status_code == 404
    assert len(client.get("/node", data={"project_id": 1}).json["nodes"]) == 4
    assert client.get("/node", data={"project_id": -1}).status_code == 404
    assert client.get("/node", data={"project_id": 3}).status_code == 403


def test_create(client):
    # 创建节点失败（未登录）
    assert (
        client.post("/node", data={"project_id": 1, "node_type": "123"}).status_code
        == 401
    )
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    # 创建节点失败（项目不存在）
    assert (
        client.post("/node", data={"project_id": -1, "node_type": "123"}).status_code
        == 404
    )
    # 创建节点失败（项目不属于你）
    assert (
        client.post("/node", data={"project_id": 3, "node_type": "123"}).status_code
        == 403
    )
    # 创建节点成功
    res = client.post("/node", data={"project_id": 1, "node_type": "123"})
    assert res.status_code == 201
    id_ = res.json["id"]
    assert client.get("/node/{}".format(id_)).json["node_type"] == "123"


def test_modify(client):
    # 修改节点失败（未登录）
    assert client.put("/node/1", data={"extra": '{"a": "b"}'}).status_code == 401
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    # 修改节点失败（节点不存在）
    assert client.put("/node/-10", data={"extra": '{"a":"b"}'}).status_code == 404
    # 修改节点失败（项目不属于你）
    assert client.put("/node/2", data={"extra": '{"a": "b"}'}).status_code == 403
    # 修改节点失败（无法解析json）
    assert client.put("/node/1", data={"extra": '{"a": "b}'}).status_code == 400
    # 修改节点失败（解析后非dict）
    assert client.put("/node/1", data={"extra": "[0, 1, 2]"}).status_code == 400
    # 修改节点成功
    assert client.put("/node/1", data={"extra": '{"a": "b"}'}).status_code == 200
    assert client.get("/node/1").json["extra"] == {"a": "b"}


def test_delete(client):
    # 删除节点失败（未登录）
    assert client.delete("/node/1").status_code == 401
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    # 删除节点失败（节点不存在）
    assert client.delete("/node/-1").status_code == 404
    # 删除节点失败（项目不属于你）
    assert client.delete("/node/2").status_code == 403
    # 删除节点成功
    assert client.delete("/node/1").status_code == 204
    assert client.get("/node/1").status_code == 404


def test_edge_create(client):
    # 创建边失败（未登录）
    assert (
        client.post(
            "/node/edge", data={"project_id": 1, "node1_id": 1, "node2_id": 3}
        ).status_code
        == 401
    )
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    # 创建边失败（项目不存在）
    assert (
        client.post(
            "/node/edge", data={"project_id": -1, "node1_id": 1, "node2_id": 3}
        ).status_code
        == 404
    )
    # 创建边失败（项目不属于你）
    assert (
        client.post(
            "/node/edge", data={"project_id": 3, "node1_id": 1, "node2_id": 3}
        ).status_code
        == 403
    )
    # 创建边失败（节点不存在）
    assert (
        client.post(
            "/node/edge", data={"project_id": 2, "node1_id": 1, "node2_id": -1}
        ).status_code
        == 400
    )
    assert (
        client.post(
            "/node/edge", data={"project_id": 2, "node1_id": -1, "node2_id": 1}
        ).status_code
        == 400
    )
    # 创建边失败（节点不属于该项目）
    assert (
        client.post(
            "/node/edge", data={"project_id": 1, "node1_id": 1, "node2_id": 2}
        ).status_code
        == 403
    )
    assert (
        client.post(
            "/node/edge", data={"project_id": 1, "node1_id": 2, "node2_id": 1}
        ).status_code
        == 403
    )
    # 创建边失败（边已存在）
    assert (
        client.post(
            "/node/edge", data={"project_id": 1, "node1_id": 1, "node2_id": 3}
        ).status_code
        == 400
    )
    # 创建成功
    assert (
        client.post(
            "/node/edge", data={"project_id": 1, "node1_id": 3, "node2_id": 4}
        ).status_code
        == 201
    )
    assert client.get("/node/1").json["out_edges"].count(4) == 1
    assert client.get("/node/4").json["in_edges"].count(1) == 1


def test_edge_delete(client):
    # 删除边失败（未登录）
    assert (
        client.delete(
            "/node/edge", data={"project_id": 1, "node1_id": 1, "node2_id": 3}
        ).status_code
        == 401
    )
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    # 删除边失败（项目不存在）
    assert (
        client.delete(
            "/node/edge", data={"project_id": -1, "node1_id": 1, "node2_id": 3}
        ).status_code
        == 404
    )
    # 删除边失败（项目不属于你）
    assert (
        client.delete(
            "/node/edge", data={"project_id": 3, "node1_id": 1, "node2_id": 3}
        ).status_code
        == 403
    )
    # 删除边失败（节点不存在）
    assert (
        client.delete(
            "/node/edge", data={"project_id": 2, "node1_id": 1, "node2_id": -1}
        ).status_code
        == 400
    )
    assert (
        client.delete(
            "/node/edge", data={"project_id": 2, "node1_id": -1, "node2_id": 1}
        ).status_code
        == 400
    )
    # 删除边失败（节点不属于该项目）
    assert (
        client.delete(
            "/node/edge", data={"project_id": 1, "node1_id": 1, "node2_id": 2}
        ).status_code
        == 403
    )
    assert (
        client.delete(
            "/node/edge", data={"project_id": 1, "node1_id": 2, "node2_id": 1}
        ).status_code
        == 403
    )
    # 删除边失败（边不存在）
    assert (
        client.delete(
            "/node/edge", data={"project_id": 1, "node1_id": 3, "node2_id": 4}
        ).status_code
        == 400
    )
    # 删除成功
    assert (
        client.delete(
            "/node/edge", data={"project_id": 1, "node1_id": 1, "node2_id": 3}
        ).status_code
        == 204
    )
    assert client.get("/node/1").json["out_edges"].count(3) == 0
    assert client.get("/node/3").json["in_edges"].count(1) == 0


def test_csv(client):
    # 读取csv失败（未登录）
    assert client.get("/node/1/csv").status_code == 401
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    # 读取csv失败（节点不存在）
    assert client.get("/node/-1/csv").status_code == 404
    # 读取csv失败（项目不属于你）
    assert client.get("/node/2/csv").status_code == 403
    # 读取csv失败（文件不存在）
    assert (
        "File not found"
        in client.get("/node/1/csv", data={"filename": "x.csv"}).json["message"]
    )
    # 复制文件
    with open(pkg_resources.resource_filename("tests.files", "x1.csv"), "rb") as f:
        data = f.read()
    with open(
        "./{}/1/node/1/x.csv".format(current_app.config["FILE_DIRECTORY"]), "wb"
    ) as f:
        f.write(data)
    # 读取csv成功
    assert client.get("/node/1/csv", data={"filename": "x.csv"}).status_code == 200


def test_status(client):
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 创建项目
    project = Project.create(name=str(random.random()), tag="", user_id=1)
    # 上传文件
    with open(pkg_resources.resource_filename("tests.files", "telco.csv"), "rb") as f:
        file_id = client.post("/file", data={"file": f, "project_id": project.id}).json[
            "id"
        ]
    # 创建节点
    node1 = Node.create(
        project_id=project.id,
        node_type="not_split_input_node",
        extra={"has_header": True, "input_file": file_id, "label_columns": "100"},
    )
    node2 = Node.create(
        project_id=project.id,
        node_type="data_split_node",
        extra={"test_ratio": 0.2, "random_state": 888},
    )
    node3 = Node.create(
        project_id=project.id,
        node_type="classifier_node",
        extra={"model": "LogisticRegression", "model_kwargs": {"max_iter": 10000}},
    )
    # 创建边
    client.post(
        "/node/edge",
        data={
            "project_id": project.id,
            "node1_id": node1.id,
            "node2_id": node2.id,
        },
    )
    client.post(
        "/node/edge",
        data={
            "project_id": project.id,
            "node1_id": node2.id,
            "node2_id": node3.id,
        },
    )
    # 训练
    current_app.config["THREAD"] = True
    node3.run()
    # 等待线程结束
    if getattr(g, "thread_list", None):
        for thread in g.thread_list:
            thread.join()
        g.thread_list = None
    # 查看运行状态
    assert node1.status == Node.Status.FAILED
    assert node2.status == Node.Status.FAILED
    assert node3.status == Node.Status.FAILED


def test_description(client):
    res = client.get("/node/description").json
    assert isinstance(res["data"], list)
    assert isinstance(res["data"][0], dict)
    assert isinstance(res["data"][0]["params"], list)
    assert isinstance(res["data"][0]["params"][0], dict)
