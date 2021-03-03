from Crypto.Cipher import DES
from Crypto import Random
from binascii import unhexlify
import sys
import time

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


# Get and check iv and cbc
iv = sys.argv[1]
cbc_key = sys.argv[2]

if not is_hex(iv):
    print("Error: IV is not in hexadecimal string")
    sys.exit()

if not is_hex(cbc_key):
    print("Error: Key is not in hexadecimal string")
    sys.exit()

# Convert hex to binary
cbc_key = unhexlify(sys.argv[2])
print('='*100)
print('Key used: ', [x for x in cbc_key])

iv = unhexlify(sys.argv[1])
print("IV used: ", [x for x in iv])
print('='*100)

# Open file
try:
    file_name = sys.argv[3]
    f = open(file_name,'rb')
    plain_text = f.read()
except:
    sys.exit()

# Padding
pad = 8 - len(plain_text) % 8
if pad != 8:
    for i in range(pad):
        plain_text = plain_text.__add__(b'\x00')
#print("Plaintext is: ", plain_text)

# Encrypt
start_time1 = time.time()
des1 = DES.new(cbc_key, DES.MODE_CBC, iv)
cipher_text = des1.encrypt(plain_text)
encrypt_time = time.time() - start_time1
#print("Ciphertext is: ",cipher_text)

with open(sys.argv[4], 'wb') as f:
    f.write(cipher_text)

# Decrypt
start_time2 = time.time()
des2 = DES.new(cbc_key, DES.MODE_CBC, iv)
msg = des2.decrypt(cipher_text)
decrypt_time = time.time() - start_time2
#print("Original Message", msg)
#print('='*100)

print("Encryption time is: ", encrypt_time)
print("Decryption time is: ", decrypt_time)