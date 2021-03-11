from flask_restful import fields

user_node_field = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "code": fields.String,
    "node_type": fields.String,
    "extra": fields.Raw,
}
user_nodes_field = {"user_nodes": fields.List(fields.Nested(user_node_field.copy()))}
