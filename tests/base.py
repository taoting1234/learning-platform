import os
import shutil
import tempfile

import pytest

from app import create_app
from app.libs.global_varible import g
from app.models.node import Node
from app.models.project import Project
from app.models.user import User


@pytest.fixture
def client():
    g.file_directory = "./test_files"
    shutil.rmtree(g.file_directory, ignore_errors=True)
    os.makedirs(g.file_directory, exist_ok=True)
    app = create_app(test=True, file_directory=g.file_directory)
    with app.test_client() as client:
        with app.app_context():
            # 测试前运行
            # 创建用户
            User.create(username="user1", password="123")
            User.create(username="user2", password="123")
            # 创建项目
            Project.create(
                user_id=1, name="project1", description="description1", tag="tag1"
            )
            Project.create(
                user_id=1, name="project2", description="description2", tag="tag2"
            )
            Project.create(
                user_id=2, name="project3", description="description3", tag="tag3"
            )
            # 创建文件
            file_path = "{}/1.test".format(tempfile.gettempdir())
            with open(file_path, "wb") as f:
                f.write(os.urandom(128))
            client.post("/session", data={"username": "user1", "password": "123"})
            with open(file_path, "rb") as f:
                client.post("/file", data={"file": f, "project_id": 1})
            client.post("/session", data={"username": "user2", "password": "123"})
            with open(file_path, "rb") as f:
                client.post("/file", data={"file": f, "project_id": 3})
            client.delete("/session")
            # 创建节点
            Node.create(project_id=1, node_type="123")
            Node.create(project_id=3, node_type="123")
            Node.create(project_id=1, node_type="123")
            Node.create(project_id=1, node_type="123")
            Node.create(project_id=1, node_type="123")
            # 创建边
            client.post("/session", data={"username": "user1", "password": "123"})
            client.post(
                "/node/edge", data={"project_id": 1, "node1_id": 1, "node2_id": 3}
            )
            client.post(
                "/node/edge", data={"project_id": 1, "node1_id": 1, "node2_id": 4}
            )
            client.post(
                "/node/edge", data={"project_id": 1, "node1_id": 5, "node2_id": 1}
            )
            client.delete("/session")

            # yield
            yield client

            # 测试后运行
            # 等待线程结束
            if getattr(g, "thread_list", None):
                for thread in g.thread_list:
                    thread.join()
                g.thread_list = None
        # 删除文件夹
        shutil.rmtree(app.config["FILE_DIRECTORY"])
