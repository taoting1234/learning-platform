from .base import client


def test_get(client):
    assert client.get('/project/1').status_code == 401
    assert client.get('/project').status_code == 401
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    assert client.get('/project/1').json['name'] == 'project1'
    assert client.get('/project/2').json['name'] == 'project2'
    assert client.get('/project/3').status_code == 403
    assert client.get('/project/4').status_code == 404
    assert len(client.get('/project').json['projects']) == 2


def test_post(client):
    # 创建失败（未登录）
    assert client.post(
        '/project', data={
            'name': 'project',
            'tag': '123'
        }
    ).status_code == 401
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    # 创建失败（重名）
    assert client.post(
        '/project', data={
            'name': 'project1',
            'tag': '123'
        }
    ).status_code == 400
    # 创建成功
    res = client.post('/project', data={'name': 'project', 'tag': '123'})
    assert res.status_code == 201
    id_ = res.json['id']
    assert client.get('/project/{}'.format(id_)).json['name'] == 'project'


def test_put(client):
    # 修改失败（未登录）
    assert client.put(
        '/project/1', data={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 401
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    # 修改失败（项目不存在）
    assert client.put(
        '/project/10', data={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 404
    # 修改失败（项目不属于你）
    assert client.put(
        '/project/3', data={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 403
    # 修改失败（项目重名）
    assert client.put(
        '/project/1', data={
            'name': 'project1',
            'tag': '123'
        }
    ).status_code == 400
    # 修改成功
    assert client.put(
        '/project/1', data={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 200
    assert client.get('/project/1').json['name'] == 'project3'


def test_delete(client):
    # 删除失败（未登录）
    assert client.delete(
        '/project/1', data={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 401
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    # 删除失败（项目不存在）
    assert client.delete(
        '/project/10', data={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 404
    # 删除失败（项目不属于你）
    assert client.delete(
        '/project/3', data={
            'name': 'project3',
            'tag': '123'
        }
    ).status_code == 403
    # 删除成功
    assert client.delete('/project/1').status_code == 204
    assert client.get('/project/1').status_code == 404
