from flask import session
from flask_login import login_required
from flask_restful import Resource, marshal_with

from app.fields.configuration import configurations_field
from app.models.configuration import Configuration
from app.parsers.configuration import language_parser


class ResourceConfiguration(Resource):
    @marshal_with(configurations_field)
    def get(self):
        return {"data": Configuration.search(page_size=-1)["data"]}


class ResourceConfigurationLanguage(Resource):
    @login_required
    def post(self):
        args = language_parser.parse_args()
        session["lang"] = args["lang"]
        return {"message": "Change language success"}
