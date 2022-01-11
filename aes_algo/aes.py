#!/usr/bin/python3
# References
# https://www.youtube.com/watch?v=nC0mjaUZd8w
# https://www.kavaliro.com/wp-content/uploads/2014/03/AES.pdf
# https://www.youtube.com/watch?v=5PHMbGr8eOA


# Notes:
# * Requires galois.
# * Requires numpy
import galois
import numpy as np
from aes_algo.tools import *
# from aes_algo.tools import *
GF8 = galois.GF(2 ** 8)


def inv_s_box(s_box):
    n = KC * 4
    inverted = [[0 for _ in range(n)] for _ in range(n)]
    # S_BOX[val >> 4][val & 0b1111]
    for i in range(n):
        for j in range(n):
            x = s_box[i][j]
            inverted[x >> 4][x & 0b1111] = (i << 4) | j
    return inverted


KC = 4

S_BOX = [ # substitution box
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],

    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],

    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],

    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16],
]

INV_S_BOX = inv_s_box(S_BOX)

RCON = [ # round constant
    [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

]

MIXER = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

INV_MIXER = np.linalg.inv(GF8(MIXER))

def gen_hex_mat(txt: str):
    res = []
    for i in range(KC):
        res.append([])
        for j in range(0, KC ** 2, KC):
            res[-1].append(ord(txt[i + j]))
    return res

def gen_string(hex_mat):
    res = []
    for j in range(KC):
        for i in range(KC):
            res.append(chr(hex_mat[i][j]))
    return "".join(res)

def box_sub(data_vector, box):
    # print(data_vector)
    new_vector = []
    for val in data_vector:
        new_vector.append(box[val >> 4][val & 0b1111])
    return new_vector

def shift_left(data_vector, k):
    # shifts a data_vector k units to the left
    return data_vector[k:] + data_vector[:k]

def shift_right(data_vector, k):
    return data_vector[-k:] + data_vector[:-k]

class KeyState:

    def __init__(self, key_str: str):
        self.key_state = gen_hex_mat(key_str)

    def transpose(self, data_matrix):
        for i in range(KC):
            for j in range(i + 1, KC):
                data_matrix[i][j], data_matrix[j][i] =\
                    data_matrix[j][i], data_matrix[i][j]
    

    def rot_word(self, data_vector):
        data_vector = shift_left(data_vector, 1)
        return box_sub(data_vector, S_BOX)

    def gen_sub_key(self):
        """
        Generates sub key matrices of given
        key string
        """
        sub_keys = [self.key_state]
        for i in range(10):

            # Acquire asb column
            self.transpose(sub_keys[i])
            asb_col = sub_keys[i][-1]
            asb_col = self.rot_word(asb_col)
            
            # creating new sub key
            new_mat = [[sub_keys[i][0][k] ^ asb_col[k] ^ RCON[k][i] for k in range(KC)]]
            for j in range(1, KC):
                new_mat.append([sub_keys[i][j][k] ^ new_mat[-1][k] for k in range(KC)])
            self.transpose(sub_keys[i])
            self.transpose(new_mat)

            sub_keys.append(new_mat)
        return sub_keys

def key_expansion(key: str):
    if not input_guard(key):
        raise Exception("'key' must satisfy input guard condition")
    if len(key) != 16:
        raise Exception("'key' must be 16 characters long")
    s = KeyState(key)
    return s.gen_sub_key()

def xor_mat(mat1, mat2):
    """Applies the XOR operation element wise"""
    return [[mat1[i][j] ^ mat2[i][j] for j in range(KC)] for i in range(KC)]

def opg(n1: int, n2: int):
    """Applies special integer multiplication"""
    res = 0
    while (n1 and n2):
        if (n2 & 1):
            res ^= n1

        if (n1 & 0x80):
            n1 = (n1 << 1) ^ 0x11b
        else:
            n1 <<= 1
        n2 >>= 1
    return res

def mix_column(mat1):
    """Applies the mixing operation"""
    res = [[0 for _ in range(KC)] for _ in range(KC)]
    for i in range(KC):
        for j in range(KC):
            res[i][j] = opg(MIXER[i][0], mat1[0][j])
            for k in range(1, KC):
                res[i][j] ^= opg(MIXER[i][k], mat1[k][j])
    return res

def unmix_column(mat1):
    """Applies the unmixing operation"""
    res = [[0 for _ in range(KC)] for _ in range(KC)]
    for i in range(KC):
        for j in range(KC):
            res[i][j] = opg(int(INV_MIXER[i][0]), mat1[0][j])
            for k in range(1, KC):
                res[i][j] ^= opg(int(INV_MIXER[i][k]), mat1[k][j])
    return res

def input_guard(txt):
    """
    every key and message must go through the input guard.
    returns true if txt satisfies input guard.
    check out the ascii wikipedia page on printable ascii characters:
    https://en.wikipedia.org/wiki/ASCII
    """
    # input must be non-empty
    if len(txt) == 0:
        return False
    # input must consist of printable ascii characters
    printable_ascii_range = (0x01, 0xff)
    for char in txt:
        if (ord(char) < printable_ascii_range[0])\
                or (ord(char) > printable_ascii_range[1]):
            return False

    return True


def encrypt16(msg, sub_keys):
    """
    Encrypts the message using subkeys.
    only encrypts 16 bytes of text
    """
    cphr = gen_hex_mat(msg)

    for j in range(0, 11):
        # Substitution Bytes and shift row
        if (j > 0):
            for i, row in enumerate(cphr):
                cphr[i] = box_sub(row, S_BOX)
                cphr[i] = shift_left(cphr[i], i)

        # Mix Column
        # Do not mix columns on 10'th round
        # and 0th round
        if ((j > 0) and (j < 10)):
            cphr = mix_column(cphr)

        # Add Roundkey, Round 1
        # Applies XOR operation to each sub key
        cphr = xor_mat(sub_keys[j], cphr)

    return gen_string(cphr)

def decrypt16(cphr, sub_keys):
    """
    Decrypts the cipher using subkeys
    only decrypts 16 bytes of text
    """
    msg = gen_hex_mat(cphr)
    for j in range(10, -1, -1):

        # Add Roundkey, Round 1
        msg = xor_mat(sub_keys[j], msg)

        # Mix Column
        # Do not mix columns on 10'th round
        if (j > 0) and (j < 10):
            msg = unmix_column(msg)

        # Substitution Bytes and shift row
        if (j > 0):
            for i, row in enumerate(msg):
                msg[i] = box_sub(row, INV_S_BOX)
                msg[i] = shift_right(msg[i], i)

    return gen_string(msg)

def encrypt(msg, sub_keys):
    # 1. Check if msg passes input guard
    if not input_guard(msg):
        raise Exception("'msg' must satisfy input guard")

    # 2. Pad message with null character
    if (len(msg) % 16):
        pad_count = 16 - (len(msg) % 16)
        msg += "".join(['\0'] * pad_count)

    # 3. Break message into chunks of 16 characters
    chunks = [msg[i:i+16] for i in range(0, len(msg), 16)]
    for i, v in enumerate(chunks):
        chunks[i] = encrypt16(v, sub_keys)
    return "".join(chunks)

def decrypt(cphr, sub_keys):
    # 1. break cphr into chunks
    chunks = [cphr[i:i+16] for i in range(0, len(cphr), 16)]
    for i, v in enumerate(chunks):
        chunks[i] = decrypt16(v, sub_keys)
    
    # 2. remove padding, works on an empty string
    i = 16
    while (i > 0) and (chunks[-1][i - 1] == '\0'):
        i -= 1
    chunks[-1] = chunks[-1][:i]
    return "".join(chunks)


def debug_mat():
    mat = [
        [0x63, 0xeb, 0x9f, 0xa0],
        [0x2f, 0x93, 0x92, 0xc0],
        [0xaf, 0xc7, 0xab, 0x30],
        [0xa2, 0x20, 0xcb, 0x2b]
    ]
    print_hexmat(INV_MIXER)
    print()
    print_hexmat(mat)
    print()
    mat = mix_column(mat)
    print_hexmat(mat)
    print()
    mat = unmix_column(mat)
    print_hexmat(mat)

def debug16():
    key1 = "abcts my Kung Fu"
    msg1 = "1234567890123456"
    sub_keys = key_expansion(key1)
    print("-- encryption --")
    cphr = encrypt16(msg1, sub_keys)
    print(f"{cphr = }")
    print("-- decrypt --")
    msg = decrypt16(cphr, sub_keys)
    print(f"{msg = }")

def debug():
    key1 = "abcts my Kung Fu"
    msg1 = "Hello my name is Bryn Ghiffar. I am a cat. But I am not as well."
    sub_keys = key_expansion(key1)
    cphr = encrypt(msg1, sub_keys)
    dmsg = decrypt(cphr, sub_keys)

def example1():
    # Here the key must be 16 characters long for AES to work
    #      |              | <- 16 characters
    key = "Encryption key12"
    msg = "Here is the message. Any length is okay"
    
    # Generate sub keys for encryption
    sub_keys = key_expansion(key)
    
    # Encryption and decryption
    cphr = encrypt(msg, sub_keys)
    print(f"{cphr = }")
    dmsg = decrypt(cphr, sub_keys)
    print(f"{dmsg = }")

if __name__ == '__main__':
    # debug()
    # debug_mat()
    example1()
