import socket
import sys
import hmac

# arguments client.py asHostname asListenPort ts1ListenPort_c ts2ListenPort_c

results = []

# check command line arguments
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

# socket to talk to AS server
try:
    asSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: AS Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

asServer_addr = socket.gethostbyname(asHostname)
print(asServer_addr)
asServer_binding = (asServer_addr, asListenPort)
print(asServer_binding)
asSocket.connect(asServer_binding)
print("[C]: got a connection to AS Server")

with open("PROJ3-HNS.txt") as file:
    lines = [line.rstrip('\r\n') for line in file]
    for line in lines:
        lineSplit = line.split()
        key = lineSplit[0]
        challenge = lineSplit[1]
        query = lineSplit[2]


        # generate the digest string using the key and challenge string
        #digest = hmac.new(key.encode("utf-8"), challenge.encode("utf-8"))


        # send challenge string and the generated digest seperately to the asServer

        digest = hmac.new(key.encode("utf-8"), challenge.encode("utf-8")).hexdigest()
        asSocket.send("{} {}".format(challenge, digest).encode("utf-8"))
       #asSocket.send(challenge.encode('utf-8'))
        print("[C] to [AS]: " + "{} {}".format(challenge, digest))
        #asSocket.send(str(digest).encode('utf-8'))

        data_AS = asSocket.recv(200).decode('utf-8') # return the hostname of ts server to query
        # return ts1/2 ts_hostname
        print("[AS] to [C]: "+data_AS)
        data_AS=data_AS.split()
        ts_server = data_AS[0]
        ts_hostname = data_AS[1]

        if ts_server == "ts1":
            for attempt in range(2):
                try:
                    # print("[C]: " + line)
                    ts1Socket.send(query.encode('utf-8'))
                    ts_msg = ts1Socket.recv(200).decode('utf-8')
                    results.append(ts_msg)
                    # print("[TS]: " + msg_received)
                    break;
                except:
                    # open socket
                    try:
                        ts1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # print("[C]: TS Client socket created")
                    except socket.error as err:
                        print('socket open error: {} \n'.format(err))
                        exit()

                    ts1Server_addr = socket.gethostbyname(ts_hostname)
                    ts1Server_binding = (ts1Server_addr, ts1ListenPort_c)
                    ts1Socket.connect(ts1Server_binding)
        else:
            for attempt in range(2):
                try:
                    # print("[C]: " + line)
                    ts2Socket.send(query.encode('utf-8'))
                    ts_msg = ts2Socket.recv(200).decode('utf-8')
                    results.append(ts_msg)
                    break;
                except:
                    # open socket
                    try:
                        ts2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # print("[C]: TS Client socket created")
                    except socket.error as err:
                        print('socket open error: {} \n'.format(err))
                        exit()

                    ts2Server_addr = socket.gethostbyname(ts_hostname)
                    ts2Server_binding = (ts2Server_addr, ts2ListenPort_c)
                    ts2Socket.connect(ts2Server_binding)


        #print("send query: "+ query+" to "+ ts_hostname)



        """create a socket using ts_hostname and portNumber
        then send query over the connection and await response"""

    # results.append(data_from_ASserver.decode('utf-8'))
    # print(data_from_ASserver.decode('utf-8'))

    closing_msg = "done"
    asSocket.send(closing_msg.encode('utf-8'))
    try:
        ts1Socket.send("done".encode('utf-8'))
    except:
        pass
    try:
        ts2Socket.send("done".encode('utf-8'))
    except:
        pass



file = open("RESOLVED.txt", "w")
for result in results:
    file.write(result + "\n")
file.close()

asSocket.close()
exit()
