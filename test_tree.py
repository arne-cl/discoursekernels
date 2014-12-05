
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
