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
    assert client.get("/node/1").json["node_type"] == "input_node"
    assert client.get("/node/2").status_code == 403
    assert client.get("/node/-1").status_code == 404
    assert len(client.get("/node", data={"project_id": 1}).json["nodes"]) == 3
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
            "/node/edge", data={"project_id": 1, "node1_id": 1, "node2_id": 4}
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
            "/node/edge", data={"project_id": 1, "node1_id": 1, "node2_id": 4}
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
