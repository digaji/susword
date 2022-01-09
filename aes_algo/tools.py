def print_hexmat(mat):
    n, m = len(mat), len(mat[0])
    for i in range(n):
        for j in range(m):
            print(hex(mat[i][j]), end=' ')
        print()


def print_hexcol(col):
    for v in col:
        print(hex(v), end=' ')
    print()

def debug():

    pass

if __name__ == '__main__':
    debug()

