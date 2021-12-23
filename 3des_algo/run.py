from trides import *

data = "Hello World"
k = triple_des("DESCRYPTDESCRY--", ECB, pad=None, padmode=PAD_PKCS5)
d = k.encrypt(data)

print (f"Encrypted: {d}")
print (f"Encrypted: {k.decrypt(d)}")