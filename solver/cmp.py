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
    return "".join(tools.getrow(pos=tools.yield_add((b + args for b in pre[a]), a), neg=()) for a in range(1, args + 1))


def substitutions(args, pre):
    return "".join(tools.getrow(pos=tools.yield_add(pre[b], b + args), neg=()) for b in range(1, args + 1))


def solve_cmp(path, writeout, ext_assumps=None):
    cmp_cnf, args, pre = prepare_cmp(path)
    if writeout:
        with open(path + ".cmp", "w+") as outt:
            outt.write(cmp_cnf)
    lookup = idecoder.getlookup(path)
    yield from (idecoder.decode(pos=real_pos, lookup=lookup) for real_pos in
                solve_cmp_encoded(cmp_cnf, args, pre, ext_assumps))


def solve_cmp_encoded(cmp_cnf, args, pre, ext_assumps=None):
    if ext_assumps is None:
        ext_assumps = set()

    for (pos, neg) in isolver.solve_all(cmp_cnf, ext_assumps):
        # print(f'pos: {pos}, neg: {neg}')
        real_pos = tuple(lit for lit in pos if lit < args)
        if next((lit for lit in pos if lit >= args and pre[lit - args].intersection(real_pos)), None) is None:
            # hinders kissat to check for an already found solution with different replacement-literals > args
            ext_assumps.add(tools.negate_clause(pos=real_pos, neg=()))
            yield real_pos
