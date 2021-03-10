import sys

from solver import isolver, idecoder
from solver.tools import *
import graph


def prepare_cf(path):
    args, edges = graph.parse_graph(path)
    header = getheader(args, len(edges))
    rows = [getrow(pos=(), neg=(a1, a2)) for (a1, a2) in edges]
    path_cf = path + ".cf"
    with open(path_cf, "w") as cf_dimacs:
        cf_dimacs.write(header)
        cf_dimacs.writelines(rows)
    return path_cf, header, rows


def solve(path):
    path_cf, _, _ = prepare_cf(path)
    yield from idecoder.decode_all(isolver.solve_all(path_cf), path)


if __name__ == '__main__':
    prepare_cf(sys.argv[1])
