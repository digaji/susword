#!/usr/bin/python3
import math
import numpy
import time
import rsa_algo.ctxtime as ctx

# 100 digit prime numbers
P100 =  20747222467734852078_21695222107608587480_99647472111729275299_25899121966847505496_58310084416732550077
Q100 =  23674957702171429952_64827948666809233066_40949769987011200314_93523803751248552300_68487109373226251983 

# 1000 digit prime numbers
P1_000 = (6935 * 2 ** 3309) + 1
Q1_000 = (6611 * 2 ** 3309) + 1

# 10_000 digit prime numbers
P10_000 = 572391 * 2 ** 33199 + 1
Q10_000 = 4459 * 2 ** 33206 + 1

def egcd(a, b):
    """
    The extended euclidean algorithm finds two integers x, y such that:
    a * x + b * y = gcd(a, b)
    source: https://brilliant.org/wiki/extended-euclidean-algorithm/
    """
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def mod_power(a, n, m):
    """
    computes a ** n % m
    source: https://www.youtube.com/watch?v=3Bh7ztqBpmw&ab_channel=JacksonInfoSec
    """
    r = 1
    while n > 0:
        if n & 1 == 1:
            r = (r * a) % m
        a = (a * a) % m
        n >>= 1 
    return r

def encrypt_char(i, e, n):
    """
    encrypts the algorithm using the key pair (e, n)
    """
    return mod_power(i, e, n)
    # return i ** e % n

def decrypt_char(i, d, n):
    """decrypts the algorithm using the key pair (d, n)"""
    return mod_power(i, d, n)
    # return i ** d % n

def get_encryption_key(phi, n):
    """
    returns the encryption key
    """
    for i in range(2, phi, 1):
        if (math.gcd(i, n) == 1) \
                and (math.gcd(i, phi) == 1):
            return i

def get_decryption_key(e, phi):
    """
    returns the decryption key
    """
    return egcd(e, phi)[1]

def get_2factor(n):
    """returns the two prime factors of n"""
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if (n % i == 0):
            return (i, n // i)
    raise Exception("n cannot be prime")

def crack_key(e, n):
    """attempts to obtain the private key for the public key"""
    p, q = get_2factor(n)
    phi = (p - 1) * (q - 1)
    return (egcd(e, phi)[1], n)

def gen_key(p = 2, q = 7):
    """
    generates the encryption and decryption keys based
    on the given prime numbers
    """
    # p, q = 2, 7
    n = p * q
    # amount of numbers
    # that are coprime to n 
    # that are below n
    phi = (p - 1) * (q - 1)

    # choosing e
    # This is the public key
    e = get_encryption_key(phi, n)

    # This is the private key
    d = get_decryption_key(e, phi)
    print(f"{(e * d) % phi = }")
    return ((e, n), (d, n))

def encrypt_string(txt: str, e: int, n: int):
    """only inputs ascii characters"""
    # print(li_txt)
    return [encrypt_char(ord(c), e, n) for c in txt]

def decrypt_string(cipher: list, d: int, n: int):
    return "".join([chr(decrypt_char(i, d, n)) for i in cipher])

def test():
    # enc_key is the public key
    # dec_key is the private key

    enc_key, dec_key = gen_key(P100, Q100)

    print(f"{enc_key = }")
    print(f"{dec_key = }")
    sm = 1011010111
    print(f"{sm = }")
    with ctx.Timer():
        em = encrypt_char(sm, *enc_key)
    print(f"{em = }")
    with ctx.Timer():
        dm = decrypt_char(em, *dec_key)
    print(f"{dm = }")

    # --- Cracking the key ---
    # with ctx.Timer():
    #     crk_key = crack_key(*enc_key)
    # # print(f"crack time: {time.time() - s}")
    # print(f"{crk_key = }")
    # cm = decrypt_char(em, *crk_key)
    # print(f"{cm = }")


def main():
    enc_key, dec_key = gen_key(P100, Q100)
    print(f"{enc_key = }")
    print(f"{dec_key = }")
    sm = "Hello123!;.\na123"
    print(f"{sm = }")
    with ctx.Timer():
        em = encrypt_string(sm, *enc_key)
    print(f"{em = }")
    with ctx.Timer():
        dm = decrypt_string(em, *dec_key)
    print(f"{dm = }")
    pass

if __name__ == '__main__':
    main()
