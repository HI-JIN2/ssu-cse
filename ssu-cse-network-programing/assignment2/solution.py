"""
과제2-1

1. tls/ssl
2. 서버는 여러 클라이언트 동시에 처리 멀티플. 비동기 처리
3. 로깅<- 연결, 연결 끊김, 오류
4. 적절한 종료 처리
5. compression 압축 메커니즘. zlib
6. 네트워크 오류 처리 (연결, 소켓, 시간 초과, 유효하지 않은 클라이언트 요청 )
"""

# 클라이언트 :1. 쿼리스트링 {‘task’: ‘ping’, ‘domain’: ‘google.com’}
# 2. 압축. 
# 3. 암호화, 그리고 그것을 서버한테 전송하기

# 서버 : 
# 1. 복호화. 받은 암호화된 데이터
# 2 .복호화된 데이터를 압축 해제
# 3. 제이슨 형식으로 읽기, 일 요청, 클라로 부터 리턴 응답받기. 제이슨으로

import argparse, socket, ssl, logging, zlib, json

def client(host, port, cafile=None):
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    print('Connected to host {!r} and port {}'.format(host, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    
    query = json.dumps({'task': 'ping', 'domain': 'google.com'} )
    #{'task': 'ping', 'domain': 'google.com'} #쿼리


    #쿼리 압축 
    compressed_query=zlib.compress(query)

    #쿼리 암호화 어캐하지??



    #전송
    raw_sock.sendto(compressed_query.encode(), (host, port))



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
    print('Listening at interface {!r} and port {}'.format(host, port))
    raw_sock, address = listener.accept()
    print('Connection from host {!r} and port {}'.format(*address))
    ssl_sock = context.wrap_socket(raw_sock, server_side=True)

    
    while True:
        recv_query, addr = ssl_sock.recvfrom(1024)  # receive the message from the client
        print("received message:", recv_query.decode())
        zlib.decompress(recv_query)

        json.loads(recv_query)
        
        #encrypted_data = encrypt_message(data.decode())  # encrypt the message using the custom algorithm
        #ssl_sock.sendto(encrypted_data.encode(), addr)  # send the encrypted message back to the client
        ssl_sock.close


    

    #받야야함
    #받고 압축 해제, 복호화


    ssl_sock.sendall('Simple is better than complex.'.encode('ascii'))
    ssl_sock.close()

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