import json
import os
import random

import pkg_resources
from flask import current_app

from app.models.user import User

from ..base import client


def test_data_split_node(client):
    User.create(username="user1", password="123")
    client.post("/session", data={"username": "user1", "password": "123"})
    res = client.post("/project", data={"name": str(random.random()), "tag": "test"})
    assert res.status_code == 201
    project_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "split_input_node"}
    )
    assert res.status_code == 201
    node1_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "data_split_node"}
    )
    assert res.status_code == 201
    node2_id = res.json["id"]
    with open(pkg_resources.resource_filename("tests.files", "x1.csv"), "rb") as f:
        client.post("/file", data={"file": f, "project_id": project_id, "dir": "/"})
    with open(pkg_resources.resource_filename("tests.files", "y1.csv"), "rb") as f:
        client.post("/file", data={"file": f, "project_id": project_id, "dir": "/"})
    assert (
        client.put(
            "/node/{}".format(node1_id),
            data={
                "extra": json.dumps(
                    {
                        "has_header": False,
                        "x_input_file": "/x1.csv",
                        "y_input_file": "/y1.csv",
                    }
                )
            },
        ).status_code
        == 200
    )
    assert (
        client.put(
            "/node/{}".format(node2_id),
            data={"extra": json.dumps({"test_ratio": 0.2, "random_state": 888})},
        ).status_code
        == 200
    )
    assert client.post(
        "/node/edge",
        data={"project_id": project_id, "node1_id": node1_id, "node2_id": node2_id},
    )
    assert client.post("/project/{}/run".format(project_id)).status_code == 201
    # 确认是否成功
    assert client.get("/node/{}".format(node2_id)).json["input_shape"] == [
        [
            [50, 500],
            [50, 1],
        ]
    ]
    assert client.get("/node/{}".format(node2_id)).json["output_shape"] == [
        [40, 500],
        [10, 500],
        [40, 1],
        [10, 1],
    ]
    assert os.path.exists(
        "{}/{}/node/{}/x_train.csv".format(
            current_app.config["FILE_DIRECTORY"], project_id, node2_id
        )
    )
    assert os.path.exists(
        "{}/{}/node/{}/x_test.csv".format(
            current_app.config["FILE_DIRECTORY"], project_id, node2_id
        )
    )
    assert os.path.exists(
        "{}/{}/node/{}/y_train.csv".format(
            current_app.config["FILE_DIRECTORY"], project_id, node2_id
        )
    )
    assert os.path.exists(
        "{}/{}/node/{}/y_test.csv".format(
            current_app.config["FILE_DIRECTORY"], project_id, node2_id
        )
    )
