from des_algo.trides import *
from aes_algo.aes import *
from rsa_algo.rsa import *
import pandas as pd
from time import perf_counter
# for progress bar
from tqdm import tqdm

def main():
    dataframe = pd.read_csv('data.csv', header = 0, usecols=["password"]) # ISO-8859-1
    print(dataframe)
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
    for i, d in tqdm(enumerate(dataframe["password"][:10_000])):
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
    print(f"total time encrypt (aes): {sum(tot_enc_aes)}")
    print(f"total time decrypt (aes): {sum(tot_dec_aes)}")
    print(f"total time encrypt (des): {sum(tot_enc_des)}")
    print(f"total time decrypt (des): {sum(tot_dec_des)}")
    print(f"total time encrypt (rsa): {sum(tot_enc_rsa)}")
    print(f"total time decrypt (rsa): {sum(tot_dec_rsa)}")


if __name__ == '__main__':
    main()



