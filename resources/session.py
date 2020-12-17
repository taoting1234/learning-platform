from flask_login import current_user, login_user, logout_user
from flask_restful import Resource, abort, marshal_with

from fields.user import user_fields
from models.user import User
from parsers.session import session_parser


class ResourceSession(Resource):
    @marshal_with(user_fields)
    def get(self):
        if current_user.is_anonymous:
            abort(404, message='Not login')
        return current_user

    def post(self):
        args = session_parser.parse_args()
        user = User.get_by_username(args['username'])
        if user is None or user.check_password(args['password']) is not True:
            abort(400, message='Username or password wrong')
        login_user(user)
        return {'message': 'Login success'}, 201

    def delete(self):
        logout_user()
        return {'message': 'Logout success'}, 204
