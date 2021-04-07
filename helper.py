from binascii import hexlify, unhexlify

def print_id(id, recv_shares):
	print()
	print(f"Make new 16-byte ID: {hexlify(id)}")
	for i, recv_share in recv_shares:
		print(f"Share {i}: ({i}, {hexlify(recv_share)})")
	print()
