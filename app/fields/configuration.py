from flask_restful import fields

configuration_field = {"key": fields.String, "value": fields.String}
configurations_field = {"data": fields.List(fields.Nested(configuration_field))}
