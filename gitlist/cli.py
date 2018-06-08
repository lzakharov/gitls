import os
import argparse
from collections import namedtuple
from pathlib import Path

DESCRIPTION = '''Print all local git repositories.'''
GIT_DIR = '.git'

Repository = namedtuple('Repository', ['name', 'path'])


def find_repositories(path):
    """Returns a list of git repositories inside the path."""
    return [Repository(os.path.basename(dirpath), os.path.abspath(dirpath))
            for dirpath, dirnames, _ in os.walk(path)
            if GIT_DIR in dirnames]


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('dir', type=str, nargs='?', default=Path.cwd(),
                        help='where to find repositories (default: current directory)')
    args = parser.parse_args()

    repositories = sorted(find_repositories(args.dir))
    name_width = max(map(len, map(lambda x: x.name, repositories)))
    print('\n'.join(map(lambda x: f'{x.name:{name_width}} ({x.path})', repositories)))


if __name__ == '__main__':
    main()
