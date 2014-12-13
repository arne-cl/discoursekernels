#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

"""
This module contains code to efficiently enumerate subgraphs
(for some arbitrary definition of efficiently).

Most of the code is based on
Wernicke, Sebastian (2006). Efficient Detection of Network Motifs.
"""

import random
import networkx as nx
from multiprocessing import Pool # CPUs


def open_neighborhood(graph, node_subset):
    """
    $N(V')$: returns the set of all nodes that are in the graph's node set
    (but not in the given subset) and are adjacent to at least one node
    in the subset. Based on Wernicke (2006).

    WARNING: different results for directed vs. undirected graphs
    """
    open_nbh = set()
    node_set = set(graph.nodes())
    nodes_not_in_subset = node_set - node_subset
    for node_not_in_subset in nodes_not_in_subset:
        if any(neighbor in node_subset
               for neighbor in graph.neighbors(node_not_in_subset)):
            open_nbh.add(node_not_in_subset)
    return open_nbh


def exclusive_neighborhood(graph, node, node_subset):
    """
    given a node v that doesn't belong to the given node subset V',
    returns all nodes that are neighbors of v, but don't belong to
    the node subset V' or its open neighborhood N(V').
    Based on Wernicke (2006).

    WARNING: different results for directed vs. undirected graphs
    """
    assert node not in node_subset
    open_nbh = open_neighborhood(graph, node_subset)

    exclusive_nbh = set()
    for neighbor in graph.neighbors(node):
        if neighbor not in node_subset and neighbor not in open_nbh:
            exclusive_nbh.add(neighbor)
    return exclusive_nbh


def enumerate_all_size_k_subgraphs(graph, k):
    """
    returns all subgraphs of the given graph that have k nodes.
    The algorith is called ``ESU`` in Wernicke (2006).
    """
    assert all(isinstance(node, int) for node in graph.nodes_iter())
    if not 1 <= k <= len(graph):
        return []

    all_subgraphs = []
    for node in graph.nodes_iter():
        extension = {neighbor for neighbor in graph.neighbors(node)
                     if neighbor > node}
        subgraphs = extend_subgraph(graph, k, {node}, extension, node)
        if isinstance(subgraphs, list):
            all_subgraphs.extend(subgraphs)
        else: # isinstance(subgraphs, nx.Graph)
            all_subgraphs.append(subgraphs)
    return all_subgraphs


def extend_subgraph(graph, k, subgraph_nodes, extension_nodes, node):
    """
    This function is the recursively called part of the ``ESU`` algorithm
    in Wernicke (2006).
    """
    if len(subgraph_nodes) == k:
        return graph.subgraph(subgraph_nodes)

    all_subgraphs = []
    while extension_nodes:
        # remove random node w from extension_nodes
        random_extension_node = random.choice(list(extension_nodes))
        extension_nodes.remove(random_extension_node)
        exclusive_neighbors = {neighbor for neighbor in exclusive_neighborhood(graph,
                                                                               random_extension_node,
                                                                               subgraph_nodes)
                               if neighbor > node}
        vbar_extension = extension_nodes | exclusive_neighbors # union
        extended_subgraph_nodes = subgraph_nodes | {random_extension_node}
        subgraphs = extend_subgraph(graph, k, extended_subgraph_nodes, vbar_extension, node)

        if isinstance(subgraphs, list):
            all_subgraphs.extend(subgraphs)
        else: # isinstance(subgraphs, nx.Graph)
            all_subgraphs.append(subgraphs)
    return all_subgraphs


def __extract_subgraphs_from_node(graph, node, k):
    extension = {neighbor for neighbor in graph.neighbors(node)
                 if neighbor > node}
    return extend_subgraph(graph, k, {node}, extension, node)


def enumerate_all_size_k_subgraphs_parellel(graph, k, num_of_workers=4):
    """
    Trivial parallelization of the ESU algorithm from Wernicke (2006).
    """
    assert all(isinstance(node, int) for node in graph.nodes_iter())
    if not 1 <= k <= len(graph):
        return []

    pool = Pool(num_of_workers) # number of CPUs / workers
    results = [pool.apply_async(__extract_subgraphs_from_node,
                                args=(graph, node, k))
               for node in graph.nodes_iter()]

    pool.close()
    pool.join()
    return [result.get() for result in results]


def enumerate_all_subgraphs_upto_size_k(document_graph, k):
    """
    returns all subgraphs of a DiscourseDocumentGraph (i.e. a MultiDiGraph)
    with up to k nodes.

    WARNING: This just calls ESU / enumerate_all_size_k_subgraphs() for
    1 ... k.

    TODO: optimize the algorithm to use the results of ESU(k-1) to calculate
    ESU(k).
    """
    document_nodes = len(document_graph)
    if k > document_nodes:
        k = document_nodes

    all_subgraphs = []
    int_graph = nx.convert_node_labels_to_integers(nx.DiGraph(document_graph),
                                                   first_label=1,
                                                   label_attribute='node_id')
    for i in xrange(1, k+1):
        size_k_subgraphs = enumerate_all_size_k_subgraphs(int_graph, i)
        all_subgraphs.extend(size_k_subgraphs)
    return all_subgraphs


def enumerate_all_subgraphs_upto_size_k_parallel(document_graph, k, num_of_workers=4):
    """
    returns all subgraphs of a DiscourseDocumentGraph (i.e. a MultiDiGraph)
    with up to k nodes. This is a trivially parallelized version of
    enumerate_all_subgraphs_upto_size_k()
    """
    document_nodes = len(document_graph)
    if k > document_nodes:
        k = document_nodes

    int_graph = nx.convert_node_labels_to_integers(nx.DiGraph(document_graph),
                                                   first_label=1,
                                                   label_attribute='node_id')

    pool = Pool(processes=num_of_workers) # number of CPUs
    results = [pool.apply_async(enumerate_all_size_k_subgraphs, args=(int_graph, i))
                for i in xrange(1, k+1)]
    pool.close()
    pool.join()

    subgraphs = []
    for result in results:
        tmp_result = result.get()
        if isinstance(tmp_result, list):
            subgraphs.extend(tmp_result)
        else:
            subgraphs.append(tmp_result)
    return subgraphs
