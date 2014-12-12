#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

from inspect import getsource
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from IPython.core.display import HTML
from IPython.display import display, Image

# install with: sudo pip install git+http://github.com/chebee7i/nxpd/#egg=nxpd
from nxpd import draw


def memoize(f):
    """
    Memoization decorator for functions taking one or more arguments and
    keyword arguments.
    
    adapted from: http://code.activestate.com/recipes/578231-probably-the-fastest-memoization-decorator-in-the-/#c1
    
    NOTE: All LRU (last recently used) cache implementations that I've found
    only work with functions with one argument (or at least don't work with
    keyword args)!
    """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args, **kwargs):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)


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


def draw_multiple_graphs(graphs):
    """
    draws multiple networkx graphs with graphviz and put the generated
    images in the same IPython notebook output cell.
    """
    for graph in graphs:
        display(Image(filename=draw(graph, show=False)))


def print_source(function):
    """
    For use inside an IPython notebook: given a function name, print it's
    source code.
    
    # cf. http://stackoverflow.com/q/20665118
    """
    return HTML(highlight(getsource(function), PythonLexer(), 
                HtmlFormatter(full=True, nobackground=True)))
