import pytest

from src.tree import Node, Tree


class TestNode:

    def test_create_node(self):
        operation = (
            "(at 2020-october-5 12:1:32.4338850 utc: access with last access update enabled)",
            " <- (at 2020-october-5 12:1:32.4338850 utc: access with last access update enabled)",
            "<2020-10-05T12:01:32.4338850 +0000 (At)>",
            ["access with last access update enabled"],
            "normal"
        )
        actual = Node(operation)


class TestTree:

    def test_create_tree(self):
        tree = Tree()

    def test_add_node(self):
        tree = Tree()
        operation = (
            "(at 2020-october-5 12:1:32.4338850 utc: access with last access update enabled)",
            " <- (at 2020-october-5 12:1:32.4338850 utc: access with last access update enabled)",
            "<2020-10-05T12:01:32.4338850 +0000 (At)>",
            ["access with last access update enabled"],
            "normal"
        )
        tree.add_node(operation)
        assert operation[0] in [n.operation for n in tree.tree.values()]

    def test_add_duplicate_node(self):
        tree = Tree()
        operation = (
            "(at 2020-october-5 12:1:32.4338850 utc: access with last access update enabled)",
            " <- (at 2020-october-5 12:1:32.4338850 utc: access with last access update enabled)",
            "<2020-10-05T12:01:32.4338850 +0000 (At)>",
            ["access with last access update enabled"],
            "normal"
        )
        tree.add_node(operation)
        tree.add_node(operation)
        assert len(tree.tree.keys()) == 2

