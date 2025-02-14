import os
import time
import sys
from contextlib import contextmanager


def get_project_abspath(relative: str):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", relative))


@contextmanager
def timed_zone(name: str, *, print_time_points: bool = False):
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        if print_time_points:
            print(f"{name}:\n\t started: {start_time:.3f}s, ended: {end_time}s\n\ttook {end_time - start_time:.3f}s")
        else:
            print(f"{name}:\n\ttook {end_time - start_time:.3f}s")
