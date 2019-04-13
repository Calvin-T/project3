import socket
import sys
import hmac

TS1_DNS_Table = {}

if len(sys.argv) == 3:
	try:
		ts1ListenPort_a = int(sys.argv[1])
		ts1ListenPort_c = int(sys.argv[2])
	except ValueError:
		exit(1)
else:
	#incorrect arguments
	exit(1)

lines = [line.rstrip('\r\n') for line in open("PROJ3-KEY1.txt")]
key = lines[0]

lines = [line.rstrip('\r\n') for line in open("PROJ3-DNSTS1.txt")]
for line in lines:
	lineSplit = line.split()
	TS1_DNS_Table[lineSplit[0].lower()] = line


try:
	asSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[S]: Server socket created")
except socket.error as err:
	print('socket open error: {}\n'.format(err))
	exit()

#set up the server socket
as_binding = ('', ts1ListenPort_a)
asSocket.bind(as_binding)
asSocket.listen(1)
assockid, addr = asSocket.accept()

try:
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[S]: Server socket created")
except socket.error as err:
	print('socket open error: {}\n'.format(err))
	exit()

#set up the server socket
server_binding = ('', ts1ListenPort_c)
serverSocket.bind(server_binding)
serverSocket.listen(1)
csockid, addr = serverSocket.accept()

recv_msg = csockid.recv(200)
print recv_msg

csockid.send("TS1 says hello")

recv_msg = assockid.recv(200)
print recv_msg

assockid.send("TS1 says hello")

#while True:
#
#	data_from_as = assockid.recv(200)
#
#	digest_query = hmac.new(key.encode("utf-8"), data_from_as.encode("utf-8"))
#
#	assocket.send(digest_query.encode("utf-8"))
#
#	data_from_client = csockid.recv(200)
#
#	if data_from_client == "done":
#		break
#	else:
#		if data_from_client.lower() in TS1_DNS_Table:
#			send_msg = TS1_DNS_Table[data_from_client.lower()]
#			print("[S]: " + send_msg)
#			csockid.send(send_msg.encode("utf-8"))
#		else:
#			send_msg = data_from_client + " - Error:HOST NOT FOUND"
#			print("[S]: " + send_msg)
#			csockid.send(send_msg.encode('utf-8'))
#