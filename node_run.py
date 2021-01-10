import os

from app import create_app
from app.models.node import Node

if __name__ == "__main__":
    create_app().app_context().push()
    node_id = os.environ.get("NODE_ID")
    node = Node.get_by_id(node_id)
    node.run()
