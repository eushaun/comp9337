from bloom import *
from ephid import *
from socket import *
import threading
import time
from hashlib import sha256
from binascii import hexlify, unhexlify
from Crypto.Protocol.SecretSharing import Shamir

# global variable
port = 38000
priv_key = 0
broadcast_hash = ""

print("[STARTING] UDP Broadcaster is starting...")

def print_id(id, recv_shares):
	print()
	print(f"Make new 16-byte ID: {hexlify(id)}")
	for i, recv_share in recv_shares:
		print(f"Share {i}: ({i}, {hexlify(recv_share)})")
	print()

######################

# broadcasting thread
def udp_broadcaster():

	# global port, broadcast_id_recv_shares, broadcast_des1, broadcast_des2, x, g
	global port, broadcast_hash, priv_key

	# create socket
	broadcast_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
	broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	# create new ephID and generate recv_shares
	priv_key, broadcast_id = generate_ephid()
	broadcast_id_recv_shares = Shamir.split(3, 6, broadcast_id)
	
	# hash of ephid
	broadcast_hash = sha256(broadcast_id).hexdigest()

	# print recv_shares and id
	print_id(broadcast_id, broadcast_id_recv_shares)

	# timer
	start_time = time.time()
	id_timer = 18
	broadcast_timer = 0
	curr_timer = time.time() - start_time

	while True:

		# broadcast id every 10 seconds
		if curr_timer > broadcast_timer and len(broadcast_id_recv_shares) != 0:
			print(f"Broadcast recv_share: {broadcast_id_recv_shares[0][0], hexlify(broadcast_id_recv_shares[0][1])}")
			send_str = str(broadcast_id_recv_shares[0][0]) + "|" + hexlify(broadcast_id_recv_shares[0][1]).decode() + "|" + broadcast_hash
			broadcast_socket.sendto(send_str.encode('utf-8'), ('192.168.4.255', port))
			broadcast_id_recv_shares.pop(0)
			broadcast_timer += 3

		# create new id every minute
		elif curr_timer > id_timer:
			# create new ephID and generate recv_shares
			priv_key, broadcast_id = generate_ephid()
			broadcast_id_recv_shares = Shamir.split(3, 6, broadcast_id)
			
			# hash of ephid
			broadcast_hash = sha256(broadcast_id).hexdigest()

			# print recv_shares and id
			print_id(broadcast_id, broadcast_id_recv_shares)

			# set timer
			id_timer += 18

		# update timer
		curr_timer = time.time() - start_time

# receiving thread
def udp_receiver():

	global port, broadcast_hash, priv_key

	QBF = BloomFilter(100)
	QBF_list = []
	
	new_contact_list = {}

	# create socket
	server_socket = socket(AF_INET, SOCK_DGRAM) # UDP
	server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	server_socket.bind(("", port))

	while True:

		# receive message
		recv_msg, recv_addr = server_socket.recvfrom(2048)
		recv_index, recv_share, recv_hash = recv_msg.decode("utf-8").split("|")

		# skip if receive own message
		if recv_hash == broadcast_hash:
			continue
		else:
			# recv_index
			recv_index = int(recv_index)

			# recv_share
			recv_share = unhexlify(recv_share.encode())
			
			if recv_hash not in new_contact_list.keys():
				new_contact_list[recv_hash] = [(recv_index, recv_share)]
			else:
				new_contact_list[recv_hash].append((recv_index, recv_share))
			
			# keep track of number of recv_shares received
			num_recv_shares = len(new_contact_list[recv_hash])
			print()
			print(f"Received {num_recv_shares} recv_shares for {recv_hash}.")
			print()
			
			# Check if the hash contains 3 entries
			if num_recv_shares == 3:
				sec = Shamir.combine(new_contact_list[recv_hash])
				print(f"Reconstructing EphID: {hexlify(sec)}")
				print("Verifying integrity of EphID...")
				new_hash = sha256(sec).hexdigest()
				print()
				print(f"Received hash: 	   {recv_hash}")
				print(f"Recontructed hash: {new_hash}")
				print()
				if recv_hash == new_hash:
					print(f"Verified hash. Computing EncID...")
					enc_id = int(hexlify(sec), 16) * priv_key
					print(f"EncID is: {enc_id}")
				else:
					print("Error: Hash not verified.")
				print()

				QBF.add(str(enc_id))
				print(QBF.bit_array)

# thread for listening for beacons
udp_broad_thread = threading.Thread(name = "ClientBroadcaster", target = udp_broadcaster, daemon = True)
udp_broad_thread.start()

# thread for receiving messages
udp_receiver_thread = threading.Thread(name = "ClientReceiver", target = udp_receiver)
udp_receiver_thread.start()
