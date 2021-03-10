from solver import isolver, idecoder
from solver.tools import *
import graph


def prepare(path):
    header, rows = head_rows(*graph.parse_graph(path))
    path_cf = path + ".cf"
    with open(path_cf, "w") as cf_dimacs:
        cf_dimacs.write(header)
        cf_dimacs.writelines(rows)
    return path_cf, header, rows


def head_rows(args, edges):
    header = getheader(args, len(edges))
    rows = [getrow(pos=(), neg=(a1, a2)) for (a1, a2) in edges]
    return header, rows


def solve(path):
    path_cf, _, _ = prepare(path)
    yield from idecoder.decode_all(isolver.solve_all(path_cf), path)
