from time import perf_counter
from aes_algo.aes import *
from des_algo.trides import *
from rsa_algo.rsa import *

def benchmark(sample: list, verbose = False):
    k = triple_des("DESCRYPTDESCRY--", ECB, pad=None, padmode=PAD_PKCS5)
    aes_sub_key = key_expansion("1234567890123456")
    tot_enc_aes = []
    tot_dec_aes = []
    tot_enc_des = []
    tot_dec_des = []
    tot_enc_rsa = []
    tot_dec_rsa = []
    # Huge decryption key made RSA slow
    enc_key, dec_key = gen_key(P100, Q100)

    # using tqdm so we can easily see progress
    for d in sample:
        start = perf_counter()
        result = encrypt(str(d), aes_sub_key)
        tot_enc_aes.append(perf_counter() - start)
        start = perf_counter()
        dec_res = decrypt(result, aes_sub_key)
        tot_dec_aes.append(perf_counter() - start)

        start = perf_counter()
        result = k.encrypt(str(d))
        tot_enc_des.append(perf_counter() - start)
        start = perf_counter()
        dec_res = k.decrypt(result)
        tot_dec_des.append(perf_counter() - start)

        start = perf_counter()
        result = encrypt_string(str(d), *enc_key)
        tot_enc_rsa.append(perf_counter() - start)
        start = perf_counter()
        dec_res = decrypt_string(result, *dec_key)
        tot_dec_rsa.append(perf_counter() - start)

    tott_enc_aes = sum(tot_enc_aes)
    tott_dec_aes = sum(tot_dec_aes)
    tott_enc_des = sum(tot_enc_des)
    tott_dec_des = sum(tot_dec_des)
    tott_enc_rsa = sum(tot_enc_rsa)
    tott_dec_rsa = sum(tot_dec_rsa)
    if verbose:
        print(f"total time encrypt (aes): {sum(tott_enc_aes)}")
        print(f"total time decrypt (aes): {sum(tott_dec_aes)}")
        print(f"total time encrypt (des): {sum(tott_enc_des)}")
        print(f"total time decrypt (des): {sum(tott_dec_des)}")
        print(f"total time encrypt (rsa): {sum(tott_enc_rsa)}")
        print(f"total time decrypt (rsa): {sum(tott_dec_rsa)}")
    return (tott_enc_aes, tott_dec_aes), (tott_enc_des, tott_dec_des), (tott_enc_rsa, tott_dec_rsa)

