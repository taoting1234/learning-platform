from flask_restful import fields

from app.fields.search import meta_field

user_field = {
    "id": fields.Integer,
    "username": fields.String,
    "organization": fields.String,
    "permission": fields.Integer,
    "block": fields.Integer,
}

user_search_field = {
    "data": fields.List(fields.Nested(user_field)),
    "meta": fields.Nested(meta_field),
}
