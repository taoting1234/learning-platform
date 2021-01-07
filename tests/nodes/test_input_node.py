import json
import os
import random

import pkg_resources
from flask import current_app

from ..base import client


def test_split_input_node(client):
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
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
    # 确认是否成功
    assert client.get("/node/{}".format(node_id)).json["input_shape"] == []
    assert client.get("/node/{}".format(node_id)).json["output_shape"] == [
        [50, 500],
        [50, 1],
    ]
    assert os.path.exists(
        "{}/{}/node/{}/x.csv".format(
            current_app.config["FILE_DIRECTORY"], project_id, node_id
        )
    )
    assert os.path.exists(
        "{}/{}/node/{}/y.csv".format(
            current_app.config["FILE_DIRECTORY"], project_id, node_id
        )
    )


def test_not_split_input_node(client):
    assert (
        client.post(
            "/session", data={"username": "user1", "password": "123"}
        ).status_code
        == 201
    )
    res = client.post("/project", data={"name": str(random.random()), "tag": "test"})
    assert res.status_code == 201
    project_id = res.json["id"]
    res = client.post(
        "/node", data={"project_id": project_id, "node_type": "not_split_input_node"}
    )
    assert res.status_code == 201
    node_id = res.json["id"]
    with open(pkg_resources.resource_filename("tests.files", "telco.csv"), "rb") as f:
        res = client.post("/file", data={"file": f, "project_id": project_id})
        assert res.status_code == 201
        file_id = res.json["id"]
    assert (
        client.put(
            "/node/{}".format(node_id),
            data={
                "extra": json.dumps(
                    {
                        "has_header": True,
                        "x_input_file": file_id,
                        "label_columns": "-1",
                    }
                )
            },
        ).status_code
        == 200
    )
    assert client.post("/project/{}/run".format(project_id)).status_code == 201
    # 确认是否成功
    assert client.get("/node/{}".format(node_id)).json["input_shape"] == []
    assert client.get("/node/{}".format(node_id)).json["output_shape"] == [
        [1000, 41],
        [1000, 1],
    ]
    assert os.path.exists(
        "{}/{}/node/{}/x.csv".format(
            current_app.config["FILE_DIRECTORY"], project_id, node_id
        )
    )
    assert os.path.exists(
        "{}/{}/node/{}/y.csv".format(
            current_app.config["FILE_DIRECTORY"], project_id, node_id
        )
    )
