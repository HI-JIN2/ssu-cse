"""
3. (4 points) Write a Python script to create a TCP Server and Client 
using the python socket standard library to develop a game "Guess the number.".

The game will follow as:
1. The server will choose a random number between 1 to 10.
2. Inform the client and ask to guess a number between 1 to 10.
3. The client will send a guessed number as a request to the server.

Conditions:
1. The client will request to start the game by sending the first request as "start."
2. The client will have only 5 attempts to guess the correct number
3. The client will only win if he guesses the correct number within 5 attempts and loses the game.
The exchange of messages between the server and client during the game will follow the following conditions and message text based on the difference 
between the actual number with the server and guessed number by the client:
x = randomly chosen number by server 
guess = number guessed by a client

Conditions and messages:
(x = guess) -> "Congratulations you did it." 
(x > guess) -> "You guessed too small!"
(x < guess) -> "You Guessed too high!" 
"""



import argparse, random, socket


# Define a function for the server role
def server(port):
    MAX_CLIENTS = 1 # Maximum number of clients to accept

    # Create a TCP/IP socket for IPv4
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    sock.bind(("127.0.0.1", port))

    # Listen for incoming connections
    sock.listen(MAX_CLIENTS)

    # Print a message to indicate the server is running
    print("Server is running on {}:{}".format("127.0.0.1", port))

    # Loop to accept incoming connections and play the game
    while True:
        conn, addr = sock.accept() # Accept a new connection
        print("Connected by", addr)

        # Generate a random number between 1 to 10
        random_number = random.randint(1, 10)

        # Send the instruction to start the game to the client
        conn.send("Welcome to the Guess the number game! You have 5 attempts to guess a number between 1 to 10. Please enter 'start' to begin.\n".encode())

        attempts = 0
        # Loop to handle the game logic
        while attempts < 5:
            # Receive data from the client
            data = conn.recv(1024).decode().strip()
            if not data: # If no data is received, break out of the loop
                break
            if data.lower() == "start":
                # If the client sends the "start" command, send the prompt to guess a number
                conn.send("Game has started! Please guess a number between 1 to 10: ".encode())
                attempts += 1
            elif data.isdigit() and int(data) >= 1 and int(data) <= 10:
                # If the client sends a valid number, check if it matches the random number
                guess = int(data)
                if guess == random_number:
                    # If the guess is correct, send a congratulatory message and break out of the loop
                    conn.send("Congratulations you did it.".encode())
                    break
                elif guess < random_number:
                    # If the guess is too small, send a message indicating that and increment the attempts counter
                    conn.send("You guessed too small!".encode())
                    attempts += 1
                    if attempts == 5:
                        # If the client has used up all attempts, send a message indicating that and the correct number
                        conn.send("Game over. You lost. The number was {}.".format(random_number).encode())
                else:
                    # If the guess is too large, send a message indicating that and increment the attempts counter
                    conn.send("You Guessed too high!".encode())
                    attempts += 1
                    if attempts == 5:
                        # If the client has used up all attempts, send a message indicating that and the correct number
                        conn.send("Game over. You lost. The number was {}.".format(random_number).encode())
            else:
                # If the client sends an invalid input, send a message to prompt for a valid number
                conn.send("Invalid input. Please enter a number between 1 to 10.".encode())

        conn.close() # Close the connection


# Define a function for the client role
def client(port):
    # Create a TCP/IP socket for IPv4
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    sock.connect(("127.0.0.1", port))

    # Receive the initial instruction from the server
    data = sock.recv(1024).decode()
    print(data, end="")
    
    response = input() # Get input from the user


    if response.lower() == "start":
        # Send the input to the server
        sock.send(response.encode())
        
        # Receive the next instruction from the server
        data = sock.recv(1024).decode()
        print(data, end="")
        attempts = 1 # Initialize attempts to 1
        while attempts <= 5: 
            response = input() # Get input from the user
            sock.send(response.encode())
            data = sock.recv(1024).decode()
            print(data, end="")
            
            # If the response from the server contains "Congratulations", break the loop
            if "Congratulations" in data:
                break
            # If the response from the server contains "Game over", break the loop
            elif "Game over" in data:
                break
            else:
                attempts += 1

        # Close the socket
        sock.close()
    else:
        print("Invalid input. Exiting...")


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='"Guess the number" game over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                                     ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)