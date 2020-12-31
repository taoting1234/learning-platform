from app.libs.global_varible import g
from app.libs.nodes import node_mapping


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
    for node in nodes:
        try:
            node.run()
        except Exception as e:
            if testing:
                raise
            node.logger.error(e)
        finally:
            node.update()
