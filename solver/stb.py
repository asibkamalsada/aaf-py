from solver import isolver, idecoder, cf, tools
import graph


def prepare_stb(path):
    args, edges = graph.parse_graph(path)
    pre, suc = graph.pre_suc(args, edges)
    header = tools.getheader(args, len(edges) + args)
    cf_rows = cf.getrows_cf(edges)
    stb_rows = "".join(getrows_stb(args, pre))
    return f'{header}{cf_rows}{stb_rows}'


def getrows_stb(args, pre):
    yield from (tools.getrow(pos=tools.yield_add(pre[arg], arg), neg=()) for arg in range(1, args + 1))


def solve_stb(path, writeout):
    cnf_stb = prepare_stb(path)
    if writeout:
        with open(path + ".stb", "w+") as outt:
            outt.write(cnf_stb)
    yield from idecoder.decode_all(isolver.solve_all(cnf_stb), path)
