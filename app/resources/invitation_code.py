from flask_login import current_user, login_required
from flask_restful import Resource, abort, marshal_with

from app.fields.invitation_code import invitation_code_field, invitation_codes_field
from app.models.invitation_code import InvitationCode
from app.parsers.invitation_code import invitation_code_list_parser


class ResourceInvitationCode(Resource):
    @login_required
    def delete(self, id_):
        invitation_code = InvitationCode.get_by_id(id_)
        if invitation_code is None:
            abort(404, message="invitation code not found")
        if invitation_code.is_used:
            abort(400, message="invitation code already used")
        invitation_code.delete()
        return "", 204


class ResourceInvitationCodeList(Resource):
    @marshal_with(invitation_codes_field)
    @login_required
    def get(self):
        args = invitation_code_list_parser.parse_args()
        res = InvitationCode.search(**args)
        return res

    @marshal_with(invitation_code_field)
    @login_required
    def post(self):
        if not current_user.permission:
            abort(403)
        return InvitationCode.create(), 201
