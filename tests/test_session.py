from .base import client


def test_session(client):
    # 未登录
    assert client.get('/session').status_code == 404
    # 登录
    assert client.post(
        '/session', json={
            'username': 'admin',
            'password': 'admin'
        }
    ).status_code == 201
    assert client.get('/session').status_code == 200
    assert client.get('/session').json['username'] == 'admin'
    # 登出
    assert client.delete('/session').status_code == 204
    assert client.get('/session').status_code == 404
    # 失败的登录
    assert client.post(
        '/session', json={
            'username': 'admin',
            'password': '123'
        }
    ).status_code == 400
    assert client.get('/session').status_code == 404
