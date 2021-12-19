#!/usr/bin/python3

def factor(n):
    c, i = n, 2
    res = []
    while (c > 1):
        if (c % i == 0):
            print(c)
            res.append(i)
            c //= i
        else:
            i += 1
    return res


def main():
    print(f"{factor(2 ** 1000 - 1) = }")
    pass

if __name__ == '__main__':
    main()
