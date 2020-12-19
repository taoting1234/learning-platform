from .base import client


def test_post(client):
    # 创建用户（失败）
    assert client.post(
        '/user', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 400
    # 创建用户（成功）
    assert client.post(
        '/user', data={
            'username': 'user',
            'password': 'user'
        }
    ).status_code == 201
    assert client.post(
        '/session', data={
            'username': 'user',
            'password': 'user'
        }
    ).status_code == 201
    assert client.get('/user/3').json['username'] == 'user'


def test_put(client):
    # 修改用户失败（未登录）
    assert client.delete('/session').status_code == 204
    assert client.put(
        '/user/1', data={
            'password': 'user',
            'old_password': 'user'
        }
    ).status_code == 401
    # 修改用户失败（登录其他人）
    assert client.post(
        '/session', data={
            'username': 'user2',
            'password': '123'
        }
    ).status_code == 201
    assert client.put(
        '/user/1', data={
            'password': 'user',
            'old_password': 'user'
        }
    ).status_code == 403
    # 修改用户失败（密码错误）
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    assert client.put(
        '/user/1', data={
            'password': 'user',
            'old_password': 'user'
        }
    ).status_code == 400
    assert client.put(
        '/user/1', data={
            'password': 'user',
            'old_password': ''
        }
    ).status_code == 400
    # 修改成功
    assert client.put(
        '/user/1', data={
            'password': 'user',
            'old_password': '123'
        }
    ).status_code == 200
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 400
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': 'user'
        }
    ).status_code == 201
