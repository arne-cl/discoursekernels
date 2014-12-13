#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

import itertools
from collections import defaultdict

import networkx as nx
from networkx.algorithms import isomorphism as iso

from discoursegraphs.util import ensure_utf8


def dependency_children(dependency_graph, node, edge_attrib='label'):
    """
    Parameters
    ----------
    dependency_graph : networkx.DiGraph
        a dependency graphs
    node : str or int
        a node ID from the dependency graph
    edge_attrib : str
        the name of the edge attribute, which contains the dependency
        relation

    Returns
    -------
    children : set of (str, str/int)
        (relation name, target node ID) tuples, representing the nodes that
        can be reached from the given node.

    TODO: replace @memoize with an lru_cache implementation that can handle
    multiple args and keyword args.
    """
    children = set()
    for source, target, edge_attrs in dependency_graph.out_edges(node, data=True):
        children.add( (edge_attrs[edge_attrib], target) )
    return children


def common_dependency_targets(graph1, graph2, n1, n2, node_attrib='label',
                              edge_attrib='label'):
    """
    Implementatin of sim(n1, n2) from Collins and Duffy (2001). Parsing with a
    Single Neuron.

    Given two (dependency parse) graphs and a node from each one, returns
    the set of common dependency targets. Each target consists of a
    (target node ID, target node ID) tuple, where the first target is from the
    first graph and the second one is from the second graph.
    
    What is a dependency target?
    
    We check all outgoing edges of node n1 from graph1 and n2 from graph2
    for common dependency relations (e.g. 'dt' or 'subj'). If both nodes
    share a relation, we check if the neighboring nodes we reach with this
    relation represent the same token. If they do, a
    (n1 target node, n2 target node) dependency target is added to the result
    set.
    
    Parameters
    ----------
    graph1, graph2 : networkx.DiGraph
        two dependency graphs to 
    n1, n2 : str
        a node ID from the first graph and a node ID from the second one

    Returns
    -------
    common_deps : set of (str, str)
    """
    n1_children = dependency_children(graph1, n1, edge_attrib=edge_attrib)
    n2_children = dependency_children(graph2, n2, edge_attrib=edge_attrib)
    n1_rels, n2_rels = defaultdict(list), defaultdict(list)

    for source_set, target_dict in ((n1_children, n1_rels), (n2_children, n2_rels)):
        for rel, target in source_set:
            target_dict[rel].append(target)

    common_rels = set(n1_rels) & set(n2_rels)  # intersection
    common_deps = set()
    for rel in common_rels:
        for n1_target in n1_rels[rel]:
            n1_target_word = graph1.node[n1_target][node_attrib]
            for n2_target in n2_rels[rel]:
                n2_target_word = graph2.node[n2_target][node_attrib]
                if n1_target_word == n2_target_word:
                    common_deps.add( (n1_target, n2_target) )
    return common_deps


def count_common_subgraphs(graph1, graph2, n1, n2,
                     node_attrib='label', edge_attrib='label'):
    """
    Counts the number of common (dependency parse) subgraphs rooted at n1 and
    n2. This is an implementation of Cm(n1, n2) for dependency structures from
    Collins and Duffy (2001). Parsing with a Single Neuron.
    """
    for graph in (graph1, graph2):
        assert nx.is_directed_acyclic_graph(graph)
    
    if graph1.node[n1][node_attrib] != graph2.node[n2][node_attrib]:
        return 0

    n1_children = dependency_children(graph1, n1, edge_attrib=edge_attrib)
    n2_children = dependency_children(graph2, n2, edge_attrib=edge_attrib)

    if not n1_children or not n2_children:
        return 0
    else:
        result = 1  # neutral element of multiplication
        for n1_target, n2_target in common_dependency_targets(graph1, graph2, n1, n2,
                                                        node_attrib=node_attrib):
            result *= (count_common_subgraphs(graph1, graph2,
                                        n1_target, n2_target,
                                        node_attrib='label',
                                        edge_attrib='label') + 2)
        return result - 1


