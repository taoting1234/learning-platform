from typing import List

from app.libs.global_varible import g
from app.nodes import node_mapping


def change_node(node):
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
        if fail_flag is False:
            try:
                node.run()
                node.finish()
                node.modify(status=2)  # 成功
            except Exception as e:
                if testing and not thread:
                    raise
                node.logger.error(e)
                fail_flag = True
        else:
            node.modify(status=3)  # 失败


def change_columns(raw: str) -> List[int]:
    res = set()
    try:
        raw = raw.replace(" ", "")
        parts = raw.split(",")
        while "" in parts:
            parts.remove("")
        for part in parts:
            if "-" in part:
                l, r = part.split("-")
                l = int(l)
                r = int(r)
                if l == r:
                    res.add(l)
                    continue
                sign = (r - l) // abs(r - l)
                res.update(set(range(l, r + sign, sign)))
            else:
                res.add(int(part))
    except ValueError:
        assert False, "column should be integer"
    return list(res)
