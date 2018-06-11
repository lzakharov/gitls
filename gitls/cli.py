import os
import subprocess
import argparse
from collections import namedtuple
from enum import Enum
from pathlib import Path

DESCRIPTION = '''Print all local git repositories.'''
GIT_DIR = '.git'

Repository = namedtuple('Repository', ['name', 'path'])


class Status(Enum):
    """Repository statuses."""
    UP_TO_DATE = 0
    MODIFIED = 1


STATUS_SYMBOL = {
    Status.UP_TO_DATE: '\u2705',
    Status.MODIFIED: '\u2757'
}


def find_repositories(path):
    """Returns a list of git repositories inside the path."""
    return [Repository(os.path.basename(dirpath), os.path.abspath(dirpath))
            for dirpath, dirnames, _ in os.walk(path)
            if GIT_DIR in dirnames]


def get_url(repository):
    """Returns url for specified repository."""
    process = subprocess.Popen(['git', 'remote', 'get-url', 'origin'], cwd=repository.path,
                               stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode().strip()


def get_status(repository, verbose=False):
    """Returns repository status for specified repository."""
    process = subprocess.Popen(['git', 'status', '--porcelain'], cwd=repository.path,
                               stdout=subprocess.PIPE)
    out, err = process.communicate()

    if verbose and out:
        print(out.decode().strip())

    if not out:
        return Status.UP_TO_DATE

    return Status.MODIFIED


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('dir', type=str, nargs='?', default=Path.cwd(),
                        help='where to find repositories (default: current directory)')
    parser.add_argument('-u', '--url', type=str, nargs='?', default=False, const=True,
                        help='show repository urls (default: False)')
    parser.add_argument('-v', '--verbose', type=str, nargs='?', default=False, const=True,
                        help='show verbose information (default: False)')
    args = parser.parse_args()

    repositories = sorted(find_repositories(args.dir))

    for repository in repositories:
        name = repository.name
        path = repository.path
        status = STATUS_SYMBOL[get_status(repository, args.verbose)]
        line = f'{status} {name:20} ({path})'

        if args.url:
            url = get_url(repository)
            line += f' [{url}]'

        print(line)


if __name__ == '__main__':
    main()
