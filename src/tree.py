from typing import List, Dict
from hashlib import sha512

from src.parser import Parser


class Node:
    id: str
    operation: str
    path: str
    timestamp: str
    actions: List[str]
    children: List
    origin_state: bool

    def __init__(self, operation: tuple):
        self.operation = operation[0]
        self.id = Node.generate_id(operation[1], operation[4])
        self.path = operation[1]
        self.timestamp = operation[2]
        self.actions = operation[3]
        self.children = []
        if operation[4] == "origin":
            self.origin_state = True
        else:
            self.origin_state = False

    @staticmethod
    def generate_id(path: str, state: str = "normal") -> str:
        return sha512(f"{path}:{state}".encode()).hexdigest()
        
    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"<Node: {self.timestamp} {self.actions} ({self.path})>"


class Tree:
    tree: Dict
    root: Node

    def __init__(self, filename: str = ""):
        self.tree = {}
        self.root = Node(("ROOT", " <- ", "NOW", [filename], "normal"))
        self.tree.update({self.root.id: self.root})
        
    def add_node(self, operation: tuple, parent: tuple = None):
        node = self.get_node(operation)
        node_created = False
        if not node:
            node = Node(operation)
            node_created = True
                    
        # If no explicit parent is given, it is linked to the root
        # node
        if not parent:
            parent = self.root
        else:
            parent = self.get_node(parent)
        if not parent:
            raise ValueError("Parent not found")
        
        if node_created:
            self.tree.update({node.id: node})
            parent.add_child(node)

    def get_node(self, node: str) -> Node:
        node_id = Node.generate_id(node[1], node[4]) 
        node = self.tree.get(node_id)
        return node


def generate_trees(lines: List[tuple]) -> Dict[str, Tree]:
    trees = {}
    for line in lines:
        if line[0] not in trees:
            tree = Tree()
            trees.update({line[0]: tree})
        else:
            tree = trees.get(line[0])

        prev_op = None
        for op in line[1]:
            tree.add_node(op, prev_op)
            if op[4] == "normal":
                prev_op = op
    return trees
        