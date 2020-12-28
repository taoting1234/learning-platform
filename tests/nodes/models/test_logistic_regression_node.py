import json
import random

import pkg_resources

from ...base import client


def test_logistic_regression_node(client):
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    # 创建项目
    res = client.post(
        '/project', data={
            'name': str(random.random()),
            'tag': 'test'
        }
    )
    assert res.status_code == 201
    project_id = res.json['id']
    # 上传文件
    with open(
        pkg_resources.resource_filename(
            'tests.files.logistic_regression', 'x_data.csv'
        ), 'rb'
    ) as f:
        res = client.post('/file', data={'file': f, 'project_id': project_id})
        assert res.status_code == 201
        file1_id = res.json['id']
    with open(
        pkg_resources.resource_filename(
            'tests.files.logistic_regression', 'y_data.csv'
        ), 'rb'
    ) as f:
        res = client.post('/file', data={'file': f, 'project_id': project_id})
        assert res.status_code == 201
        file2_id = res.json['id']
    # 创建节点
    project_id = res.json['id']
    res = client.post(
        '/node', data={
            'project_id': project_id,
            'node_type': 'input_node'
        }
    )
    assert res.status_code == 201
    node1_id = res.json['id']
    assert client.put(
        '/node/{}'.format(node1_id),
        data={
            'extra':
                json.dumps({
                    'x_input_file': file1_id,
                    'y_input_file': file2_id
                })
        }
    ).status_code == 200
    res = client.post(
        '/node',
        data={
            'project_id': project_id,
            'node_type': 'data_split_node'
        }
    )
    assert res.status_code == 201
    node2_id = res.json['id']
    assert client.put(
        '/node/{}'.format(node2_id),
        data={
            'extra': json.dumps({
                'test_ratio': 0.2,
                'random_state': 888
            })
        }
    ).status_code == 200
    res = client.post(
        '/node',
        data={
            'project_id': project_id,
            'node_type': 'logistic_regression_node'
        }
    )
    assert res.status_code == 201
    node3_id = res.json['id']
    # 创建边
    assert client.post(
        '/node/edge',
        data={
            'project_id': project_id,
            'node1_id': node1_id,
            'node2_id': node2_id
        }
    ).status_code == 201
    assert client.post(
        '/node/edge',
        data={
            'project_id': project_id,
            'node1_id': node2_id,
            'node2_id': node3_id
        }
    ).status_code == 201
    # 运行
    assert client.post('/project/{}/run'.format(project_id)).status_code == 201
    # 确认是否成功
    assert client.get('/node/{}'.format(node3_id)).json['log']
