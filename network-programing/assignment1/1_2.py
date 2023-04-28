"""
2. (3 points) Write a python script to create a UDP Server and Client using the python socket standard library 
where the client sends a message to the server and the server replies to the message. 
However, there's a twist: the reply from the server must be encrypted using a custom encryption algorithm that you've developed.

Algorithm:
The encryption algorithm works as follows: 
each character in the message is replaced with the ASCII code for the next character in the English alphabet. 
For example, 'a' is replaced with 'b', 'b' is replaced with 'c', and so on. 
The last character in the alphabet, 'z', is replaced with 'a'. 
The resulting encrypted message is then sent over the UDP connection.
"""



import argparse, socket

# Define a custom encryption algorithm
def encrypt_message(message):
    encrypted_message = ""
    for char in message:
        if char == 'z':  # if the character is 'z', replace it with 'a'
            encrypted_message += 'a'
        else:  # otherwise, replace it with the next character in the alphabet
            encrypted_message += chr(ord(char) + 1)
    return encrypted_message

# Define the server function
def server(port):
    # Create a socket object using IPv4 and UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the IP address and port number
    sock.bind(("127.0.0.1", port))

    # Loop indefinitely, waiting for messages from the client
    while True:
        data, addr = sock.recvfrom(1024)  # receive the message from the client
        print("received message:", data.decode())
        encrypted_data = encrypt_message(data.decode())  # encrypt the message using the custom algorithm
        sock.sendto(encrypted_data.encode(), addr)  # send the encrypted message back to the client
        sock.close

# Define the client function
def client(port):
    # Get the message to send from the user and encrypt it using the custom algorithm
    message = input("Enter message to send to server: ")

    # Create a socket object using IPv4 and UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the encrypted message to the server
    sock.sendto(message.encode(), ("127.0.0.1", port))

    # Wait for the server to send back an encrypted message
    data, addr = sock.recvfrom(1024)
    print("received encrypted message:", data.decode())

# Parse the command-line arguments
if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at; host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()

    # Call the appropriate function based on the user's choice
    function = choices[args.role]
    function(args.p)