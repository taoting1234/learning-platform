from flask_login import current_user, login_required
from flask_restful import Resource, abort, marshal_with

from app.fields.node import node_field, nodes_field
from app.models.node import Node
from app.models.project import Project
from app.parsers.node import (
    node_create_parser,
    node_list_parser,
    node_modify_parser,
)


class ResourceNode(Resource):
    @marshal_with(node_field)
    @login_required
    def get(self, id_):
        node = Node.get_by_id(id_)
        if node is None:
            abort(404, message='Node not found')
        project = Project.get_by_id(node.project_id)
        if project.user_id != current_user.id:
            abort(403)
        return node

    @login_required
    def put(self, id_):
        node = Node.get_by_id(id_)
        if node is None:
            abort(404, message='Node not found')
        project = Project.get_by_id(node.project_id)
        if project.user_id != current_user.id:
            abort(403)
        args = node_modify_parser.parse_args()
        nodes = [i.id for i in Node.search(project_id=project.id, page_size=-1)['data']]
        for node_id in args['in_edges'] if args['in_edges'] else []:
            if node_id not in nodes:
                abort(400, message='Node not found')
        for node_id in args['out_edges'] if args['out_edges'] else []:
            if node_id not in nodes:
                abort(400, message='Node not found')
        node.modify(**args)
        return {'message': 'Modify file success'}

    @login_required
    def delete(self, id_):
        node = Node.get_by_id(id_)
        if node is None:
            abort(404, message='Node not found')
        project = Project.get_by_id(node.project_id)
        if project.user_id != current_user.id:
            abort(403)
        node.delete()
        return '', 204


class ResourceNodeList(Resource):
    @marshal_with(nodes_field)
    @login_required
    def get(self):
        args = node_list_parser.parse_args()
        project = Project.get_by_id(args['project_id'])
        if project is None:
            abort(404, message='Project not found')
        if project.user_id != current_user.id:
            abort(403)
        res = Node.search(project_id=project.id, page_size=-1)['data']
        return {'nodes': res}

    @login_required
    def post(self):
        args = node_create_parser.parse_args()
        project = Project.get_by_id(args['project_id'])
        if project is None:
            abort(404, message='Project not found')
        if project.user_id != current_user.id:
            abort(403)
        Node.create(**args)
        return {'message': 'Create node success'}, 201
