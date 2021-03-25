from binascii import unhexlify
from Crypto.Cipher import DES
from decimal import Decimal
from math import ceil
import os
import random
from socket import *
import sys
import threading
import time
from uuid import uuid4

# gLobal Variable
port = 37020
broadcast_id_shares = []
FIELD_SIZE = 100000

broadcast_key = 'fecdba98'
broadcast_iv = '01234567'
broadcast_des1 = DES.new(broadcast_key, DES.MODE_CBC, broadcast_iv)
broadcast_des2 = DES.new(broadcast_key, DES.MODE_CBC, broadcast_iv)

print("[STARTING] UDP Broadcaster is starting...")

def reconstruct_secret(shares):
    sums = 0
    prod_arr = []
 
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        prod *= yj
        
        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi)/(xi-xj))
 
        sums += Decimal(prod)
 
    return int(round(Decimal(sums), 0))
 
# calculate value of poly at x
def calculate_poly(x, coefficients):
    y = 0
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        y += x ** coefficient_index * coefficient_value
    return y
 
 # generate 6 shares
def generate_shares(secret):
	m = 3
	n = 6

	# generate polynomials
	coefficients = [random.randrange(0, FIELD_SIZE) for _ in range(m - 1)]
	coefficients.append(secret)

	# get 3 random points of polynomials
	shares = []
	for i in range(1, n+1):
		x = random.randrange(1, FIELD_SIZE)
		shares.append((x, calculate_poly(x, coefficients)))

	return shares

######################

# broadcast Shares
def udp_broadcaster():

	global port, broadcast_id_shares, broadcast_des1, broadcast_des2

	# create socket
	broadcast_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
	broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	# create new ephID
	broadcast_id = str(uuid4().int)[0:16]
	broadcast_id_shares = generate_shares(int(broadcast_id))
	broadcast_hash = broadcast_des1.encrypt(broadcast_id)
	print(f"Make new ID: {broadcast_id}")
	print(broadcast_id_shares)

	# timer
	start_time = time.time()
	id_timer = 18
	broadcast_timer = 0
	curr_timer = time.time() - start_time

	while True:

		# broadcast id every 10 seconds
		if curr_timer > broadcast_timer and len(broadcast_id_shares) != 0:
			print(f"Broadcast ID: {broadcast_id_shares[0]}")
			send_str = str(broadcast_id_shares[0][0]) + "|" + str(broadcast_id_shares[0][1]) + "|" + str(broadcast_hash)
			broadcast_socket.sendto(send_str.encode('utf-8'), ('192.168.4.255', port))
			broadcast_id_shares.pop(0)
			broadcast_timer += 3

		# create new id every minute
		elif curr_timer > id_timer:
			broadcast_id = str(uuid4().int)[0:16]
			broadcast_id_shares = generate_shares(int(broadcast_id))
			broadcast_hash = broadcast_des1.encrypt(broadcast_id)
			print(f"Make new ID: {broadcast_id}")
			print(broadcast_id_shares)
			id_timer += 18

		curr_timer = time.time() - start_time

def udp_receiver():

	global port, broadcast_id, broadcast_des2

	# create socket
	server_socket = socket(AF_INET, SOCK_DGRAM) # UDP
	server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	server_socket.bind(("", port))

	while True:

		# receive message
		recv_msg, recv_addr = server_socket.recvfrom(2048)
		recv_x, recv_y, recv_hash = recv_msg.decode("utf-8").split("|")
		recv_hash = recv_hash[2:len(recv_hash) - 1 ]
		print(len(recv_hash))
		#str(recv_id.decode("utf-8")).split("|")
		#print(recv_msg.decode("utf-8").split("|"))
		#print(broadcast_des2.decrypt(recv_hash))
		print(f"Received ({recv_x}, {recv_y}) - Hash = {recv_hash}")

# thread for listening for beacons
udp_broad_thread = threading.Thread(name = "ClientBroadcaster", target = udp_broadcaster, daemon = True)
udp_broad_thread.start()

udp_receiver_thread = threading.Thread(name = "ClientReceiver", target = udp_receiver)
udp_receiver_thread.start()
