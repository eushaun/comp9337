import binascii
import os
from socket import *
import sys
import threading
import time
from uuid import uuid4
import random
from math import ceil
from decimal import Decimal

port = 37020
broadcast_id = ""

print("[STARTING] UDP Broadcaster is starting...")

#######################
## SHAMIR SHARING #####
#######################

FIELD_SIZE = 100000

def reconstruct_secret(shares):
    sums = 0
    prod_arr = []
 
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        # f(x_n)
        prod *= yj
 
 		# * (x - x_n) / (x_n - x_n-1)
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
 
 
 # generate polynomial of power m
def generate_polynomial(m, secret):
    coeff = [random.randrange(0, FIELD_SIZE) for _ in range(m - 1)]
    coeff.append(secret)
    return coeff
 
 # generate 6 shares
def generate_shares(secret):
	m = 3
	n = 6

	# generate polynomials
	coefficients = generate_polynomial(m, secret)

	# get 3 random points of polynomials
	shares = []
	for i in range(1, n+1):
		x = random.randrange(1, FIELD_SIZE)
		shares.append((x, calculate_poly(x, coefficients)))

	return shares

######################

# Task 1 - 3
def udp_broadcaster():

    # Create socket
    broadcast_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    global port
    global broadcast_id

    # ephID
    broadcast_id = str(uuid4().int)[0:16]
    shares = generate_shares(int(broadcast_id))
    print(f"Make new ID: {broadcast_id}")
    print(shares)

    # timer
    start_time = time.time()
    id_timer = 18
    broadcast_timer = 0
    curr_timer = time.time() - start_time

    while True:
        # broadcast id every 10 seconds
        if curr_timer > broadcast_timer and len(shares) != 0:
            print(f"Broadcast ID: {shares[0]}")
            # broadcast_socket.sendto(broadcast_id.encode('utf-8'), ('192.168.4.255', port))
            broadcast_socket.sendto(str(shares[0]).encode('utf-8'), ('192.168.4.255', port))
            shares.pop(0)
            broadcast_timer += 3
        # create new id every minute
        elif curr_timer > id_timer:
            # id = os.urandom(16)
            broadcast_id = str(uuid4().int)[0:16]
            shares = generate_shares(int(broadcast_id))
            print(f"Make new ID: {broadcast_id}")
            print(shares)
            id_timer += 18

        curr_timer = time.time() - start_time

def udp_receiver():
    server_socket = socket(AF_INET, SOCK_DGRAM) # UDP
    server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    global port
    global broadcast_id
    server_socket.bind(("", port))

    while True:
        recv_id, recv_addr = server_socket.recvfrom(2048)
        recv_id = str(binascii.hexlify(recv_id), "utf-8")
        if broadcast_id != recv_id:
            print("Received ID: ", recv_id)

# thread for listening for beacons
udp_broad_thread = threading.Thread(name = "ClientBroadcaster", target = udp_broadcaster, daemon = True)
udp_broad_thread.start()

udp_receiver_thread = threading.Thread(name = "ClientReceiver", target = udp_receiver)
udp_receiver_thread.start()
