import os
import subprocess
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


def get_url(repository):
    """Returns url for specified repository."""
    process = subprocess.Popen(['git', 'remote', 'get-url', 'origin'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode().strip()


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('dir', type=str, nargs='?', default=Path.cwd(),
                        help='where to find repositories (default: current directory)')
    parser.add_argument('-u', '--url', type=str, nargs='?', default=False, const=True,
                        help='show repository urls (default: False)')
    args = parser.parse_args()

    repositories = sorted(find_repositories(args.dir))

    for repository in repositories:
        name = repository.name
        path = repository.path
        line = f'{name} {path}'

        if args.url:
            url = get_url(repository)
            line += f' {url}'

        print(line)


if __name__ == '__main__':
    main()
