import socket
import sys
import hmac
import threading

#py ts1.py ts1ListenPort_a ts1ListenPort_c
def client_connection():

    TS1_DNS_Table = {}
    lines = [line.rstrip('\r\n') for line in open("PROJ3-DNSTS1.txt")]
    for line in lines:
        lineSplit = line.split()
        TS1_DNS_Table[lineSplit[0].lower()] = line

    #create the socket that will accept connections from the client
    try:
        c_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    c_binding = ('', ts1ListenPort_c)
    c_Socket.bind(c_binding)
    c_Socket.listen(1)

    csockid, addr = c_Socket.accept()

    while True:
        query=csockid.recv(200).decode('utf-8')
        if query=="done":
            break
        else:
            if query.lower() in TS1_DNS_Table:
                send_msg = TS1_DNS_Table[query.lower()]
                print("[S]: " + send_msg)
                csockid.send(send_msg.encode("utf-8"))
            else:
                send_msg=query+" - Error:HOST NOT FOUND"
                csockid.send(send_msg.encode("utf-8"))

    c_Socket.close()
    exit()



def as_connection():
    with open("PROJ3-KEY1.txt") as file:
        key = file.readline().rstrip('\r\n')

    # setup socket to accept connections from AS
    try:
        AS_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("[S]: Server socket created")
    except socket.error as err:
        # print('socket open error: {}\n'.format(err))
        exit()

    AS_binding = ('', ts1ListenPort_a)
    AS_Socket.bind(AS_binding)
    AS_Socket.listen(1)
    # host = socket.gethostname()
    # print("[S]: Server host name is {}".format(host))
    # localhost_ip = (socket.gethostbyname(host))
    # print("[S]: Server IP address is {}".format(localhost_ip))
    ASsockid, addr = AS_Socket.accept()

    while True:
        challenge = ASsockid.recv(200).decode('utf-8')
        # received challenge string from as
        if challenge == "done":
            break
        else:
            digest = hmac.new(key.encode("utf-8"), challenge.encode("utf-8"))
            # generate digest based on own key
            print("[TS1]: " + digest.hexdigest())

            # send generated challenge string back to as server

            ASsockid.send("{}".format(digest.hexdigest()).encode('utf-8'))

    #print("done")
    AS_Socket.close()
    exit()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            ts1ListenPort_a = int(sys.argv[1])
            ts1ListenPort_c = int(sys.argv[2])
        except ValueError:
            exit(1)
    else:
        # incorrect arguments
        exit(1)

    AS=threading.Thread(name='AS', target=as_connection)
    client= threading.Thread(name='client', target=client_connection)
    AS.start()
    client.start()
