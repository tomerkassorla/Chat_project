__author__ = 'User'

import threading
import time
import socket
from database import *

DIC_SOCK_NAME = {}


class ClientHandler(threading.Thread):
    def __init__(self, address, client_socket, database, dict_name_client_handler):
        super(ClientHandler, self).__init__()
        self.my_socket = client_socket
        self._name = address
        self.sender_name = ''
        self.database = database
        self.dict_name_client_handler = dict_name_client_handler

    def rcv_message(self):
        return self.my_socket.recv(1024).decode()

    def send_message(self, msg):
        self.my_socket.send(bytes(msg, "utf-8"))

    def run(self):
        ok = True
        while ok:
            msg = self.rcv_message()  # first receive from client
            print(msg)
            print(self.database.read())
            if "#" in msg:  # handle the sign_up with the database
                list_sign_up = msg.split("#")
                if not self.database.check_if_username_in_database(
                        list_sign_up[0]):  # return false if username in database
                    self.send_message("username in use")
                else:
                    ok = False
                    self.send_message("ok " + list_sign_up[0])
                    self.database.write(list_sign_up)
                    self.sender_name = list_sign_up[0]
            else:  # handle the login
                list_login = msg.split()
                if not self.database.check_if_username_password_in_database(list_login) or list_login[
                    0] in self.dict_name_client_handler:
                    self.send_message("wrong username or password")
                else:
                    ok = False
                    self.send_message("ok " + list_login[0])
                    self.sender_name = list_login[0]
        self.send_message(self.sender_name + "%")
        time.sleep(0.5)
        for i in self.dict_name_client_handler:
            self.dict_name_client_handler[i].send_message(
                self.sender_name + "*")  # sends to all the clients that connect the name of this client
            self.send_message(i + "*")  # sends to the client the names of the clients that connect
            time.sleep(0.5)

        self.dict_name_client_handler.update(
            {
                self.sender_name: self})  # update the name of the client and the this client handler that connect to the dictionary
        while True:
            msg = self.rcv_message()
            print(msg)
            list_split = msg.split("&")
            for key in self.dict_name_client_handler:
                if "&" in msg:  # (to private messages) - send the message to the two clients that in a private chat
                    if key == self.sender_name:
                        to_whom = list_split[0]
                    else:
                        to_whom = self.sender_name
                    if list_split[0] == key or list_split[1] == key:
                        self.dict_name_client_handler[key].send_message(
                            to_whom + "&" + list_split[1] + list_split[2])
                else:  # (broadcast message) - send to all the clients that connect except from the client that send
                    if key != self.sender_name:
                        self.dict_name_client_handler[key].send_message(
                            self.sender_name + ": " + msg)  # sending the msg to all clients that in the dictionary except from the client that write the msg
