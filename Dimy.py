import binascii
import os
from socket import *
import sys
import threading
import time

port = 37020
broadcast_id_str = ""

print("[STARTING] UDP Broadcaster is starting...")

# Task 1 - 3
def udp_broadcaster():

    # Create socket
    broadcast_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    global port
    global broadcast_id_str

    # ephID
    id = os.urandom(16)
    broadcast_id_str = str(binascii.hexlify(id), "utf-8")
    print(f"Make new ID: {broadcast_id_str}")

    # timer
    start_time = time.time()
    id_timer = 60
    broadcast_timer = 0
    curr_timer = time.time() - start_time

    while True:

        # broadcast id every 10 seconds
        if curr_timer > broadcast_timer:
            print(f"Broadcast ID: {broadcast_id_str}")
            broadcast_socket.sendto(id, ('192.168.4.255', port))
            broadcast_timer += 10
        # create new id every minute
        elif curr_timer > id_timer:
            id = os.urandom(16)
            broadcast_id_str = str(binascii.hexlify(id), "utf-8")
            print(f"Make new ID: {broadcast_id_str}")
            id_timer += 60

        curr_timer = time.time() - start_time

def udp_receiver():
    server_socket = socket(AF_INET, SOCK_DGRAM) # UDP
    server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    global port
    global broadcast_id_str
    server_socket.bind(("", port))

    while True:
        recv_id, recv_addr = server_socket.recvfrom(2048)
        recv_id = str(binascii.hexlify(recv_id), "utf-8")
        if broadcast_id_str != recv_id:
            print("Received ID: ", recv_id)

# thread for listening for beacons
udp_broad_thread = threading.Thread(name = "ClientBroadcaster", target = udp_broadcaster, daemon = True)
udp_broad_thread.start()

udp_receiver_thread = threading.Thread(name = "ClientReceiver", target = udp_receiver)
udp_receiver_thread.start()
