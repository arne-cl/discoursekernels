#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

import networkx as nx
from discoursekernels.util import label_nodes, label_edges

# Example dependency graphs

## the man saw the woman with the telescope

the_man_saw_the_woman_with_the_telescope = nx.DiGraph()
the_man_saw_the_woman_with_the_telescope.add_nodes_from(label_nodes(
    [(1, '*'), (2, 'saw'), (3, 'man'), (4, 'the'),
     (5, 'woman'), (6, 'the'), (7, 'with'),
     (8, 'telescope'), (9, 'the')]))
the_man_saw_the_woman_with_the_telescope.add_edges_from(label_edges(
    [(1, 2, 'root'), (2, 3, 'sbj'), (3, 4, 'dt'),
     (2, 5, 'obj'), (5, 6, 'dt'),
     (2, 7, 'pp'), (7, 8, 'pp-obj'), (8, 9, 'dt')]
))

## the man

the_man = nx.DiGraph()
the_man.add_nodes_from(label_nodes([(1, 'man'), (2, 'the')]))
the_man.add_edges_from(label_edges([(1, 2, 'dt')]))

## with the telescope

with_the_telescope = nx.DiGraph()
with_the_telescope.add_nodes_from(label_nodes(
    [(1, 'with'), (2, 'telescope'), (3, 'the')]))
with_the_telescope.add_edges_from(label_edges(
    [(1, 2, 'pp-obj'), (2, 3, 'dt')]
))
