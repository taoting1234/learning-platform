from flask_restful import fields

project_field = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'tag': fields.String
}

projects_field = {'projects': fields.List(fields.Nested(project_field))}
