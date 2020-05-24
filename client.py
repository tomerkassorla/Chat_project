# -*- coding: utf-8 -*-
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8077


class Client(object):
    """class client - class that create the connection with the server
    and gives the function receive and send to the client handler"""

    def __init__(self):
        self.send_ip = SERVER_IP
        self.send_port = SERVER_PORT
        self.my_socket = socket.socket()
        self.my_socket.connect((self.send_ip, self.send_port))

    def rcv_message(self):
        """receive a message"""
        return self.my_socket.recv(1024).decode()

    def send_message(self, msg):
        """send a message"""
        self.my_socket.send(bytes(msg, "utf-8"))
