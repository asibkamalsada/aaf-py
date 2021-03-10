import os
from sys import argv, exit

from solver import cf

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
        for sol in cf.solve(path):
            print('{' + " ".join(sol) + '}')


if __name__ == '__main__':
    main()
