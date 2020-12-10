import argparse
import random
import readline
import traceback

import banko


parser = argparse.ArgumentParser()


names = {
    90: "GAMLE OLE",
}


def spil() -> None:
    parser.parse_args()
    numbers = []
    drawn = []
    while True:
        if not numbers:
            print("VELKOMMEN TIL BANKO! Let's start a new game!")
            numbers = list(range(1, 91))
            random.shuffle(numbers)
            drawn = []
        try:
            s = input("> ").split(None, 1)
        except (EOFError, KeyboardInterrupt):
            print("Bye")
            print("drawn", drawn)
            break
        try:
            if not s:
                # Go next
                i = numbers.pop()
                drawn.append(i)
                if i in names:
                    print(i, names[i])
                else:
                    print(i)
            elif s[0] == "ryst":
                print("RYST POSEN *sound of %s number(s) rustling in the bag*" % len(numbers))
                random.shuffle(numbers)
            elif s[0] == "banko":
                seed = int(s[1])
                plade = banko.plade(seed)
                print("_" * (5 * 9 + 1))
                for r in plade:
                    r_str = "|%s|" % "|".join(str(v or "").center(4, "_") for v in r)
                    banko_row = all(i in drawn for i in r if i)
                    print(r_str, "BANKO" if banko_row else "no banko")
            elif s[0] == "drawn":
                if s[1:]:
                    for i in eval(s[1]):
                        numbers.remove(i)
                        drawn.append(i)
                print("drawn", drawn)
            elif s[0] == "reset":
                numbers = []
            else:
                print("Unknown command %r" % s[0])
        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    spil()
