import os
import tempfile
import unittest


class GraphTesting(unittest.TestCase):
    import graph
    samplegraph = "arg(1)." \
                  "arg(2)." \
                  "arg(3)." \
                  "att(1,2)." \
                  "att(2,3)."
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmpgraph:
        tmpgraph.write(samplegraph)

    args, edges = graph.parse_graph(tmpgraph.name)

    os.remove(tmpgraph.name)

    def test_parsing(self):
        self.assertEqual((self.args, self.edges), (['1', '2', '3'], [('1', '2'), ('2', '3')]))

    pre, suc = graph.pre_suc(args, edges)

    def test_pre_suc(self):
        self.assertEqual((self.pre, self.suc), ({'1': set(), '2': {'1'}, '3': {'2'}}, {'1': {'2'}, '2': {'3'}, '3': set()}))


if __name__ == '__main__':
    unittest.main()
