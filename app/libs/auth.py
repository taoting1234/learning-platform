import functools

from flask_login import current_user
from flask_restful import abort

from app.models.project import Project


def self_only(model, parser=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if kwargs.get("id_"):
                base = model.get_by_id(kwargs["id_"])
                if base is None:
                    abort(
                        404, message="{} not found".format(model.__tablename__.title())
                    )
                project = None
                if isinstance(base, Project):
                    project = base
                if getattr(base, "project_id", None):
                    project = Project.get_by_id(getattr(base, "project_id"))
                if project and project.user_id != current_user.id:
                    abort(403)
            if parser:
                project = Project.get_by_id(parser.parse_args()["project_id"])
                if project is None:
                    abort(404, message="Project not found")
                if project.user_id != current_user.id:
                    abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator
