# -*- coding: utf-8 -*-
"""Misc tools."""

import os
from pathlib import Path
from typing import Any, Callable, Optional, Union

import numpy as np

###############################################################################


def clean_path(p: Union[Path, str], resolve: bool = True) -> Path:
    """Clean a path from stuff like ~ or $HOME."""
    path_str = Path(p).as_posix()
    if path_str.startswith("$HOME") or path_str.startswith("~"):
        path_str = path_str.replace("$HOME", Path().home().as_posix(), 1)
        path_str = path_str.replace("~", Path().home().as_posix(), 1)
    if not resolve:
        return Path(path_str)
    return Path(path_str).resolve()


###############################################################################


def print_progressbar(
    iteration: int,
    total: int,
    prefix: str = "",
    suffix: str = "",
    decimals: int = 1,
    length: int = 100,
    fill: str = "█",
):
    """
    Print a progress bar.

    https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    access: 2018-12-20
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    progBar = fill * filledLength + "-" * (length - filledLength)
    print("\r%s |%s| %s%% %s" % (prefix, progBar, percent, suffix), end="\r")
    # Print New Line on Complete
    if iteration == total:
        print("\n")


# #
# # Sample Usage
# #

# from time import sleep

# # A List of Items
# items = list(range(0, 57))
# l = len(items)

# # Initial call to print 0% progress
# printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
# for i, item in enumerate(items):
#     # Do stuff...
#     sleep(0.1)
#     # Update Progress Bar
#     printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)


###############################################################################


def find_youngest_file(path: Path, pattern: str, n: int = 1) -> Optional[list[Path]]:
    """
    Find the file that matches a pattern and has the youngest modification timestamp if there are multiple files that match the pattern.

    input:
        path, string or pathlib.Path, where to look for the file(s)
        pattern, string, pattern to look for in files (see pathlib.Path.glob)
        n, integer, how many to return. defaults to 1.

    Returns
    -------
        filename(s) of youngest file(s), including path
        None if no file
    """
    assert n >= 1, "n must be greater equal 1."

    path = Path(path)
    files = [Path(f) for f in path.glob(pattern) if os.path.isfile(f)]
    sortfiles = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)

    if sortfiles:
        return sortfiles[:n]
    return None


###############################################################################


def checkbytes_lt128(file: Union[str, Path]) -> bool:
    """
    Check if all bytes of a file are less than decimal 128.

    Returns
    -------
        True for an ASCII encoded text file else False.
    """
    with open(file, "rb") as f:
        content = f.read()
    return all(b < 128 for b in content)


###############################################################################


def find_fist_elem(arr: Union[list, np.ndarray], val: Any, condition: Callable) -> Optional[Any]:
    """
    Find the first element in arr that gives (arr[ix] condition val) == True.

    Inputs:
        arr: numeric numpy 1d array or python list
        val: scalar value
        condition: e.g. 'operator.ge' (operator package)

    Returns
    -------
        index of value matching the condition or None if no match is found.
    """
    if isinstance(arr, list):
        return next((ix for ix, v in enumerate(arr) if condition(v, val)), None)
    result = np.argmax(condition(arr, val))
    return result if condition(arr[result], val) else None


###############################################################################


# TODO : rename 'list_change_elem_index'
# TODO : do not mutate input; return new list
def list_chng_elem_index(lst: list, element: Any, new_index: int) -> Optional[list]:
    """
    Change the index of an element in a list.

    ! modifies the list in-place !
    see https://stackoverflow.com/a/3173159/10197418
    """
    if new_index >= len(lst) or new_index < 0:
        raise IndexError("new index is out of range")

    if element in lst:
        lst.insert(new_index, lst.pop(lst.index(element)))


###############################################################################


def set_compare(a: set, b: set) -> tuple[set, set, set]:
    """
    Compare two iterables a and b. set() is used for comparison, so only unique elements will be considered.

    Parameters
    ----------
    a : iterable
    b : iterable

    Returns
    -------
    tuple with 3 elements:
        (what is only in a (not in b),
         what is only in b (not in a),
         what is common in a and b)
    """
    a, b = set(a), set(b)
    return (a - b, b - a, a.intersection(b))
