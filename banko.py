import argparse
import math
from typing import List

import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("seed", type=int)
parser.add_argument("n", type=int)


PREAMBLE = r"""
\documentclass[extrafontsizes,17pt,oneside]{memoir}
\newcommand{\plade}[4]{%
    \par\vspace{4ex}%
    \noindent{\small ID: #1\\}%
    #2\\[-0.2ex]#3\\[-0.2ex]#4\\[-0.2ex]%
}
\newcommand{\tal}[1]{%
    \framebox[6ex][c]{\rule[-2ex]{0pt}{\dimexpr 6ex-2\fboxsep}#1}%
}
\newcommand{\tom}{\tal{}}
\begin{document}
""".strip()


def comb(N: int, k: int) -> int:
    return math.factorial(N) // (math.factorial(k) * math.factorial(N - k))


def plade(seed: int) -> List[List[int]]:
    rng = np.random.RandomState(seed)
    rows = 3
    cols = 9
    # Need to place 5 numbers in each row, so n=15 in total.
    numbers_in_row = 5
    n = numbers_in_row * rows
    # Each column needs at least 1 number,
    # so there are only x=n-9 extra numbers that we need to place.
    x = n - cols
    # Need to pick a,b>=0, a+b<=9 so that (9-a-b) + 2a + 3b = n.
    # 9 + a + 2b = n
    # a = n - 9 - 2b
    # b >= 0
    # -2b <= 0
    # 0 <= a <= n - 9
    # 0 <= n - 9 - 2b
    # 2b <= n - 9
    # b <= (n - 9) // 2
    # C(9,b) * C(9-b,a)
    ab = [(x - 2 * b, b) for b in range(min(x // 2, cols) + 1)]
    assert all(2 * a + 3 * b + (cols - a - b) == n for a, b in ab)
    weights = np.asarray([comb(cols, b) * comb(cols - b, a) for a, b in ab])
    colcounts = np.ones(cols, dtype=np.intp)
    a, b = ab[rng.choice(len(ab), 1, True, weights / weights.sum())[0]]
    colcounts[rng.choice(cols, a, False)] = 2
    colcounts[rng.choice(np.equal(colcounts, 1).nonzero()[0], b, False)] = 3
    assert colcounts.sum() == n, (colcounts, colcounts.sum(), n)
    rowcounts = np.zeros(rows)
    mask = np.zeros((cols, rows), dtype=np.bool)
    for i in sorted(range(cols), key=lambda i: -colcounts[i]):
        free = np.less(rowcounts, numbers_in_row).nonzero()[0]
        assert len(free) >= colcounts[i], (free, colcounts[i])
        r = rng.choice(free, colcounts[i], False)
        rowcounts[r] += 1
        mask[i][r] = True
    nums = np.zeros((cols, rows), dtype=np.intp)
    for i in range(cols):
        count = np.sum(mask[i])
        if not count:
            continue
        lo = i * 10
        hi = lo + 10
        if i == 0:
            lo = 1
        if i == cols - 1:
            hi += 1
        nums[i][mask[i]] = np.sort(rng.choice(np.arange(lo, hi), (count,), False))
    return np.transpose(nums).tolist()


def print_ascii_plade(p: List[List[int]]) -> None:
    print("_" * (5 * 9 + 1))
    for r in p:
        print("|%s|" % "|".join(str(v or "").center(4, "_") for v in r))


def main() -> None:
    args = parser.parse_args()
    if args.n == 1:
        seeds = [args.seed]
    else:
        rng = np.random.RandomState(args.seed)
        seeds = sorted(rng.choice(1000, args.n, False).tolist())
    with open("banko.tex", "w") as fp:
        print(PREAMBLE, file=fp)
        for i, seed in enumerate(seeds):
            p = plade(seed)
            # print_ascii_plade(p)
            print(r"\plade{%s}%%" % seed, file=fp)
            for row in p:
                print(
                    "{%s}%%"
                    % "".join(r"\tom" if v == 0 else r"\tal{%s}" % v for v in row),
                    file=fp,
                )
            if (i + 1) % 3 == 0:
                print(r"\newpage", file=fp)
        print(r"\end{document}", file=fp)


if __name__ == "__main__":
    main()
