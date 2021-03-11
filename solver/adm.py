from solver import isolver, idecoder, cf, tools
import graph


def prepare_adm(path):
    args, edges = graph.parse_graph(path)
    pre, _ = graph.pre_suc(args, edges)
    header = tools.getheader(args, len(edges) + sum(len(v) for v in pre.values()))
    cf_rows = cf.getrows_cf(edges)
    adm_rows = "".join(getrows_adm(args, pre))
    return f'{header}{cf_rows}{adm_rows}'


def getrows_adm(args, pre):
    yield from (tools.getrow(pre[attacker], (arg,)) for arg in range(1, args + 1) for attacker in pre[arg])


def solve_adm(path):
    yield from idecoder.decode_all(isolver.solve_all(prepare_adm(path)), path)
