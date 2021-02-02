from uuid import uuid4
from graphviz import Digraph
from typing import Dict, List

from src.config import Config
from src.tree import Tree

NODE_TABLE_START: str = '<<TABLE border="0" cellborder="1" cellspacing="0">'
NODE_TABLE_END: str = '</TABLE>>'
NORMAL_HEADER: str = '<TR><TD PORT="header" bgcolor="black"><font color="white">'
START_HEADER: str = '<TR><TD PORT="header" bgcolor="forestgreen"><font color="black">'
HEADER_END: str = '</font></TD></TR>'       # same as ROW_END but seperate to be able to change headers and rows seperately
NORMAL_ROW_START: str = "<TR><TD><font>"
FORGERY_ROW_START: str = '<TR><TD bgcolor="red"><font color="white">'
ROW_END: str = '</font></TD></TR>'
UNKNOWN_STATE: str = '<<font color="black" point-size="50"><b>?</b></font>>'


class Visualizer:
    trees: Dict[str, Tree]
    graph: Digraph
    nodes_added: List
    output_path: str
    output_file: str
    forgery_states: List[str]

    def __init__(self, trees, out_format: str, horizontal_sep: str,
            vertical_sep: str, dpi: str, output_path: str, output_file: str,
            forgery_states: List[str] = []):
        self.trees = trees
        self.graph = Digraph("output", format=out_format,
            node_attr={"shape": "plaintext"},
            graph_attr={
                "concentrate": "true",
                "ranksep": horizontal_sep,
                "rankdir": "LR",
                "nodesep": vertical_sep,
                "dpi": dpi
            }
        )
        self.nodes_added = []
        self.output_path = output_path
        self.output_file = output_file
        self.forgery_states = forgery_states

    def _visualize_root(self, root, file):
        root_str = NODE_TABLE_START
        root_str += NORMAL_HEADER
        root_str += "NOW"
        root_str += HEADER_END
        root_str += NORMAL_ROW_START
        root_str += file
        root_str += ROW_END
        root_str += NODE_TABLE_END
        self.graph.node(root.id, root_str)

    def _visualize_node(self, node):
        node_str = NODE_TABLE_START
        
        # determine node type and generate correct header
        if node.origin_state:
            node_str += START_HEADER
        else:
            node_str += NORMAL_HEADER
        node_str += node.timestamp[11:-1]
        node_str += HEADER_END

        # add actions
        for action in node.actions:
            if action in self.forgery_states:
                node_str += FORGERY_ROW_START
            else:
                node_str += NORMAL_ROW_START
            node_str += action
            node_str += ROW_END

        # Complete node
        node_str += NODE_TABLE_END
        self.graph.node(node.id, node_str)
        self.nodes_added.append(node.id)

    def _visualize_unknown_previous_node(self, node) -> str:
        unkown_id = f"{node.id}Unknown"
        self.graph.node(unkown_id, UNKNOWN_STATE)
        return unkown_id

    def _visualize_file(self, file, tree):
        # TODO: see if the two tree walks can be combined into one
        # create root
        self._visualize_root(tree.root, file)
        
        # create nodes
        nodes_to_generate = tree.root.children.copy()
        while len(nodes_to_generate) > 0:
            current_node = nodes_to_generate.pop()
            nodes_to_generate += current_node.children.copy()
            if current_node.id not in self.nodes_added:
                self._visualize_node(current_node)

        # create relationships
        nodes_to_generate = [tree.root]
        has_unknown_previous_node = []
        while len(nodes_to_generate) > 0:
            current_node = nodes_to_generate.pop()
            nodes_to_generate += current_node.children.copy()
            for child in current_node.children:
                self.graph.edge(f"{child.id}:header",
                    f"{current_node.id}:header")
            if not current_node.children and not current_node.origin_state:
                if current_node.id not in has_unknown_previous_node:
                    unknown_id = self._visualize_unknown_previous_node(
                        current_node)
                    self.graph.edge(unknown_id, f"{current_node.id}:header")

    def visualize(self):
        for file, tree in self.trees.items():
            self._visualize_file(file, tree)
        #self.graph.view(filename=self.output_file, directory=self.output_path,
        # cleanup=True)
        self.graph.render(filename=self.output_file, directory=self.output_path,
            cleanup=True)
            