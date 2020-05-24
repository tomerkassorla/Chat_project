__author__ = 'User'
import socket
import clientHandler
from database import *


class Server(object):
    """In the server class there are listen and accept functions which create the connection with the client"""

    def __init__(self):
        self.sock = socket.socket()
        self.port = 8077

    def s_listen(self):
        """listen"""
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(10)

    def accept(self):
        """accept"""
        return self.sock.accept()


def main():
    """server main handle the connection with the client, create database
     and start a client handler thread when client is accept"""
    server = Server()  # create server object
    server.s_listen()
    database = Database("data")
    database.create_connection()  # create connection with the database
    msg = """CREATE TABLE IF NOT EXISTS users (name text,password text)"""
    database.create_table(msg)  # create table if not exists
    dict_name_client_handler = {}  # dictionary with key-name and value-client_handler
    while True:
        client_socket, address = server.accept()  # accept the client that connect
        client_hand = clientHandler.ClientHandler(address, client_socket, database, dict_name_client_handler)
        client_hand.start()  # starts the thread


if __name__ == "__main__":
    main()
