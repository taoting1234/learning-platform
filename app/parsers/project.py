from flask_restful import reqparse

from app.parsers.search import search_parser

project_create_parser = reqparse.RequestParser()
project_create_parser.add_argument(
    "name", type=str, required=True, help="Project name cannot be empty"
)
project_create_parser.add_argument("description", type=str)
project_create_parser.add_argument(
    "tag", type=str, required=True, help="Project tag cannot be empty"
)

project_modify_parser = reqparse.RequestParser()
project_modify_parser.add_argument("name", type=str)
project_modify_parser.add_argument("description", type=str)
project_modify_parser.add_argument("tag", type=str)

project_search_parser = search_parser.copy()
project_search_parser.add_argument("user_id", type=int)
project_search_parser.add_argument("name", type=str)
project_search_parser.add_argument("description", type=str)
project_search_parser.add_argument("tag", type=str)
