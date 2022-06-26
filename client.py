from ast import arg
from email import message
import socket
import threading
import time
import sys

#if type is 0, we have no deadline
#else if type is 1 , it means that we are waiting for ack
#so it should be recieved in 10 seconds
def recieve_handler(conn, type):
    ack_recv = False
    t1 = time.time()
    while True:
        if(time.time() - t1 > 10 and type == 1 and not ack_recv):
            print("server response time exceeded 10 seconds")
            break
        try:
            data = conn.recv(1024)
        except Exception:
            print("failed to recieve data")
        if data.decode() == "ping":
            conn.sendall("pong".encode())
        elif data.decode() == "pong":
            print(data.decode())
            break
        elif "ack" in data.decode():
            print(data.decode())
            ack_recv = True
            if data.decode() == "puback":
                break
        elif len(data.decode()) > 0 and "ping" not in data.decode():
            print(data.decode())

        

def main(argv):
    serverInformation = (argv[1], int(argv[2]))
    #connect to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(serverInformation)
            print("Connection to server...")
        except Exception:
            print("Connection failed")
        msg_type = argv[3]
        #initialize message
        msg = msg_type
        if msg_type == "subscribe":
            #add topics to message
            for i in range(4, len(argv)):
                msg += " "
                msg += argv[i]
            s.sendall(msg.encode())
            recieve_handler(s, 1)

        elif msg_type == "publish":
            #add topic
            msg += " "
            msg += argv[4]
            for i in range(5, len(argv)):
                msg += " "
                msg += argv[i]
            s.sendall(msg.encode())
            recieve_handler(s,1)
        
        elif msg_type == "ping":
            s.sendall(msg.encode())
            recieve_handler(s, 0)
        
        else:
            print("invalid command")
            




if __name__ == '__main__':
    main(sys.argv)