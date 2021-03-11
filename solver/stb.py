from solver import isolver, idecoder, cf
from solver.tools import *
import graph


def prepare_stb(path):
    args, edges = graph.parse_graph(path)
    pre, suc = graph.pre_suc(args, edges)
    header = getheader(args, len(edges) + args)
    _, cf_rows = cf.head_rows(args, edges)
    path_stb = path + ".stb"
    with open(path_stb, "w") as stb_dimacs:
        stb_dimacs.write(header)
        stb_dimacs.writelines(cf_rows)
        stb_dimacs.writelines(getrows(args, pre))
    return path_stb


def getrows(args, pre):
    for arg in range(1, args + 1):
        pos = pre[arg]
        yield getrow(pos=yield_additional(pre[arg], arg), neg=())


def yield_additional(it, add):
    yield add
    yield from it


def solve(path):
    path_stb = prepare_stb(path)
    yield from idecoder.decode_all(isolver.solve_all(path_stb), path)
