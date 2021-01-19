from flasgger import swag_from
from flask_login import current_user, login_required, login_user, logout_user
from flask_restful import Resource, abort, marshal_with

from app.fields.user import user_field
from app.models.user import User
from app.parsers.session import session_parser


class ResourceSession(Resource):
    @marshal_with(user_field)
    @login_required
    @swag_from("../../docs/apis/session/session_get.yaml")
    def get(self):
        return current_user

    @marshal_with(user_field)
    @swag_from("../../docs/apis/session/session_post.yaml")
    def post(self):
        args = session_parser.parse_args()
        user = User.get_by_username(args["username"])
        if user is None or user.check_password(args["password"]) is not True:
            abort(400, message="Username or password wrong")
        login_user(user)
        return user, 201

    @swag_from("../../docs/apis/session/session_delete.yaml")
    def delete(self):
        logout_user()
        return "", 204
