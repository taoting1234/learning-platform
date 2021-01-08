import random

import pkg_resources
from flask import current_app

from app.models.node import Node
from app.models.project import Project

from ..base import client

code = """
import pandas as pd

def get_output(input_):
    return 1

def run():
    df = pd.read_csv('./{}/{}/user/telco.csv')
    print(df.describe())
"""


def test_custom_node(client):
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
    with open(pkg_resources.resource_filename("tests.files", "telco.csv"), "rb") as f:
        assert (
            client.post("/file", data={"file": f, "project_id": project.id}).status_code
            == 201
        )
    # 创建节点
    node = Node.create(
        project_id=project.id,
        node_type="custom_node",
        extra={
            "input_node": 0,
            "input_size": [0],
            "code": code.format(current_app.config["FILE_DIRECTORY"], project.id),
        },
    )
    node.run()
