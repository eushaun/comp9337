from pypresent import Present
import sys
import time

# Encrypting with a 128-bit key:
# -------------------------------
key = "0123456789abcdef0123456789abcdef".decode('hex')
cipher = Present(key)

# print('='*100)                   
# print('Key used: ', key.encode('hex'))
# print('='*100)

# Open file
try:
    file_name = sys.argv[1]
    f = open(file_name,'rb')
    # Plain text should be even-length
    plain_text = f.read().decode('hex')
except:
    sys.exit()

# plain_text = "0123456789abcdef".decode('hex') # <- 16 bytes
# print("Plaintext is: ", plain_text.encode('hex'))

# Encrypt
start_time1 = time.time()
cipher_text = cipher.encrypt(plain_text)
encrypt_time = time.time() - start_time1
# print("Ciphertext is: ", cipher_text.encode('hex'))

with open(sys.argv[2], 'wb') as f:
    f.write(cipher_text)

# Decrypt
start_time2 = time.time()
msg = cipher.decrypt(cipher_text)
decrypt_time = time.time() - start_time2
# print("Decrypted message: ", msg.encode('hex'))
# print('='*100)

print("Encryption time is: ", encrypt_time)
print("Decryption time is: ", decrypt_time)