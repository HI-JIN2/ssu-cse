"""
과제2-1

1. tls/ssl
2. 서버는 여러 클라이언트 동시에 처리 멀티플. 비동기 처리
3. 로깅<- 연결, 연결 끊김, 오류
4. 적절한 종료 처리
5. compression 압축 메커니즘. zlib
6. 네트워크 오류 처리 (연결, 소켓, 시간 초과, 유효하지 않은 클라이언트 요청 )
"""

# 클라이언트 :
# 1. 쿼리스트링 {‘task’: ‘ping’, ‘domain’: ‘google.com’}
# 2. 압축. 
# 3. 암호화, 그리고 그것을 서버한테 전송하기

# 서버 : 
# 1. 복호화. 받은 암호화된 데이터
# 2 .복호화된 데이터를 압축 해제
# 3. 제이슨 형식으로 읽기, 일 요청, 클라로 부터 리턴 응답받기. 제이슨으로

import argparse, socket, ssl, logging, zlib, json, threading


def handle_client(client_sock):
    try:
        while True:
            # receive the message from client
            recv_query = client_sock.recv(1024) 
            if not recv_query:
                break
            print("received message:", recv_query.decode())

            # decompress
            compressed_data=zlib.decompress(recv_query)
            
            # read to json
            json_data=json.loads(compressed_data)

    except Exception as e:
        logging.error('Error in handling client: %s', e)
    finally:
        logging.info('Closing connection with client')
        client_sock.close()

def client(host, port, cafile=None):
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    logging.info('Connected to host {!r} and port {}'.format(host, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    
    #make query
    query = {'task': 'ping', 'domain': 'google.com'} 
    
    #query to json
    json_query = json.dumps(query)
    
    #compressed
    compressed_query=zlib.compress(json_query.encode('utf-8'))

    #send to server
    raw_sock.sendall(compressed_query, (host, port))


    while True:
        data = ssl_sock.recv(1024)
        if not data: #EOF 
            logging.warning('end of file!')  # will print a message to the console
            break
        print(repr(data))
    

def server(host, port, certfile, cafile=None):
    purpose = ssl.Purpose.CLIENT_AUTH 
    context = ssl.create_default_context(purpose, cafile=cafile)
    context.load_cert_chain(certfile)

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host, port))
    listener.listen(1) 
    logging.info('Listening at interface {!r} and port {}'.format(host, port))


    try:
        while True:
            client_sock, address = listener.accept()
            logging.info('Accepted connection from %s:%s', *address)
            ssl_sock = context.wrap_socket(client_sock, server_side=True)

            # spawn a new thread to handle the client
            t = threading.Thread(target=handle_client, args=(ssl_sock,))
            t.start()
    except KeyboardInterrupt:
        logging.warning('Server interrupted by user')
    finally:
        logging.info('Closing server socket')
        listener.close()

    while True:
        # accept a new client connection
        raw_sock, address = listener.accept()
        print('Connection from host {!r} and port {}'.format(*address))
        ssl_sock = context.wrap_socket(raw_sock, server_side=True)

        # handle the client request in a new thread
        threading.Thread(target=handle_client, args=(ssl_sock,)).start()
    

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