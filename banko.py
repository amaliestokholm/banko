import argparse
from typing import List

import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("seed", type=int)
parser.add_argument("n", type=int)


PREAMBLE = r"""
\documentclass{memoir}
\newcommand{\banko}[1]{\framebox[1cm][c]{\rule[-3mm]{0pt}{\dimexpr 1cm-2\fboxsep}#1}}
\begin{document}
""".strip()

# \vspace{1cm}
# \noindent
# {\small ID: 123\\}
# \banko{42}%
# \banko{43}%
# \\[-1pt]%
# \banko{44}%
# \banko{45}%
# \\[-1pt]%
#
# \vspace{1cm}
# \noindent
# {\small ID: 123\\}
# \banko{42}%
# \banko{43}%
# \\[-1pt]%
# \banko{44}%
# \banko{45}%
# \\[-1pt]%
#
# \end{document}


def plade(seed: int) -> List[int]:
    rng = np.random.RandomState(seed)
    rows = 3
    cols = 9
    whichones = np.sort(rng.choice(rows * cols, (15,), False))
    col = whichones // rows
    result: List[int] = []
    for i in range(cols):
        count = np.sum(col == i)
        if not count:
            continue
        lo = i * 10
        hi = lo + 10
        if i == 0:
            lo = 1
        if i == cols - 1:
            hi += 1
        result += sorted(rng.choice(np.arange(lo, hi), (count,), False).tolist())
    assert result == sorted(result), result
    assert len(result) == len(set(result)), result
    nums = np.zeros(rows * cols)
    assert len(whichones) == len(result)
    for i, r in zip(whichones, result):
        nums[i] = r
    return np.transpose(nums.reshape((cols, rows))).tolist()


def main() -> None:
    args = parser.parse_args()
    if args.n == 1:
        seeds = [args.seed]
    else:
        rng = np.random.RandomState(args.seed)
        seeds = sorted(rng.choice(1000, args.n, False).tolist())
    print(PREAMBLE)
    for i in seeds:
        print("")
        print(r"\vspace{1cm}")
        print(r"\noindent")
        print(r"{\small ID: %s\\}" % i)
        for row in plade(i):
            for v in row:
                print(r"\banko{%s}%%" % (int(v) or ""))
            print(r"\\[-1pt]%")
    print(r"\end{document}")


if __name__ == "__main__":
    main()
