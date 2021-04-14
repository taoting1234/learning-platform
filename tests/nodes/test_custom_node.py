import random
import tempfile

import pkg_resources

from app.models.node import Node
from app.models.project import Project
from app.models.user import User

from ..base import client

code_1 = """
from sklearn.model_selection import train_test_split

def run(input_files, **kwargs):
    x_train, x_test, y_train, y_test = train_test_split(
        input_files[0][0],
        input_files[0][1],
        test_size=0.2,
        random_state=888,
    )
    return x_train, x_test, y_train, y_test
"""
code_2 = """
import pandas as pd

def run(input_files, **kwargs):
    x = pd.read_csv('/app/files/user/telco.csv')
    y = x.iloc[:, [-1]]
    x.drop(y.columns, axis=1, inplace=True)
    return x, y
"""


def test_custom_node_1(client):
    User.create(username="user1", password="123")
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 创建项目
    project = Project.create(name=str(random.random()), tag="", user_id=1)
    # 上传文件
    with open(pkg_resources.resource_filename("tests.files", "telco.csv"), "rb") as f:
        client.post("/file", data={"file": f, "project_id": project.id, "dir": "/"})
    file_path = "{}/main.py".format(tempfile.gettempdir())
    with open(file_path, "w") as f:
        f.write(code_1)
    with open(file_path, "rb") as f:
        client.post("/file", data={"file": f, "project_id": project.id, "dir": "/"})
    # 创建节点
    node1 = Node.create(
        project_id=project.id,
        node_type="not_split_input_node",
        extra={"has_header": True, "input_file": "/telco.csv", "label_columns": "-1"},
    )
    node2 = Node.create(
        project_id=project.id,
        node_type="custom_node",
        extra={
            "input_type": 1,
            "output_type": 2,
            "directory": "/",
            "target_file": "main",
        },
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
    # 运行
    node2.run()
    # 确认是否成功
    assert client.get("/node/{}".format(node2.id)).json["input_shape"] == [[[1000, 41], [1000, 1]]]
    assert client.get("/node/{}".format(node2.id)).json["output_shape"] == [
        [800, 41],
        [200, 41],
        [800, 1],
        [200, 1],
    ]


def test_custom_node_2(client):
    User.create(username="user1", password="123")
    # 登录
    client.post("/session", data={"username": "user1", "password": "123"})
    # 创建项目
    project = Project.create(name=str(random.random()), tag="", user_id=1)
    # 上传文件
    with open(pkg_resources.resource_filename("tests.files", "telco.csv"), "rb") as f:
        client.post("/file", data={"file": f, "project_id": project.id, "dir": "/"})
    file_path = "{}/main.py".format(tempfile.gettempdir())
    with open(file_path, "w") as f:
        f.write(code_2)
    with open(file_path, "rb") as f:
        client.post("/file", data={"file": f, "project_id": project.id, "dir": "/"})
    # 创建节点
    node1 = Node.create(
        project_id=project.id,
        node_type="custom_node",
        extra={
            "input_type": 0,
            "output_type": 1,
            "directory": "/",
            "target_file": "main",
        },
    )
    # 运行
    node1.run()
    # 确认是否成功
    assert client.get("/node/{}".format(node1.id)).json["input_shape"] == []
    assert client.get("/node/{}".format(node1.id)).json["output_shape"] == [
        [1000, 41],
        [1000, 1],
    ]
