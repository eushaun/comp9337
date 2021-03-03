from Crypto.Cipher import AES
from Crypto import Random
import sys
import time

cbc_key = Random.get_random_bytes(16)
iv = Random.get_random_bytes(16)

# print('='*100)                    
# print('Key used: ', [x for x in cbc_key])
# print("IV used: ", [x for x in iv])
# print('='*100)                    

# Open file
try:
    file_name = sys.argv[1]
    f = open(file_name,'rb')
    plain_text = f.read()
except:
    sys.exit()

# Padding
pad = 16 - len(plain_text) % 16
if pad != 16:
    for i in range(pad):
        plain_text = plain_text.__add__(b'\x00')
#print("Plaintext is: ", plain_text)

# Encrypt
start_time1 = time.time()
aes1 = AES.new(cbc_key, AES.MODE_CBC, iv)
cipher_text = aes1.encrypt(plain_text)
encrypt_time = time.time() - start_time1
#print("Ciphertext is: ",cipher_text)

with open(sys.argv[2], 'wb') as f:
    f.write(cipher_text)

# Decrypt
start_time2 = time.time()
aes2 = AES.new(cbc_key, AES.MODE_CBC, iv)
msg = aes2.decrypt(cipher_text)
decrypt_time = time.time() - start_time2
#print("Original Message", msg)
#print('='*100)

print("Encryption time is: ", encrypt_time)
print("Decryption time is: ", decrypt_time)
