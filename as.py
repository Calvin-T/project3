import hmac
import socket
import sys

"""authentication server program"""

# python as.py asListenPort ts1Hostname ts1ListenPort_a ts2Hostname ts2ListenPort_a


asListenPort = 0


if len(sys.argv) == 6:
	ts1HostName = sys.argv[2]
	ts2HostName = sys.argv[4]
	try:
		asListenPort = int(sys.argv[1])
		ts1ListenPort_a = int(sys.argv[3])
		ts2ListenPort_a = int(sys.argv[5])
	except ValueError:
		exit(1)
else:
	#incorrect arguments
	exit(1)

#create server socket to accept connections from client
try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("[S]: Server socket created")
except socket.error as err:
    #print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', asListenPort)
serverSocket.bind(server_binding)
serverSocket.listen(1)
host = socket.gethostname()
print("[S]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[S]: Server IP address is {}".format(localhost_ip))
csockid, addr = serverSocket.accept()
print("[AS]: Got a connection request from a client at {}".format(addr))


#establish connections to the ts servers

try:
    ts1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("[C]: AS Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()



"""asServer_addr = socket.gethostbyname(asHostname)
print(asServer_addr)
asServer_binding = (asServer_addr, asListenPort)
print(asServer_binding)
asSocket.connect(asServer_binding)"""
ts1_addr = socket.gethostbyname(ts1HostName)
#print(str(asServer_addr))
ts1_binding = (ts1_addr, ts1ListenPort_a)
ts1Socket.connect(ts1_binding)


try:
    ts2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("[C]: AS Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

ts2_addr = socket.gethostbyname(ts2HostName)
#print(str(asServer_addr))
ts2_binding = (ts2_addr, ts2ListenPort_a)
ts2Socket.connect(ts2_binding)




while True:
    recv_msg =csockid.recv(200).decode('utf-8')
    print("[C]: "+ recv_msg)
    split_msg = recv_msg.split()

    if split_msg[0] == "done":
        ts1Socket.send("done".encode('utf-8')) #close the AS to ts1 connection
        ts2Socket.send("done".encode('utf-8'))  # close the AS to ts1 connection
        break
    else:
        split_msg = recv_msg.split()
        challenge = split_msg[0]
        client_digest = split_msg[1]

        ts1Socket.send(challenge.encode('utf-8'))
        ts2Socket.send(challenge.encode('utf-8'))
        
        ts1_digest=ts1Socket.recv(200).decode('utf-8')
        ts2_digest= ts2Socket.recv(200).decode('utf-8')
        print("[TS1] & [TS1]: " + "{} {}".format(ts2_digest, ts1_digest))
        
        if(hmac.compare_digest(ts1_digest,client_digest)): #use compare_digest()
            msg="ts1 "+ts1HostName
            csockid.send(msg.encode('utf-8'))
            print("[AS] to [C]: "+ msg)
        else:
            msg = "ts2 " + ts2HostName
            csockid.send(msg.encode('utf-8'))
            print("[AS] to [C]: " + msg)
            #print("sent ts2")
        #send challenge to ts servers
        #compare the returned digests"""






# Close the server socket
serverSocket.close()
exit()