import os
import shutil
import tempfile

from .base import client


def test_get(client):
    assert client.get('/file/1').status_code == 401
    assert client.get('/file', data={'project_id': 1}).status_code == 401
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    assert client.get('/file/1').status_code == 404
    assert len(client.get('/file', data={'project_id': 1}).json['files']) == 0
    assert client.get('/file', data={'project_id': 10}).status_code == 404
    assert client.get('/file', data={'project_id': 3}).status_code == 403


def test_post(client):
    # 创建文件
    file_path = "{}/1.a".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(bytes("123", encoding='utf8'))
    # 上传文件失败（未登录）
    with open(file_path, "rb") as f:
        assert client.post(
            '/file', data={
                'file': f,
                'project_id': 1
            }
        ).status_code == 401
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    # 上传文件失败（项目不存在）
    with open(file_path, "rb") as f:
        assert client.post(
            '/file', data={
                'file': f,
                'project_id': 10
            }
        ).status_code == 404
    # 上传文件失败（项目不属于你）
    with open(file_path, "rb") as f:
        assert client.post(
            '/file', data={
                'file': f,
                'project_id': 3
            }
        ).status_code == 403
    # 上传文件成功
    with open(file_path, "rb") as f:
        assert client.post(
            '/file', data={
                'file': f,
                'project_id': 1
            }
        ).status_code == 201
    assert client.get('/file/1').json['filename'] == '1.a'
    assert len(client.get('/file', data={'project_id': 1}).json['files']) == 1
    assert os.path.exists('./file/1/user/1.a')
    size = client.get('/file/1').json['size']
    # 修改文件
    with open(file_path, "wb") as f:
        f.write(bytes("1234", encoding='utf8'))
    # 覆盖文件
    with open(file_path, "rb") as f:
        assert client.post(
            '/file', data={
                'file': f,
                'project_id': 1
            }
        ).status_code == 201
    assert client.get('/file/1').json['filename'] == '1.a'
    assert os.path.exists('./file/1/user/1.a')
    assert client.get('/file/1').json['size'] > size
    # 删除文件夹
    shutil.rmtree('./file')


def test_put(client):
    # 创建文件
    file_path = "{}/1.a".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(bytes("123", encoding='utf8'))
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    # 上传文件
    with open(file_path, "rb") as f:
        assert client.post(
            '/file', data={
                'file': f,
                'project_id': 1
            }
        ).status_code == 201
    new_file_path = file_path[:-1] + 'b'
    shutil.copy(file_path, new_file_path)
    # 上传文件
    with open(new_file_path, "rb") as f:
        assert client.post(
            '/file', data={
                'file': f,
                'project_id': 1
            }
        ).status_code == 201
    # 登出
    assert client.delete('/session').status_code == 204
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user2',
            'password': '123'
        }
    ).status_code == 201
    # 上传文件
    with open(file_path, "rb") as f:
        assert client.post(
            '/file', data={
                'file': f,
                'project_id': 3
            }
        ).status_code == 201
    # 登出
    assert client.delete('/session').status_code == 204
    # 修改文件失败（未登录）
    assert client.put('/file/1', data={'filename': '1.b'}).status_code == 401
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    # 修改文件失败（文件不存在）
    assert client.put('/file/10', data={'filename': '1.b'}).status_code == 404
    # 修改文件失败（项目不属于你）
    assert client.put('/file/3', data={'filename': '1.b'}).status_code == 403
    # 修改文件失败（目标文件已存在）
    assert client.put('/file/1', data={'filename': '1.b'}).status_code == 400
    # 修改文件成功
    assert client.put('/file/1', data={'filename': '1.c'}).status_code == 200
    assert client.get('/file/1').json['filename'] == '1.c'
    assert os.path.exists('./file/1/user/1.c')
    # 删除文件夹
    shutil.rmtree('./file')


def test_delete(client):
    # 创建文件
    file_path = "{}/1.a".format(tempfile.gettempdir())
    with open(file_path, "wb") as f:
        f.write(bytes("123", encoding='utf8'))
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    # 上传文件
    with open(file_path, "rb") as f:
        assert client.post(
            '/file', data={
                'file': f,
                'project_id': 1
            }
        ).status_code == 201
    # 登出
    assert client.delete('/session').status_code == 204
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user2',
            'password': '123'
        }
    ).status_code == 201
    # 上传文件
    with open(file_path, "rb") as f:
        assert client.post(
            '/file', data={
                'file': f,
                'project_id': 3
            }
        ).status_code == 201
    # 登出
    assert client.delete('/session').status_code == 204
    # 删除文件失败（用户未登录）
    assert client.delete('/file/1').status_code == 401
    # 登录
    assert client.post(
        '/session', data={
            'username': 'user1',
            'password': '123'
        }
    ).status_code == 201
    # 删除文件失败（文件不存在）
    assert client.delete('/file/10').status_code == 404
    # 删除文件失败（项目不属于你）
    assert client.get('/file/2').status_code == 403
    assert client.delete('/file/2').status_code == 403
    # 删除文件成功
    assert client.delete('/file/1').status_code == 204
    assert client.get('/file/1').status_code == 404
    assert os.path.exists('./file/1/user/1.a') is False
    # 删除文件夹
    shutil.rmtree('./file')
