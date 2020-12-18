from flask_restful import fields

file_fields = {
    'id': fields.Integer,
    'project_id': fields.Integer,
    'filename': fields.String,
    'size': fields.Integer,
    'access_time': fields.DateTime(dt_format='iso8601'),
    'create_time': fields.DateTime(dt_format='iso8601'),
    'modify_time': fields.DateTime(dt_format='iso8601')
}

files_fields = {'files': fields.List(fields.Nested(file_fields))}
