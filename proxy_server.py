import socket

from echo_server import BUFFER_SIZE

def main():
    listen_ipaddr = "192.168.31.26"
    listen_port = 8001

    proxy_connection_host = 'www.google.com'
    proxy_connection_port = 80

    incoming = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    incoming.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    incoming.bind((listen_ipaddr, listen_port))
    incoming.listen(1)

    while 1:
        # accept the incoming connections
        conn, addr = incoming.accept()

        # start to connect to goolge 
        # Note that the get remote ip is from the code provided
        proxy_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = get_remote_ip(proxy_connection_host)
        proxy_connection.connect((remote_ip, proxy_connection_port))

        proxy_connection.sendall(conn.recv(BUFFER_SIZE))
        proxy_connection.shutdown(socket.SHUT_WR)
        data = proxy_connection.recv(BUFFER_SIZE)

        conn.send(data)
        conn.close()

def get_remote_ip(proxy_connection_host):
    print(f'Getting IP for {proxy_connection_host}')
    try:
        remote_ip = socket.gethostbyname( proxy_connection_host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {proxy_connection_host} is {remote_ip}')
    return remote_ip

if __name__ == "__main__":
    main()