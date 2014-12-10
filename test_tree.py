
import networkx as nx
from networkx import DiGraph

def example_tree():
    """creates a tree/networkx.DiGraph of a syntactic parse tree"""
    tree = DiGraph()
    tree.add_nodes_from(['S', 'NP-1', 'N-1', 'Jeff', 'VP', 'V', 'ate', 'NP-2', 'D',
                         'the', 'N-2', 'apple'])
    tree.add_edges_from([('S', 'NP-1'), ('NP-1', 'N-1'), ('N-1', 'Jeff'),
                         ('S', 'VP'), ('VP', 'V'), ('V', 'ate'),
                         ('VP', 'NP-2'), ('NP-2', 'D'), ('D', 'the'),
                         ('NP-2', 'N-2'), ('N-2', 'apple')])
    return tree


def example_valid_subtrees():
    vs1 = DiGraph()
    vs1.add_edges_from([('NP-2', 'D'), ('NP-2', 'N-2'), ('D', 'the'), ('N-2', 'apple')])

    vs2 = DiGraph()
    vs2.add_edges_from([('NP-2', 'D'), ('NP-2', 'N-2')])

    vs3 = DiGraph()
    vs3.add_edges_from([('D', 'the')])

    vs4 = DiGraph()
    vs4.add_edges_from([('N-2', 'apple')])

    vs5 = DiGraph()
    vs5.add_edges_from([('NP-2', 'D'), ('NP-2', 'N-2'), ('D', 'the')])

    vs6 = DiGraph()
    vs6.add_edges_from([('NP-2', 'D'), ('NP-2', 'N-2'), ('N-2', 'apple')])
    return  [vs1, vs2, vs3, vs4, vs5, vs6]


def example_invalid_subtrees():
    is1 = DiGraph()
    is1.add_node('NP-2')
    is1.add_edges_from([('D', 'the'), ('N-2', 'apple')])

    is2 = DiGraph()
    is2.add_node('D')

    is3 = DiGraph()
    is3.add_nodes_from(['D', 'N-2'])

    is4 = DiGraph()
    is4.add_edges_from([('NP-2', 'D'), ('D', 'the')])

    is5 = DiGraph()
    is5.add_nodes_from(['the'])

    is6 = DiGraph()
    is6.add_nodes_from(['the', 'apple'])

    is7 = DiGraph()
    is7.add_edges_from([('the', 'apple')])
    return [is1, is2, is3, is4, is5, is6, is7]


def test_is_subtree():
    from tree_kernel import is_subtree
    tree = example_tree()
    valid_subtrees = example_valid_subtrees()
    invalid_subtrees = example_invalid_subtrees()
    for valid_subtree in valid_subtrees:
        assert is_subtree(tree, valid_subtree) == True
    for invalid_subtree in invalid_subtrees:
        assert is_subtree(tree, invalid_subtree) == False

def label_nodes(node_label_tuples_list):
    """
    convert a list of (node ID, node label) tuples into a list of
    (node ID, {'label': node label}) tuples, which can be added to a
    networkx graph via .add_nodes_from().
    """
    nodes = []
    for node_id, node_label in node_label_tuples_list:
        nodes.append( (node_id, {'label': node_label}) )
    return nodes


def label_edges(edge_label_tuples_list):
    """
    convert a list of (source ID, target ID, edge label) tuples into a list of
    (source ID, target ID, {'label': edge label}) tuples, which can be added
    to a networkx graph via .add_nodes_from().
    """
    edges = []
    for source_id, target_id, edge_label in edge_label_tuples_list:
        edges.append( (source_id, target_id, {'label': edge_label}) )
    return edges



# Example trees

## Jeff ate cookies

tree_jeff_ate_cookies = nx.DiGraph()
tree_jeff_ate_cookies.add_nodes_from(label_nodes([
    (1, 'S'),
    (2, 'NP'), (3, 'N'), (4, 'Jeff'),
    (5, 'VP'), (6, 'V'), (7, 'ate'),
    (8, 'NP'), (9, 'N'), (10, 'cookies')]))
