from solver import isolver, idecoder, cf
from solver.tools import *
import graph


def prepare_adm(path):
    args, edges = graph.parse_graph(path)
    pre, suc = graph.pre_suc(args, edges)
    header = getheader(args, len(edges) + sum(len(v) for v in pre.values()))
    _, cf_rows = cf.head_rows(args, edges)
    path_adm = path + ".adm"
    with open(path_adm, "w") as adm_dimacs:
        adm_dimacs.write(header)
        adm_dimacs.writelines(cf_rows)
        adm_dimacs.writelines(getrows(args, pre))
    return path_adm


def getrows(args, pre):
    for arg in range(1, args + 1):
        for attacker in pre[arg]:
            pos = tuple(pre[attacker])
            yield getrow(pos, (arg,))


def solve(path):
    path_adm = prepare_adm(path)
    yield from idecoder.decode_all(isolver.solve_all(path_adm), path)
