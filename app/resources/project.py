from flask_login import current_user, login_required
from flask_restful import Resource, abort, marshal_with

from app.fields.project import project_field, projects_field
from app.libs.auth import self_only
from app.models.project import Project
from app.parsers.project import project_create_parser, project_modify_parser


class ResourceProject(Resource):
    @marshal_with(project_field)
    @login_required
    @self_only(Project)
    def get(self, id_):
        project = Project.get_by_id(id_)
        return project

    @login_required
    @self_only(Project)
    def put(self, id_):
        project = Project.get_by_id(id_)
        args = project_modify_parser.parse_args()
        if Project.search(user_id=current_user.id,
                          name=args['name'])['meta']['count']:
            abort(400, message='Project already exist')
        project.modify(**args)
        return {'message': 'Modify project success'}

    @login_required
    @self_only(Project)
    def delete(self, id_):
        project = Project.get_by_id(id_)
        project.delete()
        return '', 204


class ResourceProjectList(Resource):
    @marshal_with(projects_field)
    @login_required
    def get(self):
        res = Project.search(user_id=current_user.id, page_size=-1)['data']
        return {'projects': res}

    @login_required
    def post(self):
        args = project_create_parser.parse_args()
        if Project.search(user_id=current_user.id,
                          name=args['name'])['meta']['count']:
            abort(400, message='Project already exist')
        Project.create(user_id=current_user.id, **args)
        return {'message': 'Create project success'}, 201
