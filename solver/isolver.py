import re
import subprocess
import tempfile

from solver import tools

kissat = r'C:\Users\asib1\Documents\Asib\repos\aaf-py\solver\kissat.exe'

SAT = 10
UNSAT = 20

sol_pattern = re.compile(r"^v (.+?) 0", flags=re.MULTILINE)
pos_pattern = re.compile(r"(?<!-)\d+|(?<=^)\d+")
neg_pattern = re.compile(r"(?<=-)\d+")


def solve_all(path):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmpsol:
        with open(path, "r") as origin:
            tmpsol.write(origin.read())
    while True:
        sol = solve(tmpsol.name)
        if not sol:
            break
        pos, neg = sol
        yield pos, neg
        assumption = tools.negate(pos, neg)
        with open(tmpsol.name, "a") as oldsol:
            oldsol.write(assumption)


def solve(path):
    prc = subprocess.run([kissat, path, '--relaxed'], stdout=subprocess.PIPE, encoding='utf-8')
    if prc.returncode == SAT:
        m = sol_pattern.search(prc.stdout)
        return interpret_sol(m[1])
    elif prc.returncode == UNSAT:
        return


def interpret_sol(sol_s):
    pos = [int(literal) for literal in pos_pattern.findall(sol_s)]
    neg = [int(literal) for literal in neg_pattern.findall(sol_s)]
    return pos, neg


if __name__ == '__main__':
    solve(r"C:\Users\asib1\AppData\Local\Temp\tmpfxss3b4v.cf")
