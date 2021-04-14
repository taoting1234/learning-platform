import json

from flask_restful import reqparse
from werkzeug.routing import ValidationError

from app.parsers.search import search_parser


def json_dict(raw):
    try:
        res = json.loads(raw)
        assert isinstance(res, dict)
        return res
    except Exception:
        raise ValidationError("data cannot decode")


node_create_parser = reqparse.RequestParser()
node_create_parser.add_argument("project_id", type=int, required=True)
node_create_parser.add_argument("node_type", type=str, required=True)

node_modify_parser = reqparse.RequestParser()
node_modify_parser.add_argument("extra", type=json_dict)

node_list_parser = reqparse.RequestParser()
node_list_parser.add_argument("project_id", type=int, required=True)

node_edge_parser = reqparse.RequestParser()
node_edge_parser.add_argument("project_id", type=int, required=True)
node_edge_parser.add_argument("node1_id", type=int, required=True)
node_edge_parser.add_argument("node2_id", type=int, required=True)

node_csv_parser = reqparse.RequestParser()
node_csv_parser.add_argument("filename", type=str, required=True)
node_csv_parser.add_argument("summary", type=bool)

node_predict_parser = search_parser.copy()
node_predict_parser.add_argument("type", type=int, required=True)
