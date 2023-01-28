import argparse
from pathlib import Path
from threading import Thread

import factorize
import sorter

"""
py main.py --from -f hlam
py main.py --dist -d dist 
"""

parser = argparse.ArgumentParser(description = 'my test multi sorting')

parser.add_argument('-f', '--from', required=True)      # option that takes a value
parser.add_argument('-d', '--dist', default='Sorted')

args = vars(parser.parse_args())
from_dir = args.get('from')
dist_dir = args.get('dist')

dirs = []


def read_dirs(path: Path):
    for elem in path.iterdir():
        if elem.is_dir():
            dirs.append(elem)
            read_dirs(elem)

def operative_files(old_path: Path, new_path :Path):
    sorter.sort_dir(old_path, new_path)


if __name__ == '__main__':
    bas_dir = Path(from_dir)
    new_dir = Path(dist_dir)
    dirs.append(bas_dir)
    read_dirs(bas_dir)
    threads = []
    for dir in dirs:
        new_thread = Thread(target=operative_files, args=(dir, new_dir))
        new_thread.start()
        threads.append(new_thread)

    [new_thread.join() for thread in threads]

    factorize.part2()