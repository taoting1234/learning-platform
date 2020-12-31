import random

import pkg_resources

from app.models.node import Node
from app.models.project import Project

from ..base import client

files = [
    ("telco_x.csv", "telco_y.csv"),
    ("amazon_x.csv", "amazon_y.csv"),
    ("cancer_x.csv", "cancer_y.csv"),
]


def test_classifier_node(client):
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    project = Project.create(name=str(random.random()), tag="", user_id=1)
    for file in files:
        # 上传文件
        with open(pkg_resources.resource_filename("tests.files", file[0]), "rb") as f:
            res = client.post("/file", data={"file": f, "project_id": project.id})
            assert res.status_code == 201
            file1_id = res.json["id"]
        with open(pkg_resources.resource_filename("tests.files", file[1]), "rb") as f:
            res = client.post("/file", data={"file": f, "project_id": project.id})
            assert res.status_code == 201
            file2_id = res.json["id"]
        # 创建节点
        node1 = Node.create(
            project_id=project.id,
            node_type="input_node",
            extra={"x_input_file": file1_id, "y_input_file": file2_id},
        )
        node2 = Node.create(
            project_id=project.id,
            node_type="data_split_node",
            extra={"test_ratio": 0.2, "random_state": 888},
        )
        node3 = Node.create(project_id=project.id, node_type="classifier_node")
        # 创建边
        assert (
            client.post(
                "/node/edge",
                data={
                    "project_id": project.id,
                    "node1_id": node1.id,
                    "node2_id": node2.id,
                },
            ).status_code
            == 201
        )
        assert (
            client.post(
                "/node/edge",
                data={
                    "project_id": project.id,
                    "node1_id": node2.id,
                    "node2_id": node3.id,
                },
            ).status_code
            == 201
        )
        # 测试模型
        logistic_regression(node3)
        k_neighbors_classifier(node3)


def logistic_regression(node):
    node.modify(extra={"model": "LogisticRegression", "model_kwargs": {}})
    node.run()


def k_neighbors_classifier(node):
    node.modify(
        extra={"model": "KNeighborsClassifier", "model_kwargs": {"n_neighbors": 3}}
    )
    node.run()
    node.modify(
        extra={"model": "KNeighborsClassifier", "model_kwargs": {"n_neighbors": 4}}
    )
    node.run()
    node.modify(
        extra={"model": "KNeighborsClassifier", "model_kwargs": {"n_neighbors": 5}}
    )
    node.run()
