from flask import current_app, session
from flask_login import current_user, login_required
from flask_restful import Resource, abort, marshal_with

from app.fields.user import user_field, user_search_field
from app.libs.auth import self_only
from app.models.invitation_code import InvitationCode
from app.models.user import User
from app.parsers.user import user_modify_parser, user_register_parser, user_search_parser


class ResourceUser(Resource):
    @marshal_with(user_field)
    @login_required
    @self_only(User)
    def get(self, id_):
        user = User.get_by_id(id_)
        if user is None:
            abort(404, message="User not found")
        return user

    @login_required
    def put(self, id_):
        if not current_user.permission and current_user.id != id_:
            abort(403)
        user = User.get_by_id(id_)
        args = user_modify_parser.parse_args()
        if not current_user.permission and args["password"] and user.check_password(args["old_password"]) is not True:
            abort(400, message="Old password Wrong")
        if not current_user.permission and (args["block"] or args["permission"]):
            abort(403)
        user.modify(**args)
        return {"message": "Modify user success"}


class ResourceUserList(Resource):
    @marshal_with(user_search_field)
    @login_required
    @self_only(User, user_search_parser)
    def get(self):
        args = user_search_parser.parse_args()
        res = User.search(**args)
        return res

    @marshal_with(user_field)
    def post(self):
        args = user_register_parser.parse_args()
        if current_app.config["TESTING"] is False:
            if not args["captcha"] or args["captcha"].lower() != session.get("captcha", "").lower():
                session["captcha"] = ""
                abort(400, message="Captcha wrong")
        user = User.get_by_username(args["username"])
        if user is not None:
            abort(400, message="User already exist")
        if InvitationCode.check_and_use_code(args["code"]) is False:
            abort(400, message="Invitation code wrong")
        user = User.create(**args)
        return user, 201
