# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:51:13 2019

@author: Andrey Lytvynov
"""

import socket
import logging
import threading
import Player

logging.basicConfig(level=logging.INFO, format='%(message)s',)


class Client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        """
        This function connects the client to a running server.
        """
        self.sock.connect((self.host, self.port))

    def disconnect_from_server(self):
        """
        This function disconnects the client from running server.
        """
        self.sock.close()

    def send_message(self, message):
        """
        This function sends the message.
        """
        self.sock.send(message.encode())

    def read_server_messages(self):
        """
        This  function is used for continues listenning the incomming messages from server (runs with thread).
        """
        while True:
            logging.info(self.sock.recv(1024).decode())

    def receive_message(self):
        """
        This function receives incomming messages.
        """
        return self.sock.recv(1024).decode()

    def run(self):
        """
        This function runs the proms for client and sends the client decision to the server during the game.
        """
        message_listener = threading.Thread(target=self.read_server_messages)
        message_listener.setDaemon(True)
        message_listener.start()
        message = ""
        self.send_message(player.get_name() + "," + player.get_color())
        try:
            while message.lower().strip() != 'bye':
                message = input("")
                if message.isdigit() and int(message) <= 8 or int(message) >= 1:
                    self.send_message(message)
                else:
                    logging.info("Wrong entry, please specify only digits from 1 to 9")
        except ValueError:
            logging.error("Invalid literal [" + str(message) + "], please try again.")
        self.disconnect_from_server()


if __name__ == '__main__':
    player_name = input("Hello Player, please state your name: ")
    player_color = input("Please state your favorite color: ")
    player = Player.Player(player_name, player_color)
    Client('127.0.0.1', 8081).run()
