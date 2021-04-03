from ecdsa import SigningKey, SECP128r1
from ecdsa.util import randrange
from binascii import hexlify
import random

# ECDSA library: 
# https://github.com/tlsfuzzer/python-ecdsa

# NOTE: the pre-installed ecdsa package in Kali Linux does not include 
# secp128r1 curve, but the above source code does.

# To update the package in Kali Linux, in your working directory,
# cd ~
# git clone https://github.com/tlsfuzzer/python-ecdsa
# sudo cp ~/python-ecdsa/src/*.py /usr/lib/python3/dist-packages/ecdsa

# To install the package in Raspberry Pi,
# from a terminal in Kali Linux,
# scp -r ~/python-ecdsa/src/ecdsa pi@192.168.4.1:~

# then from a terminal in your Raspberry Pi,
# sudo mv ~/ecdsa /usr/lib/python3/dist-packages/

# code snippet taken from 
# https://github.com/tlsfuzzer/python-ecdsa/blob/master/src/ecdsa/keys.py#L829

# FYI: this line works but we don't get the private key aka random number
# sk = SigningKey.generate(curve=SECP128r1)

# generate 16-byte EphID
def generate_ephid():
	curve = SECP128r1
	secexp = randrange(curve.order)
	sk = SigningKey.from_secret_exponent(secexp, curve)
	ephid = sk.to_string()

	return secexp, ephid

# print(generate_ephid())

# def generate_ephid():
# 	g = 2583682
# 	x = random.randint(1, 1000000000)
# 	id_length = len(str(g * x).encode('utf-8'))
# 	return x, '0' * (16 - id_length) + str(g * x)