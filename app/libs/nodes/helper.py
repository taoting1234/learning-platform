from app.libs.nodes.data_split_node import DataSplitNode
from app.libs.nodes.input_node import InputNode
from app.libs.nodes.models.linear_regression_node import LinearRegressionNode
from app.libs.nodes.models.logistic_regression_node import (
    LogisticRegressionNode,
)


def change_node(node):
    node_mapping = {
        'input_node': InputNode,
        'data_split_node': DataSplitNode,
        'linear_regression_node': LinearRegressionNode,
        'logistic_regression_node': LogisticRegressionNode
    }
    try:
        return node_mapping[node.node_type](
            node.id, node.node_type, node.project_id, node.in_edges,
            node.out_edges, node.extra
        )
    except KeyError:
        raise Exception(
            'Node{}({}) not support'.format(node.id, node.node_type)
        )


def run_nodes(nodes, testing, thread):
    if not testing or thread:
        from flask_app import create_app
        app = create_app(test=testing)
        app.app_context().push()
    for node in nodes:
        try:
            node.run()
        except Exception as e:
            if testing:
                raise Exception(e)
            node.logger.error(e)
        finally:
            node.update()
