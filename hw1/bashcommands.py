from collections import deque
from typing import Callable, TypeVar, Tuple
from functools import wraps

T = TypeVar("T")
R = TypeVar("R")

ReceivedFunction = Callable[[T, int, int, R], R]
ResultFunction = Callable[..., R]


def for_each_argument(initial_value: R = None) -> Callable[[ReceivedFunction], ResultFunction]:
    """
    This function must be called for a decorator to be returned!
    This returns a decorator which accepts a function that describes its behaviour for 1 target parameter of type T,
    the decorator returns a function that accepts any number of target parameters, which iterates over its arguments
    and for each calls the original function.
    The returned function is called the result function.
    :param initial_value: the initial value of the accumulator
    :return: the decorator that accepts the original function which receives 4 parameters: one of many
    target arguments of type T, current target argument index in the list of all target arguments provided
    to the result function, total number of target arguments provided to the result function,
    accumulator of type R which is equal to the return value of the f function on the previous iteration
    the result function which accepts any number of target arguments, which returns the value returned by f on
    the last iteration
    """

    # this trick is used to remain the return types clear
    def decorator(f: ReceivedFunction) -> ResultFunction:
        accumulator = initial_value

        @wraps(f)
        def f_for_many(*many_args):
            nonlocal accumulator
            n_args = len(many_args)
            for arg_index, arg in enumerate(many_args):
                accumulator = f(arg, arg_index, n_args, accumulator)
            return accumulator

        return f_for_many

    return decorator


def print_line(line: str) -> None:
    """
    This is needed to fight special cases when lines end not with a newline character but with EOF or some weird
    character. Supports only \n newlines for simplicity.
    """
    print(line if len(line) == 0 or line[-1] == "\n" else f"{line}\n", end="")


def print_file_header_conditionally(filepath: str, n_files: int) -> None:
    if n_files > 1:
        print(f"==> {filepath} <==")


@for_each_argument(initial_value=(0, 0, 0))
def wc(
    filepath: str, cur_filepath_index: int, n_filepaths: int, total_counters: Tuple[int, int, int]
) -> Tuple[int, int, int]:
    total_lines, total_words, total_bytes = total_counters
    cur_lines, cur_words, cur_bytes = 0, 0, 0
    try:
        with open(filepath) as f:
            for line in f:
                cur_lines += 1
                cur_words += len(line.split())
                cur_bytes += len(bytes(line, encoding="utf8"))
        total_lines += cur_lines
        total_words += cur_words
        total_bytes += cur_bytes
        print(f"lines : {cur_lines}, words : {cur_words}, bytes : {cur_bytes} for {filepath}")
    except FileNotFoundError:
        print(filepath, "no such file")

    is_last_file = cur_filepath_index == n_filepaths - 1
    if is_last_file:
        print(f"lines : {total_lines}, words : {total_words}, bytes : {total_bytes} in total\n")
    return total_lines, total_words, total_bytes


def is_blank(string: str) -> bool:
    blank_chars = {"\n", "\r", "\r\n", "\t"}
    return set(string) | blank_chars == blank_chars


@for_each_argument(initial_value=1)
def nl(filepath: str, _, __, line_count: int) -> int:
    cur_line_count = line_count
    try:
        with open(filepath) as f:
            for line in f:
                if is_blank(line):
                    print()
                else:
                    print_line(f"{cur_line_count}\t{line}")
                    cur_line_count += 1
    except FileNotFoundError:
        print(filepath, "no such file")

    return cur_line_count


@for_each_argument()
def head(filepath: str, _, n_files: int, __) -> None:
    print_file_header_conditionally(filepath, n_files)
    try:
        with open(filepath) as f:
            for line_num, line in enumerate(f):
                if line_num >= 10:
                    break
                print_line(line)
                line_num += 1
    except FileNotFoundError:
        print(filepath, "no such file")


@for_each_argument()
def tail(filepath: str, _, n_files: int, __) -> None:
    print_file_header_conditionally(filepath, n_files)
    queue: deque = deque(maxlen=10)
    try:
        with open(filepath) as f:
            for line in f:
                queue.append(line)
    except FileNotFoundError:
        print(filepath, "no such file")
    for line in queue:
        print_line(line)


if __name__ == "__main__":
    wc("bashcommands.py", "test.txt")
    nl("bashcommands.py", "test.txt")
    head("bashcommands.py", "test.txt")
    tail("bashcommands.py", "test.txt")
