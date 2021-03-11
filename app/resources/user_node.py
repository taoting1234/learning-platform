from flask_login import login_required
from flask_restful import Resource, marshal_with

from app.fields.user_node import user_node_field, user_nodes_field
from app.libs.auth import self_only
from app.models.node import Node
from app.models.user_node import UserNode
from app.parsers.user_node import (
    user_node_create_parser,
    user_node_import_parser,
    user_node_list_parser,
    user_node_modify_parser,
)


class ResourceUserNode(Resource):
    @login_required
    @self_only(UserNode)
    def put(self, id_):
        project = UserNode.get_by_id(id_)
        args = user_node_modify_parser.parse_args()
        project.modify(**args)
        return {"message": "Modify user node success"}

    @login_required
    @self_only(UserNode)
    def delete(self, id_):
        project = UserNode.get_by_id(id_)
        project.delete()
        return "", 204


class ResourceUserNodeList(Resource):
    @marshal_with(user_nodes_field)
    @login_required
    @self_only(UserNode, user_node_list_parser)
    def get(self):
        args = user_node_list_parser.parse_args()
        res = UserNode.search(user_id=args["user_id"], page_size=-1)["data"]
        return {"user_nodes": res}

    @marshal_with(user_node_field)
    @login_required
    @self_only(UserNode, user_node_create_parser)
    def post(self):
        args = user_node_create_parser.parse_args()
        node = Node.get_by_id(args["node_id"])
        extra = node.extra
        extra.__delitem__("x")
        extra.__delitem__("y")
        return UserNode.create(node_type=node.node_type, extra=extra, **args), 201


class ResourceUserNodeImport(Resource):
    @marshal_with(user_node_field)
    @login_required
    @self_only(UserNode, user_node_import_parser)
    def post(self):
        args = user_node_import_parser.parse_args()
        user_node = UserNode.get_user_node_by_code(args["code"])
        return (
            UserNode.create(
                name=user_node.name,
                description=user_node.description,
                node_type=user_node.node_type,
                extra=user_node.extra,
            ),
            201,
        )
