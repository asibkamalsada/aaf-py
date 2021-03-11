import os
from sys import argv, exit

from solver import cf, adm, stb

extensions = ('cf', 'adm', 'cmp', 'grd', 'prf', 'stb')


def main():
    if len(argv) != 3:
        print("specify {extension} and {path to apx}")
        exit(1)

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
        print_sols(cf.solve_cf(path))
    if extension == 'adm':
        print_sols(adm.solve_adm(path))
    if extension == 'stb':
        print_sols(stb.solve_stb(path))


def print_sols(sols):
    for sol in sols:
        print('{' + " ".join(sol) + '}')


if __name__ == '__main__':
    main()
