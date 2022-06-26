from audioop import add
from email import message
from email.headerregistry import Address
from http import client
from os import remove
from pydoc import cli
import socket
from tarfile import ENCODING
import threading

ADDRESS = '127.0.0.1'
PORT = 1373
HOST_INFORMATION = (ADDRESS, PORT)

class Client:
    def __init__(self, conn, addr) -> None:
        self.connection = conn
        self.address = addr
        self.subscribing = []
    
    def send_msg(self, msg):
        self.connection.sendall(msg.encode())
    
    def subscribe(self, topic):
        self.subscribing.append(topic)

        


def handler(client, clients):
    with client.connection:
        print('Connected by', client.address)
        while True:
            data = client.connection.recv(1024).decode()
            if data:
                if 'subscribe' in data:
                    words = data.split(' ')
                    for word in words:
                        if word != 'subscribe':
                            client.subscribe(word)
                            client.send_msg("suback")
                elif 'publish' in data:
                    words = data.split(' ')
                    topic = words[1]
                    message = words[2:]
                    publish(topic, message, clients)
                    client.send_msg("puback")
                elif 'ping' in data:
                    client.send_msg("pong")


def publish(topic, message, clients):
    for client in clients:
        if topic in client.subscribing:
            msg = topic + " : "
            for word in message:
                msg+=" "
                msg+=word
            client.send_msg(msg)

def main():
    clients = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(HOST_INFORMATION)
        s.listen()
        print("server is listening on port {PORT}")
        while True:
            conn , addr = s.accept()
            client = Client(conn, addr)
            clients.append(client)
            threading.Thread(target=handler, args=(client,clients)).start()


if __name__ == '__main__':
    main()