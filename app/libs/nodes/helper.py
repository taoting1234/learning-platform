from app.libs.nodes.input_node import InputNode


def change_node(node):
    if node.node_type == 'input_node':
        return InputNode(
            node.id, node.node_type, node.project_id, node.in_edges,
            node.out_edges, get_value(node.extra, 'input_file')
        )
    # always not run
    assert False


def get_value(extra, key):
    return extra.get(key) if extra else None
