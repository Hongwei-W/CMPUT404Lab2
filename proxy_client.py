import socket

from echo_server import BUFFER_SIZE

def main():

    host = '192.168.31.26'
    port = 8001
    payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host , port))    
    s.sendall(payload.encode())
    s.shutdown(socket.SHUT_WR)

    data = s.recv(BUFFER_SIZE)
    print(data)
    
    s.close()

if __name__ == "__main__":
    main()