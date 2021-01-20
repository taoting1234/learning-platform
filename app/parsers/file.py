from flask_restful import reqparse
from werkzeug.datastructures import FileStorage

file_create_parser = reqparse.RequestParser()
file_create_parser.add_argument(
    "project_id", type=int, required=True, help="Project id cannot be empty"
)
file_create_parser.add_argument("dir", type=str, default="/")
file_create_parser.add_argument(
    "file",
    type=FileStorage,
    required=True,
    location="files",
    help="File cannot be empty",
)

file_modify_parser = reqparse.RequestParser()
file_modify_parser.add_argument(
    "project_id", type=int, required=True, help="Project id cannot be empty"
)
file_modify_parser.add_argument(
    "old_filename", type=str, required=True, help="Filename cannot be empty"
)
file_modify_parser.add_argument(
    "new_filename", type=str, required=True, help="Filename cannot be empty"
)

file_list_parser = reqparse.RequestParser()
file_list_parser.add_argument(
    "project_id", type=int, required=True, help="Project id cannot be empty"
)
file_list_parser.add_argument("dir", type=str, default="/")

file_delete_parser = reqparse.RequestParser()
file_delete_parser.add_argument(
    "project_id", type=int, required=True, help="Project id cannot be empty"
)
file_delete_parser.add_argument(
    "filename", type=str, required=True, help="Filename cannot be empty"
)
