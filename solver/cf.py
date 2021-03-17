from solver import isolver, idecoder, tools
import graph


def prepare_cf(path):
    args, edges = graph.parse_graph(path)
    return f'{tools.getheader(args, len(edges))}{getrows_cf(edges)}'


def getrows_cf(edges):
    return "".join(tools.getrow(pos=(), neg=(a1, a2)) for (a1, a2) in edges)


def solve_cf(path, writeout):
    cnf_cf = prepare_cf(path)
    if writeout:
        with open(path + ".cf", "w+") as outt:
            outt.write(cnf_cf)
    yield from idecoder.decode_all(isolver.solve_all(cnf_cf), path)
