# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:49:47 2019

@author: Andrey Lytvynov
"""
import logging
import socket
import threading
import numpy

logging.basicConfig(level=logging.INFO, format='(%(threadName)-10s) %(message)s',)


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def get_client_connected(self):
        """
        This function returns client connection into the server.
        """
        return self.sock.accept()

    @staticmethod
    def disconnects_client(client):
        client.close()

    @staticmethod
    def send_message(client, message):
        """
        This function sends an encoded message to client.
        """
        client.send(message.encode())

    @staticmethod
    def receive_message(client):
        """
        This function returns decoded message from client.
        """
        return client.recv(1024).decode("utf-8")

    def broadcast_message_to_all_players(self, message, clients):
        """
        This function broadcast message to all players
        """
        for sock in clients:
            self.send_message(sock, str(message))

    @staticmethod
    def build_dash_board():
        """
        This function returns built game dashboard.
        """
        return numpy.array([' '] * 54).reshape((6, 9))

    def update_board_game(self, client_decision, client, player_color, board_game):
        """
        This function update the dashboard with user entry.
        """
        li = ['x', 'o']
        try:
            for i in range(5, -1, -1):
                if any(color in board_game[i][client_decision-1] for color in li):  # 5 is user input
                    if i == 0:
                        self.send_message(client, "this column is full, please pick another column")
                        break
                    continue
                else:
                    board_game[i][client_decision-1] = player_color
                    break
        except IndexError:
            logging.error("Dashboard has 6x9 dimensional array, user entered wrong index.")

    @staticmethod
    def split_player_tuple_on_comma(player_attributes):
        player_name = player_attributes.split(',')[0]
        player_color = player_attributes.split(',')[1]
        return player_name, player_color

    def start_game(self, clients):
        """
        This function is a beginning of the game.
        """
        board_game = self.build_dash_board()
        self.broadcast_message_to_all_players(", hello players, Lets Begin!!!", clients)
        self.broadcast_message_to_all_players(", Game Dashboard has been built!!! \n" + str(board_game), clients)
        while True:
            for client, player_obj in clients.items():
                player_name, player_color = self.split_player_tuple_on_comma(player_obj)
                self.send_message(client, ', It is your turn ' + str(player_name) + ', please enter column (1-9):')
                client_decision = self.receive_message(client)
                if client_decision:
                    self.broadcast_message_to_all_players(str(player_name) + ' choose column [' + client_decision +
                                                          '], ' + 'broadcasting updated dashboard.', clients)
                    self.update_board_game(int(client_decision), client, player_color, board_game)
                    self.broadcast_message_to_all_players(str(board_game), clients)
                else:
                    logging.info('wrong input from player ' + str(player_name))
                    break

    def listen(self):
        clients = {}
        addresses = {}
        count = 0
        server_name = threading.main_thread().getName()
        logging.info('Waiting for clients to be connected...')
        while True:
            self.sock.listen(5)
            client, address = self.get_client_connected()
            addresses[client] = address  # thread to ping the address if it is still alive
            try:
                count += 1
                logging.info('New player been connected from ' + str(address))
                player = self.receive_message(client).split(',')
                player_name = player[0]
                logging.info("Player: " + str(player_name))
                clients[client] = player
                if len(clients) == 1:
                    self.send_message(client, str(server_name) + ': Hello ' + str(player_name) +
                                      ', the game will start once second player is joined the server, please wait...')
                    clients[client] = player[0] + "," + str('x')
                else:
                    self.send_message(client, str(server_name) + ': Hello ' + str(player_name) +
                                      ', other player is waiting for you, lets start a game')
                    clients[client] = player[0] + "," + str('o')
                    self.start_game(clients)
            except ConnectionError:
                logging.error("Connection with client been lost.")
                self.disconnects_client(client)


if __name__ == '__main__':
    threading.current_thread().name = 'Game Server'
    ThreadedServer('127.0.0.1', 8081).listen()
