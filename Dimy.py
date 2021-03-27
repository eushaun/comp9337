from ephid import *
from Crypto.Cipher import DES
from shamir import *
from socket import *
import threading
import time

# gLobal Variable
port = 37020
broadcast_id_shares = []

g = 2583682
x = 0

broadcast_key = 'fecdba98'
broadcast_iv = '01234567'
broadcast_des1 = DES.new(broadcast_key, DES.MODE_CBC, broadcast_iv)
broadcast_des2 = DES.new(broadcast_key, DES.MODE_CBC, broadcast_iv)

print("[STARTING] UDP Broadcaster is starting...")

######################

# broadcast Shares
def udp_broadcaster():

	global port, broadcast_id_shares, broadcast_des1, broadcast_des2, x, g

	# create socket
	broadcast_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
	broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	# create new ephID
	x, broadcast_id = generate_ephid(g)
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
			x, broadcast_id = generate_ephid(g)
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
