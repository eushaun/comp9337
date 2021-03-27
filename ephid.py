import random

# generate 16-byte id
def generate_ephid(g):
	x = random.randint(1, 1000000000)
	id_length = len(str(g * x).encode('utf-8'))
	return x, '0' * (16 - id_length) + str(g * x)
