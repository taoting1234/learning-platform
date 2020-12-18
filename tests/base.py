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
