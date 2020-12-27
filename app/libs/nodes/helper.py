from app.libs.nodes.base_node import BaseNode
from app.libs.nodes.data_split_node import DataSplitNode
from app.libs.nodes.input_node import InputNode
from app.models.node import Node


def change_node(node: Node) -> BaseNode:
    node_mapping = {'input_node': InputNode, 'data_split_node': DataSplitNode}
    try:
        return node_mapping[node.node_type](
            node.id, node.node_type, node.project_id, node.in_edges,
            node.out_edges, node.extra
        )
    except KeyError:
        raise Exception(
            'Node{}({}) not support'.format(node.id, node.node_type)
        )


def run_nodes(nodes: [BaseNode], testing, thread):
    if not testing or thread:
        from flask_app import create_app
        app = create_app(test=testing)
        app.app_context().push()
    for node in nodes:
        try:
            node.run()
        except Exception as e:
            node.logger.error(e)
        finally:
            node.update()
