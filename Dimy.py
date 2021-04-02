from bloom import *
from ephid import *
from shamir import *
from socket import *
import threading
import time
from hashlib import sha1

# global variable
port = 37030
x = 0
broadcast_hash = ""

print("[STARTING] UDP Broadcaster is starting...")

def print_id(id, shares):
	print()
	print(f"Make new ID: {id}")
	for i, shares in enumerate(shares):
		print(f"Share {i+1}: {shares}")
	print()

######################

# broadcast Shares
def udp_broadcaster():

	# global port, broadcast_id_shares, broadcast_des1, broadcast_des2, x, g
	global port, broadcast_hash, x, g

	# create socket
	broadcast_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
	broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	# create new ephID
	x, broadcast_id = generate_ephid()
	broadcast_id_shares = generate_shares(int(broadcast_id))

	# hash of ephid
	broadcast_hash = sha1(str(broadcast_id).encode()).hexdigest()

	# print shares and id
	print_id(broadcast_id, broadcast_id_shares)

	# timer
	start_time = time.time()
	id_timer = 18
	broadcast_timer = 0
	curr_timer = time.time() - start_time

	while True:

		# broadcast id every 10 seconds
		if curr_timer > broadcast_timer and len(broadcast_id_shares) != 0:
			print(f"Broadcast share: {broadcast_id_shares[0]}")
			send_str = str(broadcast_id_shares[0][0]) + "|" + str(broadcast_id_shares[0][1]) + "|" + broadcast_hash
			broadcast_socket.sendto(send_str.encode('utf-8'), ('192.168.4.255', port))
			broadcast_id_shares.pop(0)
			broadcast_timer += 3

		# create new id every minute
		elif curr_timer > id_timer:
			x, broadcast_id = generate_ephid()
			broadcast_id_shares = generate_shares(int(broadcast_id))
			broadcast_hash = sha1(str(broadcast_id).encode()).hexdigest()
			print_id(broadcast_id, broadcast_id_shares)
			id_timer += 18

		# update timer
		curr_timer = time.time() - start_time

def udp_receiver():

	global port, broadcast_hash, x

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
		recv_x, recv_y, recv_hash = recv_msg.decode("utf-8").split("|")

		# skip if receive own message
		if recv_hash == broadcast_hash:
			continue
		else:
			recv_x = int(recv_x)
			recv_y = int(recv_y)
			
			if recv_hash not in new_contact_list.keys():
				new_contact_list[recv_hash] = [(recv_x, recv_y)]
			else:
				new_contact_list[recv_hash].append((recv_x, recv_y))
			
			# keep track of number of shares received
			num_shares = len(new_contact_list[recv_hash])
			print()
			print(f"Received {num_shares} shares for {recv_hash}.")
			print()
			
			# Check if the hash contains 3 entries
			if num_shares == 3:
				sec = reconstruct_secret(new_contact_list[recv_hash])
				print()
				print(f"Reconstructing EphID: {sec}")
				print("Verifying integrity of EphID...")
				new_hash = sha1(str(sec).encode()).hexdigest()
				print(f"Received hash: {recv_hash}")
				print(f"Recontructed hash: {new_hash}")
				if recv_hash == new_hash:
					print("Verified hash. Computing EncID...")
					enc_id = sec * x
					print(f"EncID is: {enc_id}")
				print()

				QBF.add(str(enc_id))
				print(QBF.bit_array)

# thread for listening for beacons
udp_broad_thread = threading.Thread(name = "ClientBroadcaster", target = udp_broadcaster, daemon = True)
udp_broad_thread.start()

udp_receiver_thread = threading.Thread(name = "ClientReceiver", target = udp_receiver)
udp_receiver_thread.start()
