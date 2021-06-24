from flask_restful import reqparse

language_parser = reqparse.RequestParser()
language_parser.add_argument("lang", type=int, required=True)
