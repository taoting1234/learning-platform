import pytest
from flask import Flask

from app.models.project import Project
from app.models.user import User
from flask_app import register_plugin, register_resource


@pytest.fixture
def client():
    app = Flask(__name__)
    try:
        app.config.from_object("app.config")
    except ImportError:
        app.config.from_object("app.config_demo")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['TESTING'] = True
    register_resource(app)
    register_plugin(app)

    with app.test_client() as client:
        with app.app_context():
            User.create(username='user1', password='123')
            User.create(username='user2', password='123')
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
        yield client
