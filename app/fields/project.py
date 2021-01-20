from flask_restful import fields

from app.fields.search import meta_field

project_field = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "tag": fields.String,
}

project_search_field = {
    "data": fields.List(fields.Nested(project_field)),
    "meta": fields.Nested(meta_field),
}
