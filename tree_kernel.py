#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

from networkx import DiGraph, dfs_edges
from networkx.algorithms.traversal.depth_first_search import dfs_tree
from networkx.algorithms.tree import is_tree
from ordered_set import OrderedSet


def is_proper(tree):
    """
    returns True, iff input is a proper tree.
    A tree is proper if it contains at least one edge.
    """
    return True if len(tree.edges()) > 0 else False


def is_leave(tree, node_id):
    """returns True, if the given node is a leave node"""
    return True if tree.out_degree(node_id) == 0 else False


def get_production_rules(syntax_tree, root_node='S'):
    """
    Iterates through a tree (starting at the given node) and returns
    a dictionary of 'production rules'. each 'rule' consists of a node ID
    as its key and a list of it successors (i.e. the node IDs of all the nodes
    connected via outgoing edges) as its value.

    I put 'production rules' in quotes, as they are based on unique node IDs,
    and not necessarily on syntactic categories.
    """
    rules = {}
    dfs_nodes = OrderedSet()
    for source, target in dfs_edges(syntax_tree, root_node):
        dfs_nodes.append(source)
    for lhs in dfs_nodes:
        rules[lhs] = syntax_tree.successors(lhs)
    return rules


def contains_only_complete_productions(tree, subtree):
    """
    checks, if a syntax subtree only consists of complete productions from the
    given tree.
    """
    assert is_tree(tree)
    for node_id in subtree.nodes_iter():
        production = []
        # in a tree, each node can only have one parent
        parent, _this = tree.in_edges(node_id)[0]
        production.append(parent)
        # siblings = all children of parent, incl. node_id
        production.extend(tree.successors(parent))
        for node in production:
            if node not in subtree:
                return False
    return True



def get_proper_corooted_subtrees(tree, root_node):
    """
    """
    if not is_proper(tree):
        return []

    # base case for the recursion:
    # a leave node has no proper, co-rooted subtrees
    if is_leave(tree, root_node):
        return []

    subtrees = []
    for child_node in tree.successors(root_node):
        # cf. http://stackoverflow.com/questions/7892144/subtree-with-networkx
        child_subtree = dfs_tree(tree, child_node)
        subtrees.append(child_subtree)
        subtrees.extend(get_proper_corooted_subtrees(child_subtree, child_node))
    return subtrees


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


def get_syntax_subtrees(tree, root_node='S', debug_dir='/tmp/subtrees'):
    """
    Collins and Duffy (2001) define a subtree to be any subgraph, which
    includes more than one node. A subtree must not include partial rule
    productions, i.e. [NP [D the]] is not a subtree, while
    [NP [D the] [N apple]] and [D the] are subtrees.

    cf. Collins and Duffy (2001). Convolution Kernels for Natural Language.
    """
    import os
    from networkx import write_dot

    def is_subtree(tree, subtree, subtree_root_node):
        if len(subtree.nodes()) < 2:
            return False
        elif not contains_only_complete_productions(tree, subtree):
            return False
        else:
            return True

    subtrees = []
    for i, child_node in enumerate(tree.successors(root_node)):
        # cf. http://stackoverflow.com/questions/7892144/subtree-with-networkx
        child_subgraph = dfs_tree(tree, child_node)
        if debug_dir:
            write_dot(child_subgraph, os.path.join(debug_dir, 'subtree-{}.dot'.format(i)))
        if is_subtree(tree, child_subgraph, child_node):
            subtrees.append(child_subgraph)
    return subtrees


def count_syntax_subtrees(tree, root_node):
    return len(get_syntax_subtrees(tree, root_node))
