from flask_restful import fields

file_field = {
    "name": fields.String,
    "type": fields.String,
    "size": fields.Integer,
    "access_time": fields.DateTime(dt_format="iso8601"),
    "create_time": fields.DateTime(dt_format="iso8601"),
    "modify_time": fields.DateTime(dt_format="iso8601"),
}

files_field = {"data": fields.List(fields.Nested(file_field))}
