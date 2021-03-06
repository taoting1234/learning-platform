from flask import current_app, session
from flask_login import current_user, login_required, login_user, logout_user
from flask_restful import Resource, abort, marshal_with

from app.fields.user import user_field
from app.models.user import User
from app.parsers.session import session_parser


class ResourceSession(Resource):
    @marshal_with(user_field)
    @login_required
    def get(self):
        return current_user

    @marshal_with(user_field)
    def post(self):
        args = session_parser.parse_args()
        if current_app.config["TESTING"] is False:
            if not args["captcha"] or args["captcha"].lower() != session.get("captcha", "").lower():
                session["captcha"] = ""
                abort(400, message="Captcha wrong")
        user = User.get_by_username(args["username"])
        if user is None or user.check_password(args["password"]) is not True:
            abort(400, message="Username or password wrong")
        if user.block:
            abort(403, message="User is blocked")
        login_user(user)
        return user, 201

    def delete(self):
        logout_user()
        return "", 204
