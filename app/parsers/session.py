from flask_restful import reqparse

session_parser = reqparse.RequestParser()
session_parser.add_argument("username", type=str, required=True)
session_parser.add_argument("password", type=str, required=True)
session_parser.add_argument("captcha", type=str)
