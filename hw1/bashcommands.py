from collections import deque


def for_each_argument(f):
    def f_for_many(*many_args):
        for arg in many_args:
            f(arg)

    return f_for_many


def wc(*filepaths):
    total_lines = 0
    total_words = 0
    total_bytes = 0
    for filepath in filepaths:
        cur_lines = 0
        cur_words = 0
        cur_bytes = 0
        try:
            with open(filepath) as f:
                for line in f:
                    cur_lines += 1
                    cur_words += len(line.split())
                    cur_bytes += len(bytes(line, encoding="utf8"))
            total_lines += cur_lines
            total_words += cur_words
            total_bytes += cur_bytes
            print(f"lines:{cur_lines} words:{cur_words} bytes:{cur_bytes} for {filepath}")
        except FileNotFoundError:
            print(filepath, "no such file")
    print(f"lines:{total_lines} words:{total_words} bytes:{total_bytes} in total\n")


@for_each_argument
def nl(filepath):
    print(f"==> {filepath} <==")
    try:
        with open(filepath) as f:
            for index, line in enumerate(f):
                print("\t", index + 1, line, end="")
    except FileNotFoundError:
        print(filepath, "no such file")


@for_each_argument
def head(filepath):
    print(f"==> {filepath} <==")
    try:
        with open(filepath) as f:
            line_num = 0
            for line in f:
                if line_num >= 10:
                    break
                print(line, end="")
                line_num += 1
    except FileNotFoundError:
        print(filepath, "no such file")


@for_each_argument
def tail(filepath):
    print(f"==> {filepath} <==")
    queue = deque(maxlen=10)
    try:
        with open(filepath) as f:
            for line in f:
                queue.append(line)
    except FileNotFoundError:
        print(filepath, "no such file")
    for line in queue:
        print(line, end="")


if __name__ == "__main__":
    wc("bashcommands.py", "matrices.py")
    nl("bashcommands.py", "matrices.py")
    head("bashcommands.py", "matrices.py")
    tail("bashcommands.py", "matrices.py")
