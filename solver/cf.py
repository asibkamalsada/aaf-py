import sys
from solver.tools import *
import graph


def prepare_cf(path):
    args, edges = graph.parse_graph(path)
    header = getheader(args, len(edges))
    rows = [getrow(pos=(), neg=(a1, a2)) for (a1, a2) in edges]
    with open(path + ".cf", "w") as cf_dimacs:
        cf_dimacs.write(header)
        cf_dimacs.writelines(rows)
    return header, rows


if __name__ == '__main__':
    prepare_cf(sys.argv[1])
