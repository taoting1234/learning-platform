import os
import random

import pkg_resources

from app.models.node import Node
from app.models.project import Project

from ..base import client


def test_classifier_node(client):
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
        extra={"has_header": True, "x_input_file": file_id, "label_columns": "-1"},
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
    node3.run(not os.environ.get("COMPLETE_TEST"))
