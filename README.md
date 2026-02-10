# Guess the Number – TCP Client-Server Game

A simple TCP client-server guessing game implemented in Python.
The server generates a random number between **0 and 500**, and the client
tries to guess it based on feedback received from the server.

Each execution represents a full **game session** that can contain multiple
rounds. At the end of the session, the **best score** (minimum number of guesses
needed to find the number) is displayed.
