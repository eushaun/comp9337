import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import sys
import time

random_generator = Random.new().read
key = RSA.generate(1024, random_generator) # generate pub and priv key

publickey = key.publickey() # pub key export for exchange

# Open file
try:
    file_name = sys.argv[1]
    f = open(file_name,'rb')
    plain_text = f.read()
except:
    sys.exit()

# Padding
pad = 8 - len(plain_text) % 8
if pad != 8:
    for i in range(pad):
        plain_text = plain_text.__add__(b'\x00')

# Encrypt
start_time1 = time.time()
cipher_text = publickey.encrypt(plain_text, 32) # message to encrypt is in the above line 'encrypt this message'
encrypt_time = time.time() - start_time1

# Decrypt
start_time2 = time.time()
decrypted = key.decrypt(ast.literal_eval(str(cipher_text)))
decrypt_time = time.time() - start_time2

print("Encryption time is: ", encrypt_time)
print("Decryption time is: ", decrypt_time)

# print('Plaintext encrypted using Public Key is:', cipher_text)
# print()
# print('Ciphertext decrypted with Private key is', decrypted)
# print('='*100)
