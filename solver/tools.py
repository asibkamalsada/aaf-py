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


def negate(pos, neg):
    return getrow(neg, pos)


def yield_additional(it, add):
    yield add
    yield from it

