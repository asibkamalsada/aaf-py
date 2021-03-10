import tempfile
import unittest


class GraphTesting(unittest.TestCase):
    def test_parsing(self):
        import graph
        samplegraph = "arg(1)." \
                      "arg(2)." \
                      "arg(3)." \
                      "att(1,2)." \
                      "att(2,3)."
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmpgraph:
            tmpgraph.write(samplegraph)
        args, edges = graph.parse_graph(tmpgraph.name)
        self.assertEqual((args, edges), (['1', '2', '3'], [('1', '2'), ('2', '3')]))


if __name__ == '__main__':
    unittest.main()
