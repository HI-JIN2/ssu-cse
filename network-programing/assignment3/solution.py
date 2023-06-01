import socket
import ssl
import json
import zlib
import logging
import argparse
import threading
import random
import time
import zmq
import socket, ssl, json, zlib, logging, argparse, threading


class NewsGenerator:
    def __init__(self):
        # Initialize the news generator.
        self.topics = ["business", "entertainment", "health", "science", "sports", "technology"]
        self.events = ["new product launch", "merger", "acquisition", "lawsuit", "scandal", "government regulation"]
        self.companies = ["Apple", "Microsoft", "Google", "Amazon", "Facebook", "Tesla"]
    
    def get_news(self):
        # Generate a random news headline.
        topic = random.choice(self.topics)
        event = random.choice(self.events)
        company = random.choice(self.companies)
        headline = topic + " " + company + " " + event
        return headline
    
class StockTicker: # task 4
    def __init__(self):
        self.companies = ["AAPL", "MSFT", "GOOGL"] 
        self.prices = {}
        for company in self.companies:
            self.prices[company] = random.randint(100, 1000)

    def generate_stock_price(self, company):
        if company not in self.companies:
            raise ValueError("Invalid company")

        # Generate a random stock price for the company 
        price = random.randint(100, 1000)
        self.prices[company] = price 
        
        return price

class Chatroom: #task 5
    
    def __init__(self):
        self.clients = []

    def join(self, client):
        self.clients.append(client) 

    def leave(self, client):
        self.clients.remove(client) 

    def send(self, sender, message):
        for client in self.clients: 
            if client != sender:
                client.send((sender, message))



def toggle_string(S):
    s = ""
    # Write your code between start and end for solution of problem 2
    # Start
    # dictionary to match lowercase to uppercase
    lower2Upper = {"a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G",
                   "h": "H", "i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N",
                   "o": "O", "p": "P", "q": "Q", "r": "R", "s": "S", "t": "T", "u": "U",
                   "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z"}
    # dictionary to match uppercase to lowercase
    upper2Lower = {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g",
                   "H": "h", "I": "i", "J": "j", "K": "k", "L": "l", "M": "m", "N": "n",
                   "O": "o", "P": "p", "Q": "q", "R": "r", "S": "s", "T": "t", "U": "u",
                   "V": "v", "W": "w", "X": "x", "Y": "y", "Z": "z"}
    for c in S:
        if 'a' <= c <= 'z':  # lower case -> upper case
            s += lower2Upper[c]
        elif 'A' <= c <= 'Z':  # upper case -> lower case
            s += upper2Lower[c]
        else:
            s += c

    return s


