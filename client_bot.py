#!/usr/bin/python3

from argparse import ArgumentParser
import os
import socket
import time

def main():
    # Parse arguments
    arg_parser = ArgumentParser(description='Client Bot', add_help=False)
    arg_parser.add_argument('-p', '--port', dest='port', action='store',
            type=int, default=80, help='Port to connect on')
    arg_parser.add_argument('-h', '--hostname', dest='hostname', action='store',
            default='picard.cs.colgate.edu', help='Port to connect on')
    settings = arg_parser.parse_args()

    input("Press Enter to run client_bot...")
    print('Client Bot PID: %d' % os.getpid())
    
    # Connect to server
    with socket.socket() as client_sock:
        print("Connecting to %s:%d..." % (settings.hostname, settings.port))
        client_sock.connect(('', settings.port))
        for uri in ["/agent.php", "/time.php"]:
            send_request(client_sock, uri, settings.hostname)
            recv_response(client_sock)

    input("Press Enter to exit...")

def recv_response(sock):
    # Receive response
    response = sock.recv(4096).decode()
    lines = response.split('\r\n')

    print(lines[-1], end='')

def send_request(sock, uri, host):
    # Construct request parts
    first = "GET %s" % uri
    host = "Host: %s" % host
    agent = "UserAgent client_bot/2022.02"
    accept = "Accept: */*"
        
    # Construct full request
    request = "\n".join([first, host, agent, accept])

    # Send response
    sock.send(request.encode())

if __name__ == '__main__':
    main()
