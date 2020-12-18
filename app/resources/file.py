from flask_login import current_user, login_required
from flask_restful import Resource, abort, marshal_with

from app.fields.file import file_fields, files_fields
from app.models.file import File
from app.models.project import Project
from app.parsers.file import (
    file_create_parser,
    file_list_parser,
    file_modify_parser,
)


class ResourceFile(Resource):
    @marshal_with(file_fields)
    @login_required
    def get(self, id_):
        file = File.get_by_id(id_)
        if file is None:
            abort(404, message='File not found')
        project = Project.get_by_id(file.id)
        if project.user_id != current_user.id:
            abort(403)
        return file

    @login_required
    def put(self, id_):
        file = File.get_by_id(id_)
        if file is None:
            abort(404, message='File not found')
        project = Project.get_by_id(file.id)
        if project.user_id != current_user.id:
            abort(403)
        args = file_modify_parser.parse_args()
        args['filename'] = args['filename'].lstrip('/')
        if File.search(project_id=project.id,
                       filename=args['filename'])['meta']['count']:
            abort(400, message='File already exist')
        file.modify(**args)
        return {'message': 'Modify file success'}

    @login_required
    def delete(self, id_):
        file = File.get_by_id(id_)
        if file is None:
            abort(404, message='File not found')
        project = Project.get_by_id(file.id)
        if project.user_id != current_user.id:
            abort(403)
        file.delete()
        return '', 204


class ResourceFileList(Resource):
    @marshal_with(files_fields)
    @login_required
    def get(self):
        args = file_list_parser.parse_args()
        project = Project.get_by_id(args['project_id'])
        if project is None:
            abort(404, message='Project not found')
        if project.user_id != current_user.id:
            abort(403)
        res = File.search(project_id=project.id, page_size=-1)['data']
        return {'files': res}

    @login_required
    def post(self):
        args = file_create_parser.parse_args()
        project = Project.get_by_id(args['project_id'])
        if project is None:
            abort(404, message='Project not found')
        if project.user_id != current_user.id:
            abort(403)
        File.create(**args)
        return {'message': 'Create file success'}, 201
