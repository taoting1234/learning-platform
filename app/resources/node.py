from flask_login import login_required
from flask_restful import Resource, marshal_with

from app.fields.node import node_field, nodes_field
from app.libs.auth import self_only
from app.models.node import Node
from app.parsers.node import (
    node_create_parser,
    node_list_parser,
    node_modify_parser,
)


class ResourceNode(Resource):
    @marshal_with(node_field)
    @login_required
    @self_only(Node)
    def get(self, id_):
        node = Node.get_by_id(id_)
        return node

    @login_required
    @self_only(Node)
    def put(self, id_):
        node = Node.get_by_id(id_)
        args = node_modify_parser.parse_args()
        node.modify(**args)
        return {'message': 'Modify file success'}

    @login_required
    @self_only(Node)
    def delete(self, id_):
        node = Node.get_by_id(id_)
        node.delete()
        return '', 204


class ResourceNodeList(Resource):
    @marshal_with(nodes_field)
    @login_required
    @self_only(Node, node_list_parser)
    def get(self):
        args = node_list_parser.parse_args()
        res = Node.search(project_id=args['project_id'], page_size=-1)['data']
        return {'nodes': res}

    @marshal_with(node_field)
    @login_required
    @self_only(Node, node_create_parser)
    def post(self):
        args = node_create_parser.parse_args()
        node = Node.create(**args)
        return node, 201
