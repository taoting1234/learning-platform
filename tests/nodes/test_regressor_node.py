import os
import random

import pkg_resources

from app.models.node import Node
from app.models.project import Project

from ..base import client


def init(client, file):
    # 登录
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    # 创建项目
    project = Project.create(name=str(random.random()), tag="", user_id=1)
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
        node_type="split_input_node",
        extra={"has_header": False, "x_input_file": file1_id, "y_input_file": file2_id},
    )
    node2 = Node.create(
        project_id=project.id,
        node_type="data_split_node",
        extra={"test_ratio": 0.2, "random_state": 888},
    )
    node3 = Node.create(project_id=project.id, node_type="regressor_node")
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
    return node3


def test_linear_regression(client):
    files = [("x1.csv", "y1.csv")]
    model_kwargs_list = [{}]
    for file in files:
        for model_kwargs in model_kwargs_list:
            node = init(client, file)
            node.modify(
                extra={"model": "LinearRegression", "model_kwargs": model_kwargs}
            )
            node.run(False if os.environ.get("COMPLETE_TEST") else True)


def test_k_neighbors_regressor(client):
    files = [("x1.csv", "y1.csv")]
    model_kwargs_list = [{"n_neighbors": 3}, {"n_neighbors": 4}, {"n_neighbors": 5}]
    for file in files:
        for model_kwargs in model_kwargs_list:
            node = init(client, file)
            node.modify(
                extra={"model": "KNeighborsRegressor", "model_kwargs": model_kwargs}
            )
            node.run(False if os.environ.get("COMPLETE_TEST") else True)


def test_svr(client):
    files = [("x1.csv", "y1.csv")]
    model_kwargs_list = [{}]
    for file in files:
        for model_kwargs in model_kwargs_list:
            node = init(client, file)
            node.modify(extra={"model": "SVR", "model_kwargs": model_kwargs})
            node.run(False if os.environ.get("COMPLETE_TEST") else True)


def test_linear_svr(client):
    files = [("x1.csv", "y1.csv")]
    model_kwargs_list = [{}]
    for file in files:
        for model_kwargs in model_kwargs_list:
            node = init(client, file)
            node.modify(extra={"model": "LinearSVR", "model_kwargs": model_kwargs})
            node.run(False if os.environ.get("COMPLETE_TEST") else True)


def test_xgb(client):
    files = [("x1.csv", "y1.csv")]
    model_kwargs_list = [{}]
    for file in files:
        for model_kwargs in model_kwargs_list:
            node = init(client, file)
            node.modify(extra={"model": "XGBRegressor", "model_kwargs": model_kwargs})
            node.run(False if os.environ.get("COMPLETE_TEST") else True)


def test_xgb_rf(client):
    files = [("x1.csv", "y1.csv")]
    model_kwargs_list = [{}]
    for file in files:
        for model_kwargs in model_kwargs_list:
            node = init(client, file)
            node.modify(extra={"model": "XGBRFRegressor", "model_kwargs": model_kwargs})
            node.run(False if os.environ.get("COMPLETE_TEST") else True)


def test_lgb(client):
    files = [("x1.csv", "y1.csv")]
    model_kwargs_list = [{}]
    for file in files:
        for model_kwargs in model_kwargs_list:
            node = init(client, file)
            node.modify(extra={"model": "LGBMRegressor", "model_kwargs": model_kwargs})
            node.run(False if os.environ.get("COMPLETE_TEST") else True)
