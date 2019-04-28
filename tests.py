# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:51:13 2019

@author: Andrey Lytvynov
"""
import logging
import threading
import Client
import Player
import Server
import unittest
import numpy

logging.basicConfig(level=logging.INFO, format='(%(threadName)-10s) %(message)s',)
clients = {}


class TestStringMethods(unittest.TestCase):
    player_obj = Player.Player("John", "Red")
    threaded_server_obj = Server.ThreadedServer('127.0.0.1', 8080)
    threaded_server_obj.sock.listen(5)

    def test_update_game_dashboard(self):
        Client.Client('127.0.0.1', 8080)
        client, address = self.threaded_server_obj.get_client_connected()
        game_dashboard = self.threaded_server_obj.build_dash_board()
        self.threaded_server_obj.update_board_game(1, client, "x", game_dashboard)
        self.threaded_server_obj.update_board_game(1, client, "x", game_dashboard)
        self.threaded_server_obj.update_board_game(1, client, "x", game_dashboard)
        self.threaded_server_obj.update_board_game(1, client, "x", game_dashboard)
        self.threaded_server_obj.update_board_game(1, client, "x", game_dashboard)

    def test_update_game_dashboard_throw_error(self):
        Client.Client('127.0.0.1', 8080)
        client, address = self.threaded_server_obj.get_client_connected()
        game_dashboard = self.threaded_server_obj.build_dash_board()
        self.assertRaises(IndexError, self.threaded_server_obj.update_board_game(11, client, "x", game_dashboard))

    def test_build_game_dashboard(self):
        self.assertEqual(6, (len(self.threaded_server_obj.build_dash_board())))

    def test_server_sends_message_to_client(self):
        game_client = Client.Client('127.0.0.1', 8080)
        client, address = self.threaded_server_obj.get_client_connected()
        self.threaded_server_obj.send_message(client, "test message")
        self.assertEqual(game_client.receive_message(), "test message")

    def test_server_receive_message_from_client(self):
        game_client = Client.Client('127.0.0.1', 8080)
        client, address = self.threaded_server_obj.get_client_connected()
        game_client.send_message("test message")
        self.assertEqual(self.threaded_server_obj.receive_message(client), "test message")

    def test_client_connect_to_server_and_server_disconnects_client(self):
        Client.Client('127.0.0.1', 8080)
        client, address = self.threaded_server_obj.get_client_connected()
        self.assertEqual(address[0], '127.0.0.1')
        self.threaded_server_obj.disconnects_client(client)

    def test_client_connects_to_server_and_disconnects(self):
        game_client = Client.Client('127.0.0.1', 8080)
        client, address = self.threaded_server_obj.get_client_connected()
        self.assertEqual(address[0], '127.0.0.1')
        game_client.disconnect_from_server()

    def test_threaded_message_listener(self):
        game_client = Client.Client('127.0.0.1', 8080)
        client, address = self.threaded_server_obj.get_client_connected()
        threaded_message = threading.Thread(target=game_client.read_server_messages)
        threaded_message.setDaemon(True)
        threaded_message.start()
        self.threaded_server_obj.send_message(client, "test")

    def test_server_broadcast_message_to_all_players(self):
        game_client_one = Client.Client('127.0.0.1', 8080)
        game_client_two = Client.Client('127.0.0.1', 8080)
        client_one, address_one = self.threaded_server_obj.get_client_connected()
        client_two, address_two = self.threaded_server_obj.get_client_connected()
        clients[client_one] = address_one
        clients[client_two] = address_two
        self.threaded_server_obj.broadcast_message_to_all_players("test message", clients)
        self.assertEqual(game_client_one.receive_message(), "test message")
        self.assertEqual(game_client_two.receive_message(), "test message")

    def test_split_player_attributes_on_comma(self):
        player_name, player_color = self.threaded_server_obj.split_player_tuple_on_comma("John,x")
        self.assertEqual("John", player_name)
        self.assertEqual("x", player_color)

    def test_get_player_name(self):
        self.assertEqual("John", (self.player_obj.get_name()))

    def test_get_player_color(self):
        self.assertEqual("Red", (self.player_obj.get_color()))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
