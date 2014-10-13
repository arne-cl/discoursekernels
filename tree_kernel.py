#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

from networkx import DiGraph
from networkx.algorithms.traversal.depth_first_search import dfs_tree


def is_proper(tree):
    """returns True, iff input is a proper tree"""
    return True if len(tree.edges()) > 0 else False


def is_leave(tree, node_id):
    """returns True, if the given node is a leave node"""
    return True if tree.out_degree(node_id) == 0 else False


def generate_example_tree():
    """creates a tree/networkx.DiGraph of a syntactic parse tree"""
    tree = DiGraph()
    tree.add_nodes_from(['S', 'NP-1', 'N-1', 'Jeff', 'VP', 'V', 'ate', 'NP-2', 'D',
                         'the', 'N-2', 'apple'])
    tree.add_edges_from([('S', 'NP-1'), ('NP-1', 'N-1'), ('N-1', 'Jeff'),
                         ('S', 'VP'), ('VP', 'V'), ('V', 'ate'),
                         ('VP', 'NP-2'), ('NP-2', 'D'), ('D', 'the'),
                         ('NP-2', 'N-2'), ('N-2', 'apple')])
    return tree


def get_production_rules(syntax_tree, root_node='S'):
    raise NotImplementedError


def contains_only_complete_productions(tree, subtree, tree_root, subtree_root):
    raise NotImplementedError


def count_proper_corooted_subtrees(tree, root_node):
    """
    Count the number of proper, co-rooted subtrees of the given input tree.
    A proper tree has at least one edge.

    (Shawe-Taylor and Cristianini 2004, p.385)

    Parameters
    ----------
    tree : DiGraph
        a tree represented as a directed graph
    """
    if not is_proper(tree):
        return 0

    # base case for the recursion:
    # a leave node has no proper, co-rooted subtrees
    if is_leave(tree, root_node):
        return 0

    subtree_count = 1  # neutral element of multiplation
    for child_node in tree.successors(root_node):
        # cf. http://stackoverflow.com/questions/7892144/subtree-with-networkx
        child_subtree = dfs_tree(tree, child_node)
        subtree_count *= count_proper_corooted_subtrees(child_subtree, child_node) + 1
    return subtree_count


def get_syntax_subtrees(tree, root_node='S'):
    """
    Collins and Duffy (2001) define a subtree to be any subgraph, which
    includes more than one node. A subtree must not include partial rule
    productions, i.e. [NP [D the]] is not a subtree, while
    [NP [D the] [N apple]] and [D the] are subtrees.

    cf. Collins and Duffy (2001). Convolution Kernels for Natural Language.
    """
    def is_subtree(tree, subtree, subtree_root_node):
        if len(subtree.nodes()) < 2:
            return False
        elif not contains_only_complete_productions(tree, subtree, tree_root,
                                                    subtree_root):
            return False
        else:
            return True
    raise NotImplementedError


def count_syntax_subtrees(tree, root_node):
    return len(get_syntax_subtrees(tree, root_node))
