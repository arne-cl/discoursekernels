#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

import itertools
import networkx as nx
from networkx.algorithms import isomorphism as iso
from networkx import DiGraph, dfs_edges, is_arborescence, topological_sort
from networkx.algorithms.traversal.depth_first_search import dfs_tree
from ordered_set import OrderedSet


def generate_all_unique_subtrees(*trees):
    node_attrib = 'label'
    same_node_label = iso.categorical_node_match(node_attrib, '')
    if len(trees) == 0:
        return []
    elif len(trees) == 1:
        return list(get_subtrees(trees[0], node_attrib=node_attrib))
    else:
        unique_subtrees = list(get_subtrees(trees[0], node_attrib=node_attrib))
        for tree in trees[1:]:
            for subtree in get_subtrees(tree, node_attrib=node_attrib):
                # match each new subtree against all subtrees already in unique_subtrees
                # if it is not isomorphic (incl. matching node labels) to any of the existing
                # subtrees, it will be added to the list
                if not any(nx.is_isomorphic(new_subtree, old_subtree, node_match=same_node_label)
                           for new_subtree, old_subtree in itertools.product([subtree], unique_subtrees)):
                    unique_subtrees.append(subtree)
        return unique_subtrees


def is_rooted_at_node(tree, subtree, tree_node, node_attrib=None):
    """
    Indicator function $I_i(n)$: Is the subtree i rooted at node n (of the tree)?
    
    Returns
    -------
    is_rooted : int
        Returns 1, iff all rule productions of the subtree can be found in the
        set of production rules of the tree (starting at node n / ``tree_node``) and
        iff the tree_node n and the subtree's root node are equal
        (same node labels if node_attrib is given, otherwise: same node IDs).
        Otherwise, returns 0.
    """
    # the root node of a tree is the first element in a topological sort of the tree
    subtree_root_node = topological_sort(subtree)[0]
    
    # a subtree can only be rooted at a tree's tree_node (n),
    # if the tree node and the subtree root node are equal
    if node_attrib:
        if tree.node[tree_node][node_attrib] != subtree.node[subtree_root_node][node_attrib]:
            return 0
    else:
        if tree_node != subtree_root_node:
            return 0

    tree_subtree_rules = get_production_rules(tree, root_node=tree_node, node_attrib=node_attrib)
    subtree_rules = get_production_rules(subtree, node_attrib=node_attrib)
    if all(st_rule in tree_subtree_rules for st_rule in subtree_rules):
        return 1
    else:
        return 0


def count_tree_fragment_occurances(tree, subtree, node_attrib='label'):
    """
    $h_i(T_1)$ : how often does subtree i occur in Tree 1?
    """
    counter = 0
    for node in tree.nodes_iter():
        # is_rooted() returns one if the productions of the subtree and
        # the productions of the tree (beginning at "node") are the same
        counter += is_rooted_at_node(tree, subtree, tree_node=node,
                                     node_attrib=node_attrib)
    return counter


def common_subtrees(tree1, tree2, n1, n2, node_attrib='label'):
    """
    function $C(n_1, n_2)$ simply counts the number of
    _common subtrees_ rooted at both $n_1$ and $n_2$
    and is defined as $\sum_i I_i(n_1) I_i(n_2)$
    """
    n1_rules = get_production_rules(tree1, n1, node_attrib=node_attrib)
    n2_rules = get_production_rules(tree2, n2, node_attrib=node_attrib)
    
    if min(len(n1_rules), len(n2_rules)) < 1:
        # this condition isn't explicitly mentioned in Collins and Duffy (2001),
        # but they state that a valid subtree must have more than one node
        # if a subtree has no production rules, it only consists of leave nodes
        return 0
    
    if n1_rules != n2_rules:
        return 0
    else:  # n1_rules == n2_rules
        if is_preterminal(tree1, n1) and is_preterminal(tree2, n2):
            return 1
        else:  # n1 and/or n2 aren't preterminals
            n1_children = tree1.successors(n1)
            n2_children = tree1.successors(n2)
            assert len(n1_children) == len(n2_children)
            result = 1  # neutral element of multiplication
            for j, n1_child_node in enumerate(n1_children):
                result *= 1 + common_subtrees(tree1, tree2, n1_child_node, n2_children[j])
            return result


def tree_kernel_polynomial(tree1, tree2, node_attrib='label'):
    """
    \sum_{n_1 \in N_1} \sum_{n_2 \in N_2} C(n_1, n_2)
    """
    common_sts = 0
    for tree1_node in tree1.nodes_iter():
        for tree2_node in tree2.nodes_iter():
            common_sts += common_subtrees(tree1, tree2, tree1_node, tree2_node, node_attrib=node_attrib)
    return common_sts


def tree_kernel_naive(tree1, tree2, node_attrib='label'):
    """
    \sum_{n_1 \in N_1} \sum_{n_2 \in N_2} \sum_i I_i(n_1) I_i(n_2)
    """
    all_subtrees = generate_all_unique_subtrees(tree1, tree2)
    common_sts = 0
    for tree1_node in tree1.nodes_iter():
        for tree2_node in tree2.nodes_iter():
            for subtree in all_subtrees:
                common_sts += is_rooted_at_node(tree1, subtree, tree1_node) * is_rooted_at_node(tree2, subtree, tree2_node)
    return common_sts


def find_all_common_subtrees_bruteforce(tree1, tree2, node_attrib=None):
    """
    returns a list of all valid subtrees (Collins and Duffy 2001)
    that occur in both given trees.
    
    two subtrees are considered equal, iff they have the same structure
    and their node labels are identical.
    """
    same_node_label = iso.categorical_node_match('label', '')
    tree1_subtrees = get_subtrees(tree1, node_attrib=node_attrib)
    tree2_subtrees = get_subtrees(tree2, node_attrib=node_attrib)
    common_subtrees = []
    for (subtree1, subtree2) in itertools.product(tree1_subtrees, tree2_subtrees):
        if nx.is_isomorphic(subtree1, subtree2, node_match=same_node_label):
            common_subtrees.append(subtree1)
    return common_subtrees


