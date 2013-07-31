#!/usr/bin/env python
"""
Given a directional graph and certain path requests, try to 
fit as many nodes as possible. This is an NP-Hard problem.
"""

import time


def greedy_solve(fname):
    f = open(fname, 'r')
    starttime = time.time()

    nodes_count = int(f.readline())
    edges_count = int(f.readline())
    paths_count = int(f.readline())

    # skip the edges, we don't use them
    for edge_iter in xrange(edges_count):
        f.readline()

    paths = {}
    intersections = {}
    for path_iter in xrange(paths_count):
        path_nodes = f.readline().split()
        path = "".join(path_nodes)
        paths[path] = {
            "nodes": [int(i) for i in path_nodes],
            "score": 0
        }
        for node in paths[path]["nodes"]:
            if node not in intersections:
                intersections[node] = {"score": 0, "intersects": []}
            intersections[node]["score"] += 1
            intersections[node]["intersects"].append(path)
    # score each path
    # score = number of paths each node in a path intersects with
    for path in paths:
        for node in paths[path]["nodes"]:
            paths[path]["score"] += intersections[node]["score"]

    # sort by converting to min heap, not a true heap though
    heap = paths.items()
    heap = sorted(heap, key=lambda x: x[1]['score'], reverse=True)
    selected_paths = []
    while len(heap) > 0:

        # get all of the smallest paths
        minpaths = []
        minscore = heap[-1][1]["score"]
        while len(heap) > 0 and minscore == heap[-1][1]["score"]:
            minpaths.append(heap.pop())

        # if there is more than one minpath
        # repeatedly find the path with the fewest intersections
        # within this subgroup. remove the paths it intersects.
        if len(minpaths) > 1:
            # print "There is a tie between", minpaths
            node_count = {}
            for path in minpaths:
                for node in path[1]['nodes']:
                    if node not in node_count:
                        node_count[node] = {'count': 0, 'intersects': []}
                    node_count[node]["count"] += 1
                    node_count[node]["intersects"].append(path)
            for path in minpaths:
                for node in path[1]['nodes']:
                    path[1]['score'] += node_count[node]['count']
            paths_to_keep = []
            while len(minpaths) > 0:
                minp = min(minpaths, key=lambda x: x[1]['score'])
                minpaths.remove(minp)
                paths_to_keep.append(minp)
                for node in minp[1]['nodes']:
                    for p in node_count[node]["intersects"]:
                        try:
                            minpaths.remove(p)
                        except ValueError:
                            pass
            minpaths = paths_to_keep

        # choose each minpath
        # remove any paths it intersects from the heap
        for path in minpaths:
            # print "Choose ", path[1]['nodes']
            selected_paths.append(path)
            for node in path[1]['nodes']:
                for intersecting_path in intersections[node]['intersects']:
                    try:
                        heap.remove((intersecting_path, paths[
                                    intersecting_path]))
                    except ValueError:
                        pass

    endtime = time.time()
    output = open("FolseDawoodjeePatel.txt", "w")
    runtime = round((endtime - starttime) * 1000, 1)
    output.write("%g\n%d" % (runtime, len(selected_paths)))
    for path in selected_paths:
        output.write('\n')
        output.write("%s" % " ".join(str(n) for n in path[1]['nodes']))


def main():
    greedy_solve('in.txt')


if __name__ == '__main__':
    profile = False 
    if profile:
        import cProfile
        cProfile.run("main()")
    else:
        main()
