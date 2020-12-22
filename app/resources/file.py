from flask_login import current_user, login_required
from flask_restful import Resource, abort, marshal_with

from app.fields.file import file_field, files_field
from app.libs.auth import self_only
from app.models.file import File
from app.models.project import Project
from app.parsers.file import (
    file_create_parser,
    file_list_parser,
    file_modify_parser,
)


class ResourceFile(Resource):
    @marshal_with(file_field)
    @login_required
    @self_only(File)
    def get(self, id_):
        file = File.get_by_id(id_)
        return file

    @login_required
    @self_only(File)
    def put(self, id_):
        file = File.get_by_id(id_)
        project = Project.get_by_id(file.project_id)
        args = file_modify_parser.parse_args()
        args['filename'] = args['filename'].lstrip('/')
        if File.search(project_id=project.id,
                       filename=args['filename'])['meta']['count']:
            abort(400, message='File already exist')
        file.modify(**args)
        return {'message': 'Modify file success'}

    @login_required
    @self_only(File)
    def delete(self, id_):
        file = File.get_by_id(id_)
        file.delete()
        return '', 204


class ResourceFileList(Resource):
    @marshal_with(files_field)
    @login_required
    @self_only(File, file_list_parser)
    def get(self):
        args = file_list_parser.parse_args()
        res = File.search(project_id=args['project_id'], page_size=-1)['data']
        return {'files': res}

    @marshal_with(file_field)
    @login_required
    @self_only(File, file_create_parser)
    def post(self):
        args = file_create_parser.parse_args()
        file = File.create(**args)
        return file, 201
