from flask_restful import fields

project_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'tag': fields.String
}

projects_fields = {'projects': fields.List(fields.Nested(project_fields))}
