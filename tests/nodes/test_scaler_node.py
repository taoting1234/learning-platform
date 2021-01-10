import random

import pkg_resources

from app.models.node import Node
from app.models.project import Project

from ..base import client


def test_scaler_node(client):
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 创建项目
    project = Project.create(name=str(random.random()), tag="", user_id=1)
    # 上传文件
    with open(pkg_resources.resource_filename("tests.files", "x1.csv"), "rb") as f:
        client.post("/file", data={"file": f, "project_id": project.id})
    with open(pkg_resources.resource_filename("tests.files", "y1.csv"), "rb") as f:
        client.post("/file", data={"file": f, "project_id": project.id})
    # 创建节点
    node1 = Node.create(
        project_id=project.id,
        node_type="split_input_node",
        extra={"has_header": False, "x_input_file": "x1.csv", "y_input_file": "y1.csv"},
    )
    node2 = Node.create(
        project_id=project.id,
        node_type="data_split_node",
        extra={"test_ratio": 0.2, "random_state": 888},
    )
    node3 = Node.create(
        project_id=project.id,
        node_type="scaler_node",
        extra={"include_label": True, "model": "StandardScaler", "model_kwargs": {}},
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
    # 运行
    node3.run()
    # 确认是否成功
    assert client.get("/node/{}".format(node3.id)).json["input_shape"] == [
        [[40, 500], [10, 500], [40, 1], [10, 1]]
    ]
    assert client.get("/node/{}".format(node3.id)).json["output_shape"] == [
        [40, 500],
        [10, 500],
        [40, 1],
        [10, 1],
    ]
