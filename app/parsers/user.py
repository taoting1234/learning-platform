from flask_restful import reqparse

user_register_parser = reqparse.RequestParser()
user_register_parser.add_argument(
    'username', type=str, required=True, help='Username cannot be empty'
)
user_register_parser.add_argument(
    'password', type=str, required=True, help='Password cannot be empty'
)

user_modify_parser = reqparse.RequestParser()
user_modify_parser.add_argument('password', type=str)
user_modify_parser.add_argument('old_password', type=str)
