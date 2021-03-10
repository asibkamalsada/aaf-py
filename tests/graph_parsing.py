import os
import tempfile
import unittest


class GraphTesting(unittest.TestCase):
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
    path_cf, header, rows = cf.prepare_cf(tmpgraph.name)

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

    sol = [([1, 3], [2]), ([3], [1, 2]), ([], [1, 2, 3]), ([1], [2, 3]), ([2], [1, 3])]
    sol.sort()

    def test_solve_all(self):
        self.assertEqual(self.sol, self.all_sol)

    cf_sol = list(cf.solve(tmpgraph.name))
    cf_sol.sort()

    def test_cf_solve_all(self):
        self.assertEqual(self.sol, self.cf_sol)

    os.remove(tmpgraph.name)


if __name__ == '__main__':
    unittest.main()
