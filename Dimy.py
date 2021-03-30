from ephid import *
from Crypto.Cipher import DES
from shamir import *
from socket import *
import threading
import time
from hashlib import sha1

# global variable
port = 37025
broadcast_id_shares = []

g = 2583682
x = 0

# broadcast_key = 'fecdba98'
# broadcast_iv = '01234567'
# broadcast_des1 = DES.new(broadcast_key, DES.MODE_CBC, broadcast_iv)
# broadcast_des2 = DES.new(broadcast_key, DES.MODE_CBC, broadcast_iv)
broadcast_hash = ""

print("[STARTING] UDP Broadcaster is starting...")

######################

# broadcast Shares
def udp_broadcaster():

	# global port, broadcast_id_shares, broadcast_des1, broadcast_des2, x, g
	global port, broadcast_id_shares, broadcast_hash, x, g

	# create socket
	broadcast_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
	broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	# create new ephID
	x, broadcast_id = generate_ephid(g)
	broadcast_id_shares = generate_shares(int(broadcast_id))

	broadcast_hash = sha1(str(broadcast_id).encode()).hexdigest()
	# broadcast_hash = broadcast_des1.encrypt(broadcast_id)

	print()
	print(f"Make new ID: {broadcast_id}")
	for i, shares in enumerate(broadcast_id_shares):
		print(f"Share {i+1}: {shares}")
	print()

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
			x, broadcast_id = generate_ephid(g)
			broadcast_id_shares = generate_shares(int(broadcast_id))

			broadcast_hash = sha1(str(broadcast_id).encode()).hexdigest()
			# broadcast_hash = broadcast_des1.encrypt(broadcast_id)

			print()
			print(f"Make new ID: {broadcast_id}")
			for i, shares in enumerate(broadcast_id_shares):
				print(f"Share {i+1}: {shares}")
			print()
			id_timer += 18

		curr_timer = time.time() - start_time

def udp_receiver():

	# global port, broadcast_id, broadcast_des2
	global port, broadcast_hash, x
	
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
			# print(f"Received ({recv_x}, {recv_y}) - Hash = {recv_hash}")
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

			# # Check if the hash contains 3 entries 
			# new_dict = {}
			# for curr_hash in new_contact_list.keys():
			# 	lst = new_contact_list[curr_hash]
			# 	if len(lst) == 3:
			# 		sec = reconstruct_secret(lst)
			# 		print(f"Reconstructing EphID: {sec}")
			# 		print("Verifying integrity of EphID...")
			# 		new_hash = sha1(str(sec).encode()).hexdigest()
			# 		print(f"Received hash: {recv_hash}")
			# 		print(f"Recontructed hash: {new_hash}")
			# 		if recv_hash == new_hash:
			# 			print("Verified hash. Computing EncID...")
			# 			enc_id = sec * x
			# 			print(f"EncID is: {enc_id}")
			# 	else:
			# 		new_dict[curr_hash] = lst
			# new_contact_list = new_dict
			

# thread for listening for beacons
udp_broad_thread = threading.Thread(name = "ClientBroadcaster", target = udp_broadcaster, daemon = True)
udp_broad_thread.start()

udp_receiver_thread = threading.Thread(name = "ClientReceiver", target = udp_receiver)
udp_receiver_thread.start()
