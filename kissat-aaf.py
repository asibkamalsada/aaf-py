import os
from sys import argv, exit

from solver import cf, adm, stb, cmp, prf

extensions = ('cf', 'adm', 'cmp', 'grd', 'prf', 'stb')


def main():
    if len(argv) < 3:
        print("specify {extension} and {path to apx}")
        exit(1)

    writeout = len(argv) == 4

    if argv[1] in extensions:
        extension = argv[1]
        if os.path.isfile(argv[2]):
            path = argv[2]
        else:
            print(f'path leads to no file')
            exit(1)
    else:
        print(f'extensions are {extensions}')
        exit(1)

    if extension == 'cf':
        print_sols(cf.solve_cf(path, writeout))
    if extension == 'adm':
        print_sols(adm.solve_adm(path, writeout))
    if extension == 'stb':
        print_sols(stb.solve_stb(path, writeout))
    if extension == 'cmp':
        print_sols(cmp.solve_cmp(path, writeout))
    if extension == 'prf':
        print_sols(prf.solve_prf(path, writeout))


def print_sols(sols):
    for sol in sols:
        print('{' + " ".join(sol) + '}')


if __name__ == '__main__':
    main()
