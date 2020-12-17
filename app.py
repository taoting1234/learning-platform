import platform

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_restful import Api

from models.base import db

api = Api(catch_all_404s=True)
cors = CORS(supports_credentials=True)
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    register_resource(app)
    register_plugin(app)
    return app


def register_plugin(app):
    # 注册restful
    api.init_app(app)

    # 注册sqlalchemy
    db.init_app(app)

    # 初始化数据库
    with app.app_context():
        db.create_all()

    # 注册cors
    cors.init_app(app)

    # 注册用户管理器
    from models.user import User

    @login_manager.user_loader
    def load_user(id_):
        return User.get_by_id(id_)

    login_manager.init_app(app)

    return app


def register_resource(app):
    from resources.session import ResourceSession
    from resources.user import ResourceUser
    api.add_resource(ResourceSession, '/session')
    api.add_resource(ResourceUser, '/user', '/user/<int:id_>')
    return app


if __name__ == '__main__':
    flask_app = create_app()
    if platform.system() == 'Linux':
        flask_app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        flask_app.run(host="0.0.0.0", port=5000, debug=True)
