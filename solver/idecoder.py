import graph


def getlookup(path):
    args, _ = graph.getargs(path)
    return {n: arg for (n, arg) in enumerate(args, start=1)}


def decode(pos, lookup):
    return frozenset(lookup[literal] for literal in pos)


def decode_all(solutions, path):
    lookup = getlookup(path)
    for pos, _ in solutions:
        yield decode(pos, lookup)
