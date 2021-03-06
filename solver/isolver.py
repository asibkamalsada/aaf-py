import re
import subprocess

from solver import tools

kissat = r'C:\Users\asib1\Documents\Asib\repos\aaf-py\solver\kissat.exe'

SAT = 10
UNSAT = 20

sol_pattern = re.compile(r"^v (.+?) 0", flags=re.MULTILINE)
pos_pattern = re.compile(r"(?<![-\d])\d+|(?<=^)\d+")
neg_pattern = re.compile(r"(?<=-)\d+")


def solve_all(cnf, external_assumptions=None):
    while True:
        if external_assumptions is not None:
            for external_assumption in external_assumptions:
                cnf += external_assumption
            external_assumptions.clear()
        sol = solve(cnf)
        if not sol:
            break
        pos, neg = sol
        yield pos, neg
        assumption = tools.negate_clause(pos, neg)
        cnf += assumption


def solve(cnf, relaxed=True):
    if relaxed:
        prc = subprocess.run([kissat, '--relaxed'], stdout=subprocess.PIPE, input=cnf, encoding='utf-8')
    else:
        prc = subprocess.run(kissat, stdout=subprocess.PIPE, input=cnf, encoding='utf-8')
    if prc.returncode == SAT:
        m = sol_pattern.search(prc.stdout)
        return interpret_sol(m[1])
    elif prc.returncode == UNSAT:
        return


def interpret_sol(sol_s):
    pos = tuple(int(literal) for literal in pos_pattern.findall(sol_s))
    neg = tuple(int(literal) for literal in neg_pattern.findall(sol_s))
    return pos, neg


if __name__ == '__main__':
    solve(r"C:\Users\asib1\AppData\Local\Temp\tmpfxss3b4v.cf")
