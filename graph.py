import re
import sys

arg_re = re.compile(r'arg\(([^,\s]+?)\)\.')
edge_re = re.compile(r'att\(([^,\s]+?),([^,\s]+?)\)\.')


def parse_graph(path):
    with open(path, "r") as f:
        content = f.read()
    if content:
        args = [arg[1] for arg in arg_re.finditer(content)]
        edges = [(edge[1], edge[2]) for edge in edge_re.finditer(content)]
        return args, edges


if __name__ == '__main__':
    parse_graph(sys.argv[1])