def client(host, port, cafile=None):
    """
    The client function that connects to the server and sends queries securely.
    """
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    print('Connected to host {!r} and port {}'.format(host, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    logging.info(f'Connected to {host}:{port} securely')
    
    has_printed = False

    while True:
        task = input("Enter task name (ping, toggle_string, news, stock_ticker): ")
        if task == 'toggle_string':
            string = input("Enter a string to toggle: ")
            query = {'task': 'toggle_string', 'string': string}
            query_json = json.dumps(query).encode('utf-8')
            compressed = zlib.compress(query_json)
            ssl_sock.sendall(compressed)

            response = ssl_sock.recv(1024)
            decompressed = zlib.decompress(response)
            response_json = json.loads(decompressed.decode('utf-8'))


            if not has_printed:
                toggle_result = response_json["result"]
                print("result:", toggle_result)
                has_printed = True
                ssl_sock.close()
                break

            if not response:
                break

        elif task =='ping':
            query = {'task': 'ping', 'domain': 'google.com'}
            query_json = json.dumps(query).encode('utf-8')
            compressed = zlib.compress(query_json)
            ssl_sock.sendall(compressed)

            response = ssl_sock.recv(1024)
            decompressed = zlib.decompress(response)
            response_json = json.loads(decompressed.decode('utf-8'))


            if not has_printed:
                ip_address = response_json["ip"]
                print("ip address:", ip_address)
                has_printed = True
                ssl_sock.close()
                break

            if not response:
                break
            logging.info(f'Response from {host}:{port}: {response}')


        elif task == 'news':
            topic = input("Enter a string to topic(business, entertainment, health, science, sports, technology): ")
            query = {'task': 'news', 'topic': topic}
            query_json = json.dumps(query).encode('utf-8')
            compressed = zlib.compress(query_json)
            ssl_sock.sendall(compressed)

            response = ssl_sock.recv(1024)
            decompressed = zlib.decompress(response)
            response_json = json.loads(decompressed.decode('utf-8'))


            if not has_printed:
                headline = response_json["headline"]
                print("headline:", headline)
                has_printed = True
                ssl_sock.close()
                break

            if not response:
                break
            logging.info(f'Response from {host}:{port}: {response}')
        
        
        elif task == 'stock_ticker':
            company = input("Enter a string to company(AAPL, MSFT, GOOGL): ")
            query = {'task': 'stock_ticker', 'company': company}
            query_json = json.dumps(query).encode('utf-8')
            compressed = zlib.compress(query_json)
            ssl_sock.sendall(compressed)

            response = ssl_sock.recv(1024)
            decompressed = zlib.decompress(response)
            response_json = json.loads(decompressed.decode('utf-8'))


            if not has_printed:
                prices = response_json["prices"]
                print("prices:", prices)
                has_printed = True
                ssl_sock.close()
                break

            if not response:
                break
            logging.info(f'Response from {host}:{port}: {response}')
        else :
            print("wrong task!! try again~")


    logging.info(f'Disconnected from {host}:{port}')


def handle_client(conn, addr):
    """
    A function that handles the client's request on the server.
    """
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='ssu.pem')
    ssock = context.wrap_socket(conn, server_side=True)
    logging.info(f'Connected to {addr[0]}:{addr[1]} securely')
    while True:
        data = ssock.recv(1024)

        if not data:
            break
        decompressed = zlib.decompress(data)
        query = json.loads(decompressed.decode('utf-8'))

        if query['task'] == 'ping':
            # Perform the task here
            domain = query['domain']
            ip_address = socket.gethostbyname(domain)
            ip_query =  {'domain': query['domain'], 'ip': ip_address}
            ip_address_json = json.dumps(ip_query).encode('utf-8')
            compressed = zlib.compress(ip_address_json)
            ssock.sendall(compressed)
        
        elif query['task'] == 'toggle_string':
            # Perform the 'toggle_string' task here
            string = query['string']
            toggled = toggle_string(string)
            result_query = {'task': 'toggle_string', 'result': toggled}
            result_json = json.dumps(result_query).encode('utf-8')
            compressed = zlib.compress(result_json)
            ssock.sendall(compressed)
        
        elif query['task'] == 'news':
            # Perform the 'toggle_string' task here
            topic = query['topic']
            ng=NewsGenerator()
            duration = 60  # 1 minute (in seconds)
            end_time = time.time() + duration

            while time.time() < end_time:
                time.sleep(1)  # Publish news every 1 second
                    
                headline = ng.get_news(topic)
                print(headline)
                
                if topic == headline.split(" ")[0]:
                    result_query = {'task': 'news', 'headline': headline}
                    result_json = json.dumps(result_query).encode('utf-8')
                    compressed = zlib.compress(result_json)
                    ssock.sendall(compressed)

        elif query['task'] == 'stock_ticker':
            # Perform the 'toggle_string' task here
            company = query['company']
            sp =StockTicker()
            duration = 60  # 1 minute (in seconds)
            end_time = time.time() + duration

            while time.time() < end_time:
                time.sleep(1)  # Publish news every 1 second
                    
                prices = sp.generate_stock_price(company)
                print(prices)
                
                result_query = {'task': 'news', 'prices': prices}
                result_json = json.dumps(result_query).encode('utf-8')
                compressed = zlib.compress(result_json)
                ssock.sendall(compressed)

        else: 
            print("wrong task!!")

    logging.info(f'Disconnected from {addr[0]}:{addr[1]}')
    ssock.close()



def server(host, port, certfile, cafile=None):
    purpose = ssl.Purpose.CLIENT_AUTH

    """
    The server function that listens to incoming client connections.
    """
    context = ssl.create_default_context(purpose.CLIENT_AUTH)
    #context.load_verify_locations(cafile='ca.pem')
    context.load_cert_chain(certfile)


    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host, port))
    listener.listen(1)
    logging.info(f'Server listening on {host}:{port}')
    while True:
        conn, addr = listener.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Safe TLS client and server')
    parser.add_argument('host', help='hostname or IP address')
    parser.add_argument('port', type=int, help='TCP port number')
    parser.add_argument('-a', metavar='cafile', default=None,
                        help='authority: path to CA certificate PEM file')
    parser.add_argument('-s', metavar='certfile', default=None,
                        help='run as server: path to server PEM file')
    args = parser.parse_args()
    if args.s:
        server(args.host, args.port, args.s, args.a)
    else:
        client(args.host, args.port, args.a)