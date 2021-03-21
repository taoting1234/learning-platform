from flask_restful import fields

from app.fields.search import meta_field

invitation_code_field = {
    "id": fields.Integer,
    "code": fields.String,
    "user_id": fields.Integer,
    "is_used": fields.Boolean,
}

invitation_codes_field = {
    "data": fields.List(fields.Nested(invitation_code_field.copy())),
    "meta": fields.Nested(meta_field),
}
