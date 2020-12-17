from flask_restful import reqparse

session_parser = reqparse.RequestParser()
session_parser.add_argument(
    'username', type=str, required=True, help='Username cannot be empty'
)
session_parser.add_argument(
    'password', type=str, required=True, help='Password cannot be empty'
)
