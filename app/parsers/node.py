import json

from flask_restful import reqparse
from werkzeug.routing import ValidationError


def json_dict(raw):
    try:
        res = json.loads(raw)
        assert isinstance(res, dict)
        return res
    except Exception:
        raise ValidationError('data cannot decode')


node_create_parser = reqparse.RequestParser()
node_create_parser.add_argument(
    'project_id', type=int, required=True, help='Project id cannot be empty'
)
node_create_parser.add_argument(
    'node_type', type=str, required=True, help='Node type cannot be empty'
)

node_modify_parser = reqparse.RequestParser()
node_modify_parser.add_argument('extra', type=json_dict)

node_list_parser = reqparse.RequestParser()
node_list_parser.add_argument(
    'project_id', type=int, required=True, help='Project id cannot be empty'
)
