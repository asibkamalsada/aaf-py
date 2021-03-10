import os
import tempfile
import unittest


class Testing(unittest.TestCase):
    import graph
    samplegraph = "arg(a1)." \
                  "arg(a2)." \
                  "arg(a3)." \
                  "att(a1,a2)." \
                  "att(a2,a3)."
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmpgraph:
        tmpgraph.write(samplegraph)

    args, edges = graph.parse_graph(tmpgraph.name)

    def test_parsing(self):
        self.assertEqual((self.args, self.edges), (3, [(1, 2), (2, 3)]))

    pre, suc = graph.pre_suc(args, edges)

    def test_pre_suc(self):
        self.assertEqual((self.pre, self.suc), ({1: set(), 2: {1}, 3: {2}}, {1: {2}, 2: {3}, 3: set()}))

    import solver.cf as cf
    path_cf, header, rows = cf.prepare(tmpgraph.name)

    def test_cf(self):
        self.assertEqual("p cnf 3 2\n", self.header)
        self.assertEqual("-1 -2 0\n", self.rows[0])
        self.assertEqual("-2 -3 0\n", self.rows[1])

    import solver.isolver as isolver
    sol_pos, sol_neg = isolver.solve(path_cf)

    def test_isolver(self):
        self.assertEqual([1, 3], self.sol_pos)
        self.assertEqual([2], self.sol_neg)

    all_sol = list(isolver.solve_all(path_cf))
    all_sol.sort()

    cf_sol_expected = [([1, 3], [2]), ([3], [1, 2]), ([], [1, 2, 3]), ([1], [2, 3]), ([2], [1, 3])]
    cf_sol_expected.sort()

    def test_solve_all(self):
        self.assertEqual(self.cf_sol_expected, self.all_sol)

    cf_sol_actual = frozenset(cf.solve(tmpgraph.name))

    import solver.idecoder as idecoder

    dec_expected = frozenset(('a1', 'a3'))
    dec_actual = idecoder.decode([1, 3], {1: 'a1', 2: 'a2', 3: 'a3'})

    def test_decode(self):
        self.assertEqual(self.dec_expected, self.dec_actual)

    dec_all_expected = frozenset({frozenset(['a1', 'a3']), frozenset(['a3']), frozenset([]), frozenset(['a1']), frozenset(['a2'])})

    dec_all_actual = frozenset(idecoder.decode_all(cf_sol_expected, tmpgraph.name))

    def test_decode_all(self):
        self.assertEqual(self.dec_all_expected, self.dec_all_actual)

    def test_cf_solve_all(self):
        self.assertEqual(self.dec_all_expected, self.cf_sol_actual)

    os.remove(tmpgraph.name)


if __name__ == '__main__':
    unittest.main()
