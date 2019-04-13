import socket
import sys
import hmac

results = []

if len(sys.argv) == 5:
	asHostname = str(sys.argv[1])
	try:
		asListenPort = int(sys.argv[2])
		ts1ListenPort_c = int(sys.argv[3])
		ts2ListenPort_c = int(sys.argv[4])
	except ValueError:
		exit(1)
else:
	#incorrect arguments
	exit(1)

lines = [line.rstrip('\r\n') for line in open("PROJ3-KEY1.txt")]
ts1Key = lines[0]

lines = [line.rstrip('\r\n') for line in open("PROJ3-KEY2.txt")]
ts2Key = lines[0]

# socket to talk to as server
try:
	asSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
	print('socket open error: {} \n'.format(err))
	exit()

asServer_addr=socket.gethostbyname(asHostname)
asServer_binding=(asServer_addr,asListenPort)
asSocket.connect(asServer_binding)

try:
	ts1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
	print('socket open error: {} \n'.format(err))
	exit()


ts1Server_binding = ("localhost", ts1ListenPort_c)
ts1Socket.connect(ts1Server_binding)

try:
	ts2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
	print('socket open error: {} \n'.format(err))
	exit()


ts2Server_binding = ("localhost", ts2ListenPort_c)
ts2Socket.connect(ts2Server_binding)



asSocket.send("Client says hello")
ts1Socket.send("Client says hello")
ts2Socket.send("Client says hello")


#with open("PROJ3-HNS.txt") as file:
#	lines = [line.rstrip('\r\n') for line in file]
#	for line in lines:
#		split = line.split()
#		key_query = split[0]
#		challenge_query = split[1]
#		query = split[2]
#		
#		digest_query = hmac.new(key_query.encode("utf-8"), challenge_query.encode("utf-8")).hexdigest()
#
#		asSocket.send("{} {}".format(challenge_query, digest_query).encode("utf-8"))
#
#		data_from_as = asSocket.recv(200).decode("utf-8")
#
#		if data_from_as == "ts1.edu":
#			ts1Socket.send(query.encode("utf-8"))
#			data_from_ts = ts1Socket.recv(200)
#			results.append(data_from_ts.decode("utf-8"))
#		elif data_from_as == "ts2.edu":
#			ts2Socket.send(query.encode("utf-8"))
#			data_from_ts = ts2Socket.recv(200)
#			results.append(data_from_ts.decode("utf-8"))
#
#	closing_msg = "done"
#	asSocket.send(closing_msg.encode('utf-8'))
#	ts1Socket.send(closing_msg.encode('utf-8'))
#	ts2Socket.send(closing_msg.encode('utf-8'))
#
#file = open("RESOLVED.txt","w")
#for result in results:
#	file.write(result + "\n")
#file.close()
#
#asSocket.close()
#ts1Socket.close()
#ts2Socket.close()
#exit()
#