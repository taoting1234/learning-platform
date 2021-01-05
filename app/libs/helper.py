from app.libs.global_varible import g


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


def change_columns(raw):
    # TODO 支持[-1,-2]
    res = set()
    try:
        raw = raw.replace(" ", "")
        parts = raw.split(",")
        while "" in parts:
            parts.remove("")
        for part in parts:
            if "-" in part:
                left, right = part.split("-")
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
        assert False, "column should be integer"
    return list(res)
