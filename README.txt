User guide to run the games
Copy all files to one directory, ether it is in your cloud VM machine or Desktop(PyCharm).

1. PyCharm Users
	1. Copy files into one folder on the Desktop.
	2. Open that folder in your PyCharm
	3. Right click on the Server.py and choose "Run 'Server'"
		a. On the console you should see "(Game Server) Waiting for clients to be connected..."
	4. Right click on the Client.py and choose "Run 'Client'" - On the console your should see 
		a. "Hello Player, please state your name: " - it proms player to entry a name.
		b. "please state your favorite color: " - it proms player to entry a color.
		c. Once all that been given to client, Game server will acknowledge that and will send a message back to player
			"Game Server: Hello John, the game will start once second player is joined the server, please wait..."
	5. Right click on the Client.py again and choose "Run 'Client'" again - It should show you second Client console where you will be proms to enter a Name and a Color.
	6. Once second player been joined to server, Server will run start_game function which will broad cast messages to clients:
		a. with greeting
		b. game board initialization.
	7. Server will ask (Player Name) to enter a number between (1-9)
	8. Once player entered a number, server receives it, updates the game board and broad cast the message to all players about updated game board.
	9. Server ask second player to enter a number.
	10. Until any of the players will reach 5 colors in the raw.

2. Cloud VM users.
	1. Copy files into any directory of your machine
	2. To run a server type: python Server.py
	3. To run a client open another console window and type: python Client.py
	4. To run a second client open second client console window and type: python Client.py
	

Unit tests and tests coverage been also done as a part of this challenge, 
	to make sure that the quality of the game is high enough before giving it to customers.
To run tests: you can right click on tests.py in PyCharm and click on "Run 'Unittests in test.py'"
	That should show you the output of total run tests
To run test from console you just type: python tests.py - it should show you what tests been run and their status.. ok.

In order to run test coverage. you should have coverage to be installed on your PyCharm or Vm
To execute coverage, you need first run the tests and the coverage report.
	1. coverage run tests.py
	2. coverage report
		
		Name                                                          Stmts   Miss  Cover
-----------------------------------------------------------------------------------------
Client.py                                                       		 43     18    58%
Player.py                                                       		  8      0   100%
Server.py                                                       		 87     44    49%
tests.py                                                         		 78      0   100%

----------------------------------------------------------
Decisions made
---------------------------------------------------------
I decided to use socket Client-Server implementation because it is faster way to implement given challenge and threads to make the server multi-threaded. 
There are many other ones, for example request-response implementation such as REST API using MVC design (django, Node.js) full stack, 
(it is right way, but would take more time).

----------------------------------------------------------
Improvement that I would make if I would have more time.--
----------------------------------------------------------
1. Complete requirement: when any of those players reach 5 colors in the raw, stop the game and broadcast the winner.
2. Make the code more cleaner, (make more generic functions that can be used in future improvements), make code more cleaner, focus on those functions:
	a. "Start_game" in Server.py
	b. "Listerner" in Server.py
	c. "Run" in Client.py
3. After completing step 2, it should be much easer to test those functions and make percentage of test coverage even more.
4. Fixing bugs - (Throwing right errors, focus on game reliability and fail safe - for customer satisfactions, 
													F.e. "when third player are joined it throws an error,
													but should make it a second session of the game, or hold him until current game complete.")
5. Make the loggers in colors so players can recognize their messages and movements. https://pypi.org/project/coloredlogs/ 
6. There are lots of ways to go with future improvements.(implementation DB, so you can store best results of the players, make the challanges for players, etc..)

