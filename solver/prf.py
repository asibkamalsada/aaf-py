from solver import isolver, idecoder, cf, tools, adm, cmp
import graph


def prepare_prf(path):
    args, edges = graph.parse_graph(path)
    pre, _ = graph.pre_suc(args, edges)
    x = 1  # how many prf clauses are going to be added?
    header = tools.getheader(2 * args, len(edges) + sum(len(v) for v in pre.values()) + x)
    cf_rows = cf.getrows_cf(edges)
    adm_rows = adm.getrows_adm(args, pre)
    prf_rows = getrows_prf(args, pre)
    return f'{header}{cf_rows}{adm_rows}{prf_rows}', args, pre


def getrows_prf(args, pre):
    return f''


def superset(pos, args):
    return f'{tools.getrow(pos=tools.complement(pos, args), neg=())}' \
           f'{"".join((tools.getrow(pos=(lit,), neg=()) for lit in pos))}'


def solve_prf(path, writeout):
    """
    This shit has to run cmp solving algorithm and receiving the possible solutions.
    It runs its own solver too, since it has to check the incoming solutions for preferredness.
    If an incoming solution is propagated to an actual solution, all the steps are blocked for the cmp solver but
    not for the prf solver. The actual solution is going to be blocked for both solvers. That ensures that no solution
    is going to be found twice but it does not ensure that a possible incoming solution is going to be part of an
    already found actual solution.
    This has to be patched.

    The solving algorithm currently only checks whether there is an admissible superset of the given complete set.
    :param path:
    :return:
    """

    prf_cnf, args, pre = prepare_prf(path)
    lookup = idecoder.getlookup(path)

    for pos in cmp.solve_cmp_encoded(f'{prf_cnf}{cmp.getrows_cmp(args, pre)}', args, pre):
        if not isolver.solve(f'{prf_cnf}{superset(pos, args)}'):
            yield idecoder.decode(pos=pos, lookup=lookup)


def extend(pos):
    """
    An extension of pos is returned in case there is one found which satisfies admissible, therefore pos is not maximal.
    In fact it has to be distinguished whether the extensions are UNSAT or already found in which case the extensions
    before are not automatically maximal.

    This method is not used since the solving algorithm currently only checks whether there is an admissible superset of
    the given complete set.
    :param pos:
    :return:
    """
    return True
