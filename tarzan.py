#!/usr/bin/env python
"""
Models a maze with certain directional and distance constraints
as a graph and uses networkx's built in path finding function 
to find a way out (if there is one).

for each letter in input:
  add it to the graph, noting its direction and x,y position
  create an edge w/ weight 3 in the direction the node points
  create an edge w/ weight 4 in the direction the node points

to find the exit:
use networkx's shortest_path method starting at the beginning until we
find the exit
"""

import networkx as nx
from networkx.exception import NetworkXNoPath


def remove_empty_nodes(G):
    """ If some edges connect nodes not yet in the graph, the nodes are
        added automatically. There are no errors when adding nodes or
        edges that already exist.
        This does not make a difference in a digraph, since the implicitly
        added nodes have no outbound edges.
        However, we remove these nodes so that a clean graph can be drawn.
        And for good measure. """
    for node in G.nodes(data=True):
        # we can identify implicitly created nodes by their lack of attr's
        if not node[1]:
            G.remove_node(node[0])


def draw_graph(G):
    from matplotlib import pyplot
    pos = nx.spring_layout(G, weight=None)
    labels = dict((n, '%d %d\n%s' % (n[0], n[1],
                  d['direction'])) for n, d in G.nodes(data=True))
    edge_labels = dict(((u, v,), d['weight'])
                       for u, v, d in G.edges(data=True))
    nx.draw_networkx(G, pos=pos, labels=labels, node_size=1000,
                     width=2, node_color='white', edge_color='blue')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    pyplot.show()


def add_edges(x, y, x_offset, y_offset, G, set_size):
    # if x_offset == 1 and y_offset == 1 and y == 1 and x == 2:
    for weight in (3, 4):
        x_offset_value = x_offset * weight
        y_offset_value = y_offset * weight
        edge_end = x + x_offset_value, y + y_offset_value
        # only add the edge if is within the bounds
        if edge_end[0] <= set_size[0] and edge_end[1] <= set_size[1]:
            G.add_edge((x, y), edge_end, weight=weight)


def parse_set(f):

    G = nx.DiGraph()
    set_size = tuple(int(i) for i in f.readline().split())
    set_size = set_size[::-1]
    start = tuple(int(i) for i in f.readline().split())
    start = start[::-1]
    direction_offsets = {
        'N': (0, -1),
        'S': (0, 1),
        'W': (-1, 0),
        'E': (1, 0),
        'NW': (-1, -1),
        'NE': (1, -1),
        'SW': (-1, 1),
        'SE': (1, 1)
    }

    for y in xrange(1, set_size[1] + 1):
        row = f.readline().split()
        for x, direction in enumerate(row):
            x += 1
            if direction == '0':
                target = (x, y)
                G.add_node((x, y), direction=direction)
            elif direction is not 'V':
                G.add_node((x, y), direction=direction)
                x_offset, y_offset = direction_offsets[direction]
                add_edges(x, y, x_offset, y_offset, G, set_size)

    remove_empty_nodes(G)

    try:
        target
    except NameError:
        return "There is no Jojo to find."

    draw_graph(G)

    try:
        path = nx.shortest_path(
            G, source=start, target=target, weight='weight')
    except NetworkXNoPath:
        e_str = "Error: There is no path to Jojo from %s to %s" % (
            start, target)
        print e_str
        return e_str

    solution = []

    for i in range(len(path) - 1):
        node_direction = G.node[path[i]]['direction']
        node_weight = G[path[i]][path[i + 1]]['weight']
        solution.append((node_direction, node_weight))

    return solution


def write_solution(f, soln):
    if isinstance(soln, basestring):
        f.write(soln)
        return
    for index, s in enumerate(soln):
        f.write('%s-%d' % (s[0], s[1]))
        # don't write a space for the last node
        if index != len(soln) - 1:
            f.write(' ')


def main():
    f = open('tarzan_input.txt')
    fout = open('tarzan_output.txt', 'w')
    num_sets = int(f.readline())
    for i in xrange(num_sets):
        f.readline()
        soln = parse_set(f)
        write_solution(fout, soln)
        # don't write a new line for the last set
        if i != num_sets - 1:
            fout.write('\n\n')

if __name__ == '__main__':
    main()
