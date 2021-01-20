import functools

from flask_login import current_user
from flask_restful import abort

from app.models.project import Project
from app.models.user import User


def self_only(model, parser=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if kwargs.__contains__("id_"):
                base = model.get_by_id(kwargs["id_"])
                if base is None:
                    abort(
                        404, message="{} not found".format(model.__tablename__.title())
                    )
                if isinstance(base, User):
                    if (
                        current_user.permission != 1
                        and kwargs["id_"] != current_user.id
                    ):
                        abort(403)
                project = None
                if isinstance(base, Project):
                    project = base
                if getattr(base, "project_id", None):
                    project = Project.get_by_id(base.project_id)
                if (
                    project
                    and current_user.permission != 1
                    and project.user_id != current_user.id
                ):
                    abort(403)
            if parser:
                parser_args = parser.parse_args()
                if parser_args.__contains__("project_id"):
                    project = Project.get_by_id(parser_args["project_id"])
                    if project is None:
                        abort(404, message="Project not found")
                    if (
                        current_user.permission != 1
                        and project.user_id != current_user.id
                    ):
                        abort(403)
                if current_user.permission != 1 and model and issubclass(User, model):
                    abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator
