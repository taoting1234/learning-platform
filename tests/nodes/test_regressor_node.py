import os
import random

import pkg_resources

from app.models.node import Node
from app.models.project import Project
from app.models.user import User

from ..base import client


def test_regressor_node(client):
    User.create(username="user1", password="123")
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 创建项目
    project = Project.create(name=str(random.random()), tag="", user_id=1)
    # 上传文件
    with open(pkg_resources.resource_filename("tests.files", "x1.csv"), "rb") as f:
        client.post("/file", data={"file": f, "project_id": project.id, "dir": "/"})
    with open(pkg_resources.resource_filename("tests.files", "y1.csv"), "rb") as f:
        client.post("/file", data={"file": f, "project_id": project.id, "dir": "/"})
    # 创建节点
    node1 = Node.create(
        project_id=project.id,
        node_type="split_input_node",
        extra={
            "has_header": False,
            "x_input_file": "/x1.csv",
            "y_input_file": "/y1.csv",
        },
    )
    node2 = Node.create(
        project_id=project.id,
        node_type="data_split_node",
        extra={"test_ratio": 0.2, "random_state": 888},
    )
    node3 = Node.create(
        project_id=project.id,
        node_type="regressor_node",
        extra={"model": "LinearRegression", "model_kwargs": {}},
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
    node3.run(not os.environ.get("COMPLETE_TEST"))
