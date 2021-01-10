import os
import shutil

from flask import current_app
from flask_login import login_required
from flask_restful import Resource, abort, marshal_with

from app.fields.file import files_field
from app.libs.auth import self_only
from app.libs.helper import get_files
from app.parsers.file import (
    file_create_parser,
    file_delete_parser,
    file_list_parser,
    file_modify_parser,
)


class ResourceFile(Resource):
    @marshal_with(files_field)
    @login_required
    @self_only(None, file_list_parser)
    def get(self):
        args = file_list_parser.parse_args()
        root_dir = os.path.realpath(
            "{}/{}/user".format(
                current_app.config["FILE_DIRECTORY"], args["project_id"]
            )
        )
        file_dir = os.path.realpath(os.path.join(root_dir, args["dir"]))
        if os.path.commonpath([root_dir, file_dir]) != root_dir:
            abort(400)
        res = get_files(root_dir)
        return {"files": res}

    @login_required
    @self_only(None, file_create_parser)
    def post(self):
        args = file_create_parser.parse_args()
        root_dir = os.path.realpath(
            "{}/{}/user".format(
                current_app.config["FILE_DIRECTORY"], args["project_id"]
            )
        )
        file = args["file"]
        filename = file.filename.split("/")[-1]
        filepath = os.path.realpath(os.path.join(root_dir, args["dir"], filename))
        if os.path.commonpath([root_dir, filepath]) != root_dir:
            abort(400)
        os.makedirs(os.path.split(filepath)[0], exist_ok=True)
        file.save(filepath)
        return {"message": "Upload file success"}, 201

    @login_required
    @self_only(None, file_modify_parser)
    def put(self):
        args = file_modify_parser.parse_args()
        root_dir = os.path.realpath(
            "{}/{}/user".format(
                current_app.config["FILE_DIRECTORY"], args["project_id"]
            )
        )
        old_filepath = os.path.realpath(os.path.join(root_dir, args["old_filename"]))
        new_filepath = os.path.realpath(os.path.join(root_dir, args["new_filename"]))
        if (
            os.path.commonpath([root_dir, old_filepath]) != root_dir
            or os.path.commonpath([root_dir, new_filepath]) != root_dir
        ):
            abort(400)
        if not os.path.exists(old_filepath):
            abort(404, message="File not found")
        if os.path.exists(new_filepath):
            abort(400, message="File already exist")
        os.makedirs(os.path.split(new_filepath)[0], exist_ok=True)
        shutil.move(old_filepath, new_filepath)
        return {"message": "Modify file success"}

    @login_required
    @self_only(None, file_delete_parser)
    def delete(self):
        args = file_delete_parser.parse_args()
        root_dir = os.path.realpath(
            "{}/{}/user".format(
                current_app.config["FILE_DIRECTORY"], args["project_id"]
            )
        )
        filepath = os.path.realpath(os.path.join(root_dir, args["filename"]))
        if os.path.commonpath([root_dir, filepath]) != root_dir:
            abort(400)
        if not os.path.exists(filepath):
            abort(404, message="File not found")
        os.remove(filepath)
        return "", 204
