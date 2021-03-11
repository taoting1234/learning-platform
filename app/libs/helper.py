import datetime
import os
import random
import string
import sys
import traceback

from app.libs.global_varible import g
from app.models.node import Node


def change_node(node):
    from app.nodes import node_mapping

    try:
        return node_mapping[node.node_type](
            node.id,
            node.node_type,
            node.project_id,
            node.in_edges,
            node.out_edges,
            node.extra,
        )
    except KeyError:
        raise Exception("Node{}({}) not support".format(node.id, node.node_type))


def run_nodes(nodes, testing, thread):
    if not testing or thread:
        from flask_app import create_app

        app = create_app(
            test=testing, file_directory=getattr(g, "file_directory", None)
        )
        app.app_context().push()
    fail_flag = False
    for node in nodes:
        old_stdout = sys.stdout
        sys.stdout = open(node.join_path("log.txt"), "w")
        print("node-{}({}) run start".format(node.id, node.node_type))
        if fail_flag is False:
            try:
                node.run()
                node.finish()
                node.modify(status=Node.Status.FINISH)  # 成功
                print("node-{}({}) run success".format(node.id, node.node_type))
            except Exception as e:
                if testing and not thread:
                    raise  # pragma: no cover
                print(traceback.format_exc())
                fail_flag = True
                node.modify(status=Node.Status.FAILED)  # 失败
                print("node-{}({}) run failed: 节点运行出错".format(node.id, node.node_type))
        else:
            print("node-{}({}) run failed: 前序节点运行出错".format(node.id, node.node_type))
            node.modify(status=Node.Status.FAILED)  # 失败
        print("node-{}({}) run finish".format(node.id, node.node_type))
        sys.stdout = old_stdout


def change_columns(raw):
    res = set()
    try:
        raw = raw.replace(" ", "")
        parts = raw.split(",")
        while "" in parts:
            parts.remove("")
        for part in parts:
            if ":" in part:
                left, right = part.split(":")
                left = int(left)
                right = int(right)
                if left == right:
                    res.add(left)
                    continue
                sign = (right - left) // abs(right - left)
                res.update(set(range(left, right + sign, sign)))
            else:
                res.add(int(part))
    except ValueError:
        raise Exception("column should be integer")
    return list(res)


def get_files(path):
    res = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            res.append(
                {
                    "name": filename,
                    "type": "file",
                    "size": os.path.getsize(filepath),
                    "access_time": datetime.datetime.fromtimestamp(
                        os.path.getatime(filepath)
                    ),
                    "create_time": datetime.datetime.fromtimestamp(
                        os.path.getctime(filepath)
                    ),
                    "modify_time": datetime.datetime.fromtimestamp(
                        os.path.getmtime(filepath)
                    ),
                }
            )
        elif os.path.isdir(filepath):
            res.append({"name": filename, "type": "dir"})
    return res


def get_random_string(length):
    return "".join(random.sample(string.ascii_letters + string.digits, length))