def get_dependency_rules(graph, root_node=None,
                         node_attrib='label', edge_attrib='label'):
    """
    Given a graph, returns a set of its dependency rules. If root_node is
    given, returns only those rules from the subgraph rooted at that node.
    A dependency rules is represented by a
    (source node label, edge/relation label, target node label) triple, e.g.
    ('woman', 'dt', 'the').
    
    Returns
    -------
    rules : set of (str, str, str) tuples
        each dependency production rule is represented by a
        (source node label, edge/relation label, target node label)
        tuple
    """
    rules = set()

    if not root_node:
        # root node is the first element in a topological sort of the graph
        root_node = nx.topological_sort(graph)[0]

    for source, target in nx.dfs_edges(graph, root_node):
        rules.add( (ensure_utf8(graph.node[source].get(node_attrib, source)),
                    ensure_utf8(graph[source][target].get(edge_attrib, '')),
                    ensure_utf8(graph.node[target].get(node_attrib, target))) )
    return rules


def includes_all_subgraph_rules(graph, subgraph_candidate,
                                subgraph_root_node=None,
                                node_attrib='label', edge_attrib='label'):
    """
    returns True, iff a graph contains all dependency rules of the
    given subgraph candidate.
    """
    graph_rules = get_dependency_rules(graph, node_attrib=node_attrib,
                                       edge_attrib=edge_attrib)
    subgraph_rules = get_dependency_rules(subgraph_candidate,
                                          root_node=subgraph_root_node,
                                          node_attrib=node_attrib,
                                          edge_attrib=edge_attrib)
    return all(sg_rule in graph_rules for sg_rule in subgraph_rules)


def is_dependency_subgraph(graph, subgraph_candidate,
                           node_attrib='label', edge_attrib='label'):
    """
    returns True, if the graph contains all of the subgraph candidate's
    dependency rules. The subgraph must also be (weakly) connected and contain
    at least two nodes.

    NOTE: The criteria used here might not be strong enough, i.e. it would
    be possible to construct a subgraph candidate that contains only rules
    from the graph but is not a true subgraph of the graph.
    """
    if len(subgraph_candidate) > 1:
        if nx.is_weakly_connected(subgraph_candidate):
            if includes_all_subgraph_rules(graph, subgraph_candidate,
                                           node_attrib=node_attrib,
                                           edge_attrib=edge_attrib):
                return True
    return False


def get_dependency_subgraphs(graph, node_attrib='label', edge_attrib='label'):
    """
    naively generate all (dependency parse) subgraphs of a given graph by
    iterating through all possible node combinations. HIGHLY INEFFICIENT.
    """
    assert nx.is_directed_acyclic_graph(graph)
    for n in xrange(graph.number_of_nodes()):
        for subnodes in itertools.combinations(graph.nodes(), n+1):
            subgraph_candidate = graph.subgraph(subnodes)
            if is_dependency_subgraph(graph, subgraph_candidate,
                                      node_attrib=node_attrib,
                                      edge_attrib=edge_attrib):
                yield subgraph_candidate


def generate_all_unique_dependency_subgraphs(graphs, node_attrib='label',
                                             edge_attrib='label'):
    same_node_label = iso.categorical_node_match(node_attrib, '')
    same_edge_label = iso.categorical_edge_match(edge_attrib, '')
    if len(graphs) == 0:
        return []
    elif len(graphs) == 1:
        return list(get_dependency_subgraphs(graphs[0], node_attrib=node_attrib))
    else:
        unique_subgraphs = list(get_dependency_subgraphs(
            graphs[0], node_attrib=node_attrib, edge_attrib=edge_attrib))
        for graph in graphs[1:]:
            for subgraph in get_dependency_subgraphs(graph):
                sg_combs = itertools.product([subgraph], unique_subgraphs)
                if not any(nx.is_isomorphic(new_sg, old_sg,
                                            node_match=same_node_label,
                                            edge_match=same_edge_label)
                           for new_sg, old_sg in sg_combs):
                    unique_subgraphs.append(subgraph)
        return unique_subgraphs
