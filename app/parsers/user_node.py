from flask_restful import reqparse

user_node_modify_parser = reqparse.RequestParser()
user_node_modify_parser.add_argument("name", type=str)
user_node_modify_parser.add_argument("description", type=str)
user_node_modify_parser.add_argument("reset_code", type=bool)

user_node_list_parser = reqparse.RequestParser()
user_node_list_parser.add_argument(
    "user_id", type=int, required=True, help="User id cannot be empty"
)

user_node_create_parser = reqparse.RequestParser()
user_node_create_parser.add_argument(
    "name", type=str, required=True, help="Name cannot be empty"
)
user_node_create_parser.add_argument(
    "description", type=str, required=True, help="Description cannot be empty"
)
user_node_create_parser.add_argument(
    "node_id", type=int, required=True, help="Node id cannot be empty"
)

user_node_import_parser = reqparse.RequestParser()
user_node_import_parser.add_argument(
    "code", type=str, required=True, help="Code cannot be empty"
)