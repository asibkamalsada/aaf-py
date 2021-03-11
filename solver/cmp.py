from solver import isolver, idecoder, cf, tools, adm
import graph


def prepare_cmp(path):
    args, edges = graph.parse_graph(path)
    pre, _ = graph.pre_suc(args, edges)
    header = tools.getheader(2 * args, len(edges) + sum(len(v) for v in pre.values()) + 2 * args)
    cf_rows = cf.getrows_cf(edges)
    adm_rows = adm.getrows_adm(args, pre)
    cmp_rows = getrows_cmp(args, pre)
    return f'{header}{cf_rows}{adm_rows}{cmp_rows}', args, pre


def getrows_cmp(args, pre):
    return f'{cmpconstraint(args, pre)}{substitutions(args, pre)}'


def cmpconstraint(args, pre):
    return "".join(tools.getrow(pos=tools.yield_additional((b + args for b in pre[a]), a), neg=()) for a in range(1, args + 1))


def substitutions(args, pre):
    return "".join(tools.getrow(pos=tools.yield_additional(pre[b], b + args), neg=()) for b in range(1, args + 1))


def solve_cmp(path, external_assumptions=None):
    if external_assumptions is None:
        external_assumptions = set()

    cmp_cnf, args, pre = prepare_cmp(path)
    lookup = idecoder.getlookup(path)

    for (pos, neg) in isolver.solve_all(cmp_cnf, external_assumptions):
        print(f'pos: {pos}, neg: {neg}')
        real_pos = tuple(lit for lit in pos if lit < args)
        if next((lit for lit in pos if lit >= args and pre[lit - args].intersection(real_pos)), None) is None:
            external_assumptions.add(tools.negate(pos=real_pos, neg=()))
            yield idecoder.decode(pos=real_pos, lookup=lookup)
