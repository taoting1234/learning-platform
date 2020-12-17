from flask_restful import Resource, abort, marshal_with

from app.fields.user import user_fields
from app.models.user import User
from app.parsers.user import user_register_parser


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
