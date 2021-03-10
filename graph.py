import re
import sys

arg_re = re.compile(r'arg\(([^,\s]+?)\)\.')
edge_re = re.compile(r'att\(([^,\s]+?),([^,\s]+?)\)\.')


def parse_graph(path):
    with open(path, "r") as f:
        content = f.read()
    if content:
        args = (arg[1] for arg in arg_re.finditer(content))
        for n, arg in enumerate(args, start=1):
            content = content.replace(arg, str(n))
        edges = [(int(edge[1]), int(edge[2])) for edge in edge_re.finditer(content)]
        return list(range(1, n+1)), edges


def pre_suc(args, edges):
    pre = {arg: set() for arg in args}
    suc = {arg: set() for arg in args}
    for a1, a2 in edges:
        pre[a2].add(a1)
        suc[a1].add(a2)
    return pre, suc


if __name__ == '__main__':
    parse_graph(sys.argv[1])
