def getheader(literals, clauses):
    return f'p cnf {literals} {clauses}\n'


def getrow(pos, neg):
    poss = " ".join((str(literal) for literal in pos))
    negs = " ".join(("-"+str(literal) for literal in neg))
    if poss:
        if negs:
            return f'{poss} {negs} 0\n'
        else:
            return f'{poss} 0\n'
    else:
        if negs:
            return f'{negs} 0\n'
        else:
            return f'0\n'


def negate_clause(pos, neg):
    return getrow(neg, pos)


def complement(pos, args):
    return (i for i in range(1, args + 1) if i not in pos)


def yield_add(it, add):
    yield add
    yield from it
