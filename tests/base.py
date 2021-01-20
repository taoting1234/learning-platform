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
            pass

            # yield
            yield client

        # 删除文件夹
        shutil.rmtree(app.config["FILE_DIRECTORY"])
