from flask_restful import reqparse

from app.parsers.search import search_parser

user_register_parser = reqparse.RequestParser()
user_register_parser.add_argument(
    "username", type=str, required=True, help="Username cannot be empty"
)
user_register_parser.add_argument(
    "password", type=str, required=True, help="Password cannot be empty"
)

user_modify_parser = reqparse.RequestParser()
user_modify_parser.add_argument("organization", type=str)
user_modify_parser.add_argument("password", type=str)
user_modify_parser.add_argument("old_password", type=str)
user_modify_parser.add_argument("permission", type=int)
user_modify_parser.add_argument("block", type=int)

user_search_parser = search_parser.copy()
user_search_parser.add_argument("username", type=str)
user_search_parser.add_argument("permission", type=int)
