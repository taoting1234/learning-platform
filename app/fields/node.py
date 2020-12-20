from flask_restful import fields

node_field = {
    'id': fields.Integer,
    'project_id': fields.Integer,
    'node_type': fields.String,
    'input_shape': fields.List(fields.Integer),
    'output_shape': fields.List(fields.Integer),
    'in_edges': fields.List(fields.Integer),
    'out_edges': fields.List(fields.Integer),
    'status': fields.Integer,
    'extra': fields.Raw
}

nodes_field = {'nodes': fields.List(fields.Nested(node_field.copy()))}

node_field.update({'log': fields.String(default='')})
