# custom library files
from bloom import *
from ephid import *
from helper import *
from sender import *

# imported library
from binascii import hexlify, unhexlify
from Crypto.Protocol.SecretSharing import Shamir
from hashlib import sha256
from socket import *
import threading
import time
from copy import deepcopy

# global variable
port = 40000
priv_key = 0
broadcast_hash = ""
filter_size = 800000
dbf = BloomFilter(filter_size)
dbf_list = []
covid = 0
old_hash = 0


print(f"[STARTING] Program is starting on port {port}.")

######################

# thread to broadcast shares
def udp_broadcaster():

	global port, broadcast_hash, priv_key, old_hash

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
	broadcast_timer = 10		# 10 seconds
	id_timer = 60				# 1 minute
	curr_timer = time.time() - start_time

	while True:

		# broadcast id every 10 seconds
		if curr_timer > broadcast_timer and len(broadcast_id_recv_shares) != 0:
			print(f"[TASK 3A] Broadcasting shares: {broadcast_id_recv_shares[0][0], hexlify(broadcast_id_recv_shares[0][1])}")
			send_str = str(broadcast_id_recv_shares[0][0]) + "|" + hexlify(broadcast_id_recv_shares[0][1]).decode() + "|" + broadcast_hash
			broadcast_socket.sendto(send_str.encode('utf-8'), ('192.168.4.255', port))
			broadcast_id_recv_shares.pop(0)
			broadcast_timer += 10

		# create new id every minute
		elif curr_timer > id_timer:
			# create new ephID and generate recv_shares
			priv_key, broadcast_id = generate_ephid()
			broadcast_id_recv_shares = Shamir.split(3, 6, broadcast_id)
			
			# hash of ephid
			old_hash = broadcast_hash
			broadcast_hash = sha256(broadcast_id).hexdigest()

			# print recv_shares and id
			print_id(broadcast_id, broadcast_id_recv_shares)

			# set timer
			id_timer += 60

		# update timer
		curr_timer = time.time() - start_time

# thread to receive shares
def udp_receiver():

	global port, broadcast_hash, priv_key, dbf, old_hash
	
	new_contact_list = {}

	dbf.restart()

	# create socket
	server_socket = socket(AF_INET, SOCK_DGRAM) # UDP
	server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	server_socket.bind(("", port))

	print("Waiting to receive shares from other devices...")
	print()

	while True:
		# receive message
		recv_msg, _ = server_socket.recvfrom(2048)
		recv_index, recv_share, recv_hash = recv_msg.decode("utf-8").split("|")

		# skip if receive own message
		if recv_hash == broadcast_hash or recv_hash == old_hash:
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
			# print()
			print(f"[TASK 3B/3C] Received {num_recv_shares} recv_shares for {recv_hash}.")
			print()
			
			# Check if the hash contains 3 entries
			if num_recv_shares == 3:
				sec = Shamir.combine(new_contact_list[recv_hash])
				print()
				print(f"[TASK 4A] Reconstructing EphID: {hexlify(sec)}")
				print("[TASK 4B] Verifying integrity of EphID...")
				new_hash = sha256(sec).hexdigest()
				print()
				print(f"Received hash: 	   {recv_hash}")
				print(f"Recontructed hash: {new_hash}")
				print()
				if recv_hash == new_hash:
					print("Verified hash. Computing EncID...")
					enc_id = int(hexlify(sec), 16) * priv_key
					print(f"[TASK 5A/5B] EncID is: {enc_id}")
					print("[TASK 6] Adding EncID to DBF and deleting EncID...")
					dbf.add(str(enc_id))
					print()
					print(f"[TASK 7A] Current state of DBF: {dbf.get_indices()}")
					print()
				else:
					print("Error: Hash not verified.")
					print()

# thread to deal with backend API
def udp_sender():

	global dbf, dbf_list, filter_size, covid

	qbf = BloomFilter(filter_size)

	start_time = time.time()
	dbf_timer = 600		# 10 minutes
	qbf_timer = 3600  	# 60 minutes
	curr_timer = time.time() - start_time

	while not covid:
		if curr_timer > dbf_timer:
			# remove oldest DBF
			if len(dbf_list) == 6:
				dbf_list.pop(0)

			dbf_list.append(deepcopy(dbf))	
			dbf.restart()
			dbf_timer += 600

			print()
			print(f"[TASK 7B] Creating new DBF...")
			print()

		if curr_timer > qbf_timer:
			# print debug messages
			print()
			print("All available DBFs:")
			for i, bf in enumerate(dbf_list):
				print(f"DBF {i+1}: {bf.get_indices()}")
			print()
			qbf.merge(dbf_list)
			print(f"[TASK 8] Creating QBF: {qbf.get_indices()}")
			print("[TASK 9A] Sending QBF to server, waiting for result...")
			print()
			resp = send_qbf(qbf.bit_array)
			print(f"[TASK 9B] Query result: {resp['result']}. {resp['message']}")
			print()
			qbf_timer += 3600

		# update timer
		curr_timer = time.time() - start_time

def monitor_input():
	global dbf, dbf_list, filter_size, covid

	# wait till the first dbf has generated
	time.sleep(600)		# follow dbf_timer

	print("##############################################################")
	print("#                                                            #")
	print("#     Type 'uploadcbf' to upload your CBF to the server      #")
	print("#                                                            #")
	print("##############################################################")
	print()

	# listen for input from user
	while True:
		command = input()
		if command == 'uploadcbf':  
			# print messages
			print()
			print("User has COVID-19. The program will stop generating QBFs now.")
			print("[TASK 10] Uploading CBF to the backend server...")
			print()

			# create CBF
			covid = 1
			cbf = BloomFilter(filter_size)
			cbf.merge(dbf_list)
			send_cbf(cbf.bit_array)
			print("Upload success")
			break

# thread for listening for beacons
udp_broad_thread = threading.Thread(name = "ClientBroadcaster", target = udp_broadcaster)
udp_broad_thread.start()

# thread for receiving messages
udp_sender_thread = threading.Thread(name = "ClientSender", target = udp_sender)
udp_sender_thread.start()

# thread for receiving messages
udp_receiver_thread = threading.Thread(name = "ClientReceiver", target = udp_receiver)
udp_receiver_thread.start()

# thread for monitoring user input
monitor_input_thread = threading.Thread(name = "MonitorInput", target = monitor_input)
monitor_input_thread.start()