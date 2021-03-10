from io import StringIO

import pandas as pd
from flask import current_app
from flask_login import login_required
from flask_restful import Resource, abort, marshal_with

from app.fields.node import (
    node_csv_field,
    node_field,
    nodes_description_field,
    nodes_field,
)
from app.libs.auth import self_only
from app.models.node import Node
from app.nodes import node_mapping
from app.parsers.node import (
    node_create_parser,
    node_csv_parser,
    node_edge_parser,
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
        # 巨大的bug
        # nodes = node.get_nodes(node, 2)
        # for node in nodes:
        #     node.modify(status=Node.Status.NOT_RUN)
        return {"message": "Modify node success"}

    @login_required
    @self_only(Node)
    def delete(self, id_):
        node = Node.get_by_id(id_)
        node.delete()
        return "", 204


class ResourceNodeList(Resource):
    @marshal_with(nodes_field)
    @login_required
    @self_only(Node, node_list_parser)
    def get(self):
        args = node_list_parser.parse_args()
        res = Node.search(project_id=args["project_id"], page_size=-1)["data"]
        return {"nodes": res}

    @marshal_with(node_field)
    @login_required
    @self_only(Node, node_create_parser)
    def post(self):
        args = node_create_parser.parse_args()
        node = Node.create(**args)
        return node, 201


class ResourceNodeEdge(Resource):
    @login_required
    @self_only(Node, node_edge_parser)
    def post(self):
        args = node_edge_parser.parse_args()
        node1 = Node.get_by_id(args["node1_id"])
        node2 = Node.get_by_id(args["node2_id"])
        if node1 is None or node2 is None:
            abort(400, message="Node not found")
        if (
            node1.project_id != args["project_id"]
            or node2.project_id != args["project_id"]
        ):
            abort(403)
        out_edges = node1.out_edges
        in_edges = node2.in_edges
        if out_edges.count(node2.id):
            abort(400, message="Edge already exist")
        out_edges.append(node2.id)
        in_edges.append(node1.id)
        node1.modify(out_edges=out_edges)
        node2.modify(in_edges=in_edges)
        return {"message": "Create edge success"}, 201

    @login_required
    @self_only(Node, node_edge_parser)
    def delete(self):
        args = node_edge_parser.parse_args()
        node1 = Node.get_by_id(args["node1_id"])
        node2 = Node.get_by_id(args["node2_id"])
        if node1 is None or node2 is None:
            abort(400, message="Node not found")
        if (
            node1.project_id != args["project_id"]
            or node2.project_id != args["project_id"]
        ):
            abort(403)
        try:
            out_edges = node1.out_edges
            out_edges.remove(node2.id)
            node1.modify(out_edges=out_edges)
            in_edges = node2.in_edges
            in_edges.remove(node1.id)
            node2.modify(in_edges=in_edges)
        except ValueError:
            abort(400, message="Edge not found")
        return "", 204


class ResourceNodeRun(Resource):
    @login_required
    @self_only(Node)
    def post(self, id_):
        node = Node.get_by_id(id_)
        try:
            node.run()
        except Exception as e:
            if current_app.config["TESTING"]:
                raise  # pragma: no cover
            abort(400, message=str(e))
        return {"message": "Create task success"}, 201


class ResourceNodeCSV(Resource):
    @login_required
    @marshal_with(node_csv_field)
    @self_only(Node)
    def get(self, id_):
        args = node_csv_parser.parse_args()
        node = Node.get_by_id(id_)
        try:
            df = pd.read_csv(node.join_path(args["filename"]))
            if args["summary"]:
                data = df.describe(percentiles=[0.1 * (i + 1) for i in range(10)])
            else:
                data = df.head(100)
            s_io = StringIO()
            data.to_csv(s_io)
            return {"data": s_io.getvalue()}
        except OSError:
            abort(400, message="File not found")


class ResourceNodeDescription(Resource):
    @login_required
    @marshal_with(nodes_description_field)
    def get(self):
        res = []
        for k, v in node_mapping.items():
            tmp = {}
            for name in dir(v):
                tmp[name] = getattr(v, name, None)
            res.append({"type": k, **tmp})
        return {"data": res}
