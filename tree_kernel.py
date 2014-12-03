#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

from networkx import DiGraph, dfs_edges, is_arborescence, topological_sort
from networkx.algorithms.traversal.depth_first_search import dfs_tree
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


def get_production_rules(syntax_tree, root_node=None):
    """
    Iterates through a tree (starting at the given node) and returns
    a set of 'production rules'. each 'rule' is a tuple, consisting of a
    node ID (str) and a tuple of it successors (str, i.e. the node IDs of all
    the nodes connected via outgoing edges) as its value.

    I put 'production rules' in quotes, as they are based on unique node IDs,
    and not necessarily on syntactic categories.

    Parameters
    ----------
    syntax_tree : networkx.DiGraph
        a tree represented as a directed graph
    root_node : str or None
        the node ID of the tree's root node. if not specified, it will be
        determined automatically.

    Returns
    -------
    rules : set of (str, tuple of str) tuples
        each rule consists of a lhs (a string representing a node ID) and a rhs
        (a tuple of strings representing node IDs)
    """
    rules = set()

    if not root_node:
        # root node is the first element in a topological sort of the graph
        root_node = topological_sort(syntax_tree)[0]

    for source, _target in dfs_edges(syntax_tree, root_node):
        rules.add( (source, tuple(sorted(syntax_tree.successors(source)))) )
    return rules


def contains_only_complete_productions(tree, subtree, subtree_root_node=None):
    """
    checks, if a syntax subtree only consists of complete productions from the
    given tree.
    """
    tree_rules = get_production_rules(tree)
    subtree_rules = get_production_rules(subtree, root_node=subtree_root_node)
    return all(st_rule in tree_rules for st_rule in subtree_rules)




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


def get_subtrees(tree):
    """
    naively generate all subtrees of a given tree, which are valid
    according to Collins and Duffy (2001).

    Parameters
    ----------
    tree : networkx.DiGraph

    Yields
    ------
    subtrees : generator of networkx.DiGraph
    """
    for n in xrange(1, tree.number_of_nodes()+1):
        for sub_nodes in itertools.combinations(tree.nodes(), n):
            subgraph = tree1.subgraph(sub_nodes)
            if nx.is_weakly_connected(subgraph):
                if is_proper(subgraph):
                    if contains_only_complete_productions(tree, subgraph):
                        yield subgraph
