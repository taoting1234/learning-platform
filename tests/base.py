import shutil
import tempfile
import time

import pytest
from flask import Flask

from app import create_app
from app.libs.global_varible import g
from app.models.node import Node
from app.models.project import Project
from app.models.user import User


@pytest.fixture
def client():
    app = create_app(test=True)
    with app.test_client() as client:
        with app.app_context():
            # 测试前运行
            # 创建用户
            User.create(username='user1', password='123')
            User.create(username='user2', password='123')
            # 创建项目
            Project.create(
                user_id=1,
                name='project1',
                description='description1',
                tag='tag1'
            )
            Project.create(
                user_id=1,
                name='project2',
                description='description2',
                tag='tag2'
            )
            Project.create(
                user_id=2,
                name='project3',
                description='description3',
                tag='tag3'
            )
            # 创建文件
            file_path = "{}/1.test".format(tempfile.gettempdir())
            with open(file_path, "wb") as f:
                f.write(bytes("123", encoding='utf8'))
            assert client.post(
                '/session', data={
                    'username': 'user1',
                    'password': '123'
                }
            ).status_code == 201
            with open(file_path, "rb") as f:
                assert client.post(
                    '/file', data={
                        'file': f,
                        'project_id': 1
                    }
                ).status_code == 201
            assert client.post(
                '/session', data={
                    'username': 'user2',
                    'password': '123'
                }
            ).status_code == 201
            with open(file_path, "rb") as f:
                assert client.post(
                    '/file', data={
                        'file': f,
                        'project_id': 3
                    }
                ).status_code == 201
            assert client.delete('/session').status_code == 204
            # 创建节点
            Node.create(project_id=1, node_type='input_node')
            Node.create(project_id=3, node_type='input_node')
            Node.create(project_id=1, node_type='input_node')
            Node.create(project_id=1, node_type='input_node')
            # 创建边
            assert client.post(
                '/session', data={
                    'username': 'user1',
                    'password': '123'
                }
            ).status_code == 201
            assert client.post(
                '/node/edge',
                data={
                    'project_id': 1,
                    'node1_id': 1,
                    'node2_id': 3
                }
            ).status_code == 201
            assert client.delete('/session').status_code == 204

            # yield
            yield client

            # 测试后运行
            # 等待线程结束
            if getattr(g, 'thread_list', None):
                for thread in g.thread_list:
                    thread.join()
                g.thread_list = None
            # 删除文件夹
            shutil.rmtree(app.config['FILE_DIRECTORY'], ignore_errors=True)
