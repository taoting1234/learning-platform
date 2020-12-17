import pytest
from flask import Flask

from app import register_plugin, register_resource
from models.user import User


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['TESTING'] = True
    register_resource(app)
    register_plugin(app)

    with app.test_client() as client:
        with app.app_context():
            User.create(username='admin', password='admin')
        yield client


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
