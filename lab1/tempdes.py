from Crypto.Cipher import DES
from Crypto import Random
from binascii import unhexlify
import sys

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

iv = sys.argv[1]
cbc_key = sys.argv[2]

if not is_hex(iv):
    print("Error: IV is not in hexadecimal string")
elif not is_hex(cbc_key):
    print("Error: Key is not in hexadecimal string")
else:
    cbc_key = unhexlify(sys.argv[2])
    print('='*100)
    print('Key used: ', [x for x in cbc_key])

    iv = unhexlify(sys.argv[1])
    print("IV used: ", [x for x in iv])
    print('='*100)

    if len(iv) != 8:
        print("Error: IV is not 8 bytes long")
    elif len(cbc_key) != 8:
        print("Error: Key is not 8 bytes long")
    else:
        des1 = DES.new(cbc_key, DES.MODE_CBC, iv)
        des2 = DES.new(cbc_key, DES.MODE_CBC, iv)

        plain_text = ""
        with open(sys.argv[3], 'r') as f:
            plain_text = f.read().replace('\n', '')

        print("Plaintext is: ", plain_text)

        cipher_text = des1.encrypt(plain_text)
        print("Ciphertext is: ",cipher_text)

        with open(sys.argv[4], 'wb') as f:
            f.write(cipher_text)

        msg = des2.decrypt(cipher_text)
        print("Original Message", msg)
        print('='*100)