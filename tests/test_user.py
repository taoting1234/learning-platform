import pytest
from flask import Flask

from app import config
from app.models.user import User
from flask_app import register_plugin, register_resource


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['TESTING'] = True
    register_resource(app)
    register_plugin(app)

    with app.test_client() as client:
        with app.app_context():
            User.create(username='admin', password='admin')
        yield client


def test_user(client):
    # 获取用户
    assert client.get('/user/1').json['username'] == 'admin'
    assert client.get('/user/2').status_code == 404
    # 创建用户（失败）
    assert client.post(
        '/user', json={
            'username': 'admin',
            'password': 'user'
        }
    ).status_code == 400
    # 创建用户（成功）
    assert client.post(
        '/user', json={
            'username': 'user',
            'password': 'user'
        }
    ).status_code == 201
    # 登录
    assert client.post(
        '/session', json={
            'username': 'user',
            'password': 'user'
        }
    ).status_code == 201
    # 获取用户
    assert client.get('/user/2').json['username'] == 'user'
    # 修改用户失败（未登录）
    assert client.delete('/session').status_code == 204
    assert client.put(
        '/user/2', json={
            'password': 'user',
            'old_password': 'user'
        }
    ).status_code == 401
    # 修改用户失败（登录其他人）
    assert client.post(
        '/session', json={
            'username': 'admin',
            'password': 'admin'
        }
    ).status_code == 201
    assert client.put(
        '/user/2', json={
            'password': 'user',
            'old_password': 'user'
        }
    ).status_code == 403
    # 修改用户失败（密码错误）
    assert client.post(
        '/session', json={
            'username': 'user',
            'password': 'user'
        }
    ).status_code == 201
    assert client.put(
        '/user/2', json={
            'password': 'user',
            'old_password': '123'
        }
    ).status_code == 400
    assert client.put(
        '/user/2', json={
            'password': 'user',
            'old_password': ''
        }
    ).status_code == 400
    # 修改成功
    assert client.put(
        '/user/2', json={
            'password': '123',
            'old_password': 'user'
        }
    ).status_code == 201
    # 登录
    assert client.post(
        '/session', json={
            'username': 'user',
            'password': 'user'
        }
    ).status_code == 400
    assert client.post(
        '/session', json={
            'username': 'user',
            'password': '123'
        }
    ).status_code == 201
