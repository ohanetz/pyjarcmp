import os
from contextlib import contextmanager

@contextmanager
def chdir(new_dir):
    old_dir = os.getcwd()
    os.chdir(os.path.expanduser(new_dir))
    try:
        yield
    finally:
        os.chdir(old_dir)
