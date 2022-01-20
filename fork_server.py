#Note, code is taken from echo_server, then modified based on that 

#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process
from proxy_server import get_remote_ip

#define address & buffer size
HOST = "192.168.31.26"
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        proxy_connection_host = 'www.google.com'
        proxy_connection_port = 80
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            #p = Process(target=echo_server, args=(conn,))
            p = Process(target=proxy_server, args=(conn, proxy_connection_host, proxy_connection_port))
            p.daemon = True
            p.start()
            

def echo_server(conn):
    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    #conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def proxy_server(conn, proxy_connection_host, proxy_connection_port):
    proxy_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_ip = get_remote_ip(proxy_connection_host)
    proxy_connection.connect((remote_ip, proxy_connection_port))

    proxy_connection.sendall(conn.recv(BUFFER_SIZE))
    proxy_connection.shutdown(socket.SHUT_WR)
    data = proxy_connection.recv(BUFFER_SIZE)

    conn.send(data)
    #conn.shutdown(socket.SHUT_RDWR)
    conn.close()

if __name__ == "__main__":
    main()
