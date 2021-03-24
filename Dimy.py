import binascii
import os
from socket import *
import sys
import threading
import time

broadcast_id_str = ""

# create sending and receiving UDP sockets for peer-to-peer
udp_broadcast_socket = socket(AF_INET, SOCK_DGRAM)
udp_broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

server_host = gethostbyname(gethostname())
udp_server = socket(AF_INET, SOCK_DGRAM)
udp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
udp_server.bind((server_host, 55558))

print("[STARTING] UDP Broadcaster is starting...")

# Task 1 - 3
def udp_broadcaster():
    
    global broadcast_id_str
    global udp_broadcast_socket

    host = '255.255.255.255'
    port = 55558

    # ephID
    broadcast_id = os.urandom(16)
    broadcast_id_str = str(binascii.hexlify(broadcast_id), "utf-8")
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
            udp_broadcast_socket.sendto(broadcast_id, (host, port))
            broadcast_timer += 10
        # create new id every minute
        elif curr_timer > id_timer:
            broadcast_id = os.urandom(16)
            broadcast_id_str = str(binascii.hexlify(broadcast_id), "utf-8")
            print(f"Make new ID: {broadcast_id_str}")
            id_timer += 60

        curr_timer = time.time() - start_time

def udp_receiver():

    global udp_server
    global broadcast_id_str

    # print("Listening")
    while True:
        recv_id, recv_addr = udp_server.recvfrom(2048)
        recv_id = str(binascii.hexlify(recv_id), "utf-8")
        if broadcast_id_str != recv_id:
            print("Received ID: ", recv_id)

# thread for listening for beacons
udp_broad_thread = threading.Thread(name = "ClientBroadcaster", target = udp_broadcaster, daemon = True)
udp_broad_thread.start()

udp_receiver_thread = threading.Thread(name = "ClientReceiver", target = udp_receiver)
udp_receiver_thread.start()