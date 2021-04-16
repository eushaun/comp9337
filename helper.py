from binascii import hexlify, unhexlify

def print_id(id, recv_shares):
	print()
	print(f"[TASK 1] Make new 16-byte ID: {hexlify(id)}")
	for i, recv_share in recv_shares:
		print(f"[TASK 2] Share {i}: ({i}, {hexlify(recv_share)})")
	print()