def is_preterminal(tree, node):
    """
    returns True, if the given node is a preterminal in the given tree.
    False, otherwise.
    """
    if tree.out_degree(node) == 1:
        if is_leave(tree, tree.successors(node)[0]):
            return True
    else:
        return False


def is_proper(tree):
    """
    returns True, iff input is a proper tree.
    A tree is proper if it contains at least one edge.
    """
    return True if len(tree.edges()) > 0 else False


def is_leave(tree, node_id):
    """returns True, if the given node is a leave node"""
    return True if tree.out_degree(node_id) == 0 else False


def get_production_rules(syntax_tree, root_node=None, node_attrib=None):
    """
    Iterates through a tree (starting at the given node) and returns
    a set of 'production rules'. each 'rule' is a represented as a tuple,
    e.g. the rule ``S -> NP VP`` is represented by ('S', ('NP', 'VP')).
    The left-hand side of the rule is extracted from the given attribute of a
    node, while the right-hand side is extracted from the same node attribute
    of the node's successors (i.e. the nodes connected via outgoing edges).

    If no node attribute is given, the rules will be extracted from the node
    IDs of the tree.

    Parameters
    ----------
    syntax_tree : networkx.DiGraph
        a tree represented as a directed graph
    root_node : str or None
        the node ID of the tree's root node. if not specified, it will be
        determined automatically.
    node_attrib : str or None
        If a node attribute is given (e.g. 'label'), its value is used for
        generating the production rules. Otherwise, the node IDs are used.

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

    if node_attrib:
        for source, _target in dfs_edges(syntax_tree, root_node):
            source_attrib = syntax_tree.node[source][node_attrib]
            target_ids = sorted(syntax_tree.successors(source))
            target_attribs = tuple(syntax_tree.node[tid][node_attrib]
                                   for tid in target_ids)
            rules.add( (source_attrib, target_attribs) )

    else:  # rules will be generated from node IDs
        for source, _target in dfs_edges(syntax_tree, root_node):
            rules.add( (source, tuple(sorted(syntax_tree.successors(source)))) )

    return rules


def contains_only_complete_productions(tree, subtree, subtree_root_node=None,
                                       node_attrib=None):
    """
    checks, if a syntax subtree only consists of complete productions from the
    given tree.

    Parameters
    ----------
    tree : networkx.DiGraph
        a tree represented as a directed graph
    subtree : networkx.DiGraph
        a (sub)tree represented as a directed graph
    subtree_root_node : str or None
        the node ID of the subtree's root node. if not specified, it will be
        determined automatically.
    node_attrib : str or None
        If a node attribute is given (e.g. 'label'), its value is used for
        generating the production rules. Otherwise, the node IDs are used.
    """
    tree_rules = get_production_rules(tree, node_attrib=node_attrib)
    subtree_rules = get_production_rules(subtree, root_node=subtree_root_node,
                                         node_attrib=node_attrib)
    return all(st_rule in tree_rules for st_rule in subtree_rules)




def get_proper_corooted_subtrees(tree, root_node=None):
    """
    """
    if not root_node:
    # the root node of a tree is the first element in a topological sort
    # of the tree
        root_node = topological_sort(tree)[0]

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


def get_subtrees(tree, node_attrib=None):
    """
    naively generate all subtrees (tree fragments) of a given tree, which are
    valid according to Collins and Duffy (2001).

    Parameters
    ----------
    tree : networkx.DiGraph
        a tree represented as a digraph
    node_attrib : str or None
        If a node attribute is given (e.g. 'label'), its value is used for
        generating the production rules. Otherwise, the node IDs are used.
        (Generating rules from node attributes should be faster. Node
        attributes can occur repeatedly (e.g. 'NP'), while node IDs must be
        unique (e.g. 'NP-23').

    Yields
    ------
    subtrees : generator of networkx.DiGraph

    See further
    -----------
    is_treefragment()
    """
    for n in xrange(1, tree.number_of_nodes()+1):
        for sub_nodes in itertools.combinations(tree.nodes(), n):
            subgraph = tree.subgraph(sub_nodes)
            if is_treefragment(tree, subgraph, node_attrib=node_attrib):
                yield subgraph


def is_treefragment(tree, tree_fragment, node_attrib=None):
    """
    returns True, iff the given tree fragment is a valid subtree
    (according to Collins and Duffy 2001) of the given tree::

        - the subtree must contain more than one node
        - the subtree must only consist of full rule productions of the given
          tree (e.g. ``S -> NP VP`` is fine, but ``S -> VP`` isn't -- unless
          the given tree contains such a rule)

    Additionally, we check if the subtree is connected (weakly connected,
    since it is represented as a digraph).

    Parameter
    ---------
    tree : networkx.DiGraph
        a tree represented as a digraph
    tree_fragment : networkx.DiGraph
        a (sub)tree represented as a digraph
    node_attrib : str or None
        If a node attribute is given (e.g. 'label'), its value is used for
        generating the production rules. Otherwise, the node IDs are used.
        (Generating rules from node attributes should be faster. Node
        attributes can occur repeatedly (e.g. 'NP'), while node IDs must be
        unique (e.g. 'NP-23').
    """
    if nx.is_weakly_connected(tree_fragment):
        if is_proper(tree_fragment):
            if contains_only_complete_productions(tree, tree_fragment,
                                                  node_attrib=node_attrib):
                return True
    return False
