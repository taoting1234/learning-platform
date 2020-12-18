from flask_login import current_user, login_required
from flask_restful import Resource, abort, marshal_with

from app.fields.user import user_fields
from app.models.user import User
from app.parsers.user import user_modify_parser, user_register_parser


class ResourceUser(Resource):
    @marshal_with(user_fields)
    def get(self, id_):
        user = User.get_by_id(id_)
        if user is None:
            abort(404, message='User not found')
        return user

    def post(self):
        args = user_register_parser.parse_args()
        user = User.get_by_username(args['username'])
        if user is not None:
            abort(400, message='User already exist')
        User.create(**args)
        return {'message': 'Create user success'}, 201

    @login_required
    def put(self, id_):
        if int(current_user.get_id()) != id_:
            abort(403)
        user = User.get_by_id(id_)
        args = user_modify_parser.parse_args()
        if args['password'] and user.check_password(
            args['old_password']
        ) is not True:
            abort(400, message='Old password Wrong')
        user.modify(**args)
        return {'message': 'Modify user success'}, 201
