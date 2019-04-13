import socket
import sys

if len(sys.argv) == 6:
	ts1Hostname = sys.argv[2]
	ts2Hostname = sys.argv[4]
	try:
		asListenPort = int(sys.argv[1])
		ts1ListenPort_a = int(sys.argv[3])
		ts2ListenPort_a = int(sys.argv[5])
	except ValueError:
		exit(1)
else:
	#incorrect arguments
	exit(1)

try:
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[AS]: Server socket created")
except socket.error as err:
	print('socket open error: {}\n'.format(err))
	exit()

server_binding = ('', asListenPort)
serverSocket.bind(server_binding)
serverSocket.listen(1)
csockid, addr = serverSocket.accept()

try:
	ts1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
	print('socket open error: {} \n'.format(err))
	exit()


ts1Server_binding = (ts1Hostname, ts1ListenPort_a)
ts1Socket.connect(ts1Server_binding)

try:
	ts2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
	print('socket open error: {} \n'.format(err))
	exit()

ts2Server_binding = (ts2Hostname, ts2ListenPort_a)
ts2Socket.connect(ts2Server_binding)

recv_msg = csockid.recv(200)
print(recv_msg)

ts1Socket.send("AS says hello")
ts2Socket.send("AS says hello")
csockid.send("AS says hello")

#while True:
#	data_from_client = csockid.recv(200)
#	recv_msg = data_from_client.decode("utf-8")
#
#	print("[CS]: " + recv_msg)
#
#	split_msg = recv_msg.split()
#	challenge_query = split[0]
#	digest_query = split[1]
#
#	ts1Socket.send(challenge_query.encode("utf-8"))
#	ts1_digest_query = ts1Socket.recv(200)
#
#	ts2.Socket.send(challenge_query.encode("utf-8"))
#	ts2_digest_query = ts2Socket.recv(200)
#
#	if ts1_digest_query == digest_query:
#		csockid.send("ts1.edu".encode("utf-8"))
#	elif ts2_digest_query == digest_query:
#		csockid.send("ts2.edu".encode("utf-8"))
#	else:
#		print("neither digest == to given")
#
#
#
#	if recv_msg == "done":
#		break
#