tree_jeff_ate_cookies.add_edges_from([
    (1, 2), # S NP
    (1, 5), # S VP
    (2, 3), # NP N
    (3, 4), # N Jeff
    (5, 6), # VP V
    (6, 7), # V ate
    (5, 8), # VP NP
    (8, 9), # NP N
    (9, 10), # N cookies
])


## Steve ate bananas

tree_steve_ate_bananas = nx.DiGraph()
tree_steve_ate_bananas.add_nodes_from(label_nodes([
    (1, 'S'),
    (2, 'NP'), (3, 'N'), (4, 'Steve'),
    (5, 'VP'), (6, 'V'), (7, 'ate'),
    (8, 'NP'), (9, 'N'), (10, 'bananas')]))
tree_steve_ate_bananas.add_edges_from([
    (1, 2), # S NP
    (1, 5), # S VP
    (2, 3), # NP N
    (3, 4), # N Steve
    (5, 6), # VP V
    (6, 7), # V ate
    (5, 8), # VP NP
    (8, 9), # NP N
    (9, 10), # N bananas
])


# Alex died

tree_alex_died = nx.DiGraph()
tree_alex_died.add_nodes_from(label_nodes([
    (1, 'S'),
    (2, 'NP'), (3, 'N'), (4, 'Alex'),
    (5, 'VP'), (6, 'V'), (7, 'died')]))
tree_alex_died.add_edges_from([
    (1, 2), # S NP
    (1, 5), # S VP
    (2, 3), # NP N
    (3, 4), # N Alex
    (5, 6), # VP V
    (6, 7), # V died
])


# Alex

tree_fragment_alex = nx.DiGraph()
tree_fragment_alex.add_nodes_from(label_nodes([
    (2, 'NP'), (3, 'N'), (4, 'Alex')]))
tree_fragment_alex.add_edges_from([
    (2, 3), # NP N
    (3, 4), # N Alex
])


# NP-N

tree_fragment_npn = nx.DiGraph()
tree_fragment_npn.add_nodes_from(label_nodes([
    (2, 'NP'), (3, 'N')]))
tree_fragment_npn.add_edges_from([
    (2, 3) # NP N
])


# The man drank wine


tree_the_man_drank_wine = nx.DiGraph()
tree_the_man_drank_wine.add_nodes_from(label_nodes([
    (1, 'S'),
    (2, 'NP'), (3, 'D'), (4, 'the'), (5, 'N'), (6, 'man'),
    (7, 'VP'), (8, 'V'), (9, 'drank'),
    (10, 'NP'), (11, 'N'), (12, 'wine')]))
tree_the_man_drank_wine.add_edges_from([
    (1, 2), # S NP
    (1, 7), # S VP
    (2, 3), # NP D
    (2, 5), # NP N
    (3, 4), # D the
    (5, 6), # N man
    (7, 8), # VP V
    (8, 9), # V drank
    (7, 10), # V NP
    (10, 11), # NP N
    (11, 12), # N wine
])


# The man killed the woman


tree_the_man_killed_the_woman = nx.DiGraph()
tree_the_man_killed_the_woman.add_nodes_from(label_nodes([
    (1, 'S'),
    (2, 'NP'), (3, 'D'), (4, 'the'), (5, 'N'), (6, 'man'),
    (7, 'VP'), (8, 'V'), (9, 'killed'),
    (10, 'NP'), (11, 'D'), (12, 'the'), (13, 'N'), (14, 'woman')]))
tree_the_man_killed_the_woman.add_edges_from([
    (1, 2), # S NP
    (1, 7), # S VP
    (2, 3), # NP D
    (2, 5), # NP N
    (3, 4), # D the
    (5, 6), # N man
    (7, 8), # VP V
    (8, 9), # V killed
    (7, 10), # V NP
    (10, 11), # NP D
    (10, 13), # NP N
    (11, 12), # D the
    (13, 14), # N woman
])
