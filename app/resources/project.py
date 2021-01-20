from flask import current_app
from flask_login import current_user, login_required
from flask_restful import Resource, abort, marshal_with

from app.fields.project import project_field, project_search_field
from app.libs.auth import self_only
from app.models.project import Project
from app.parsers.project import (
    project_create_parser,
    project_modify_parser,
    project_search_parser,
)


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
        if Project.search(user_id=current_user.id, name=args["name"])["meta"]["count"]:
            abort(400, message="Project already exist")
        project.modify(**args)
        return {"message": "Modify project success"}

    @login_required
    @self_only(Project)
    def delete(self, id_):
        project = Project.get_by_id(id_)
        project.delete()
        return "", 204


class ResourceProjectList(Resource):
    @marshal_with(project_search_field)
    @login_required
    @self_only(Project, project_search_parser)
    def get(self):
        args = project_search_parser.parse_args()
        res = Project.search(**args)
        return res

    @marshal_with(project_field)
    @login_required
    def post(self):
        args = project_create_parser.parse_args()
        if Project.search(user_id=current_user.id, name=args["name"])["meta"]["count"]:
            abort(400, message="Project already exist")
        project = Project.create(user_id=current_user.id, **args)
        return project, 201


class ResourceProjectRun(Resource):
    @login_required
    @self_only(Project)
    def post(self, id_):
        project = Project.get_by_id(id_)
        try:
            project.run()
        except Exception as e:
            if current_app.config["TESTING"]:
                raise  # pragma: no cover
            abort(400, message=str(e))
        return {"message": "Create task success"}, 201
