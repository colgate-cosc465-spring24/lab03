#!/usr/bin/python3

from argparse import ArgumentParser
import os
import socket
import time

def main():
    # Parse arguments
    arg_parser = ArgumentParser(description='Server Bot', add_help=False)
    arg_parser.add_argument('-p', '--port', dest='port', action='store',
            type=int, required=True, help='''Port to listen on''')
    settings = arg_parser.parse_args()

    input("Press Enter to run server_bot...")
    print('Server Bot PID: %d' % os.getpid())
    
    # Listen for clients
    with socket.socket() as server_sock:
        server_sock.listen(settings.port)
        print("Listening on port %d..." % (settings.port))

        while True:
            # Handle client
            client_sock, client_addr = server_sock.accept()
            request = recv_request(server_sock)
            print("Received request from %s:%d for %s" %
                    (client_addr[0], client_addr[1], request["URI"]))
            send_response(server_sock, request)
            client_sock.close()

def recv_request(sock):
    # Receive request
    request = sock.recv(4096).decode()
    lines = request.split('\r\n')

    # Extract URI
    uri = lines[0].split(' ')[1]
    fields = { "URI" : uri }

    # Extract headers
    for header_line in lines[1:-2]:
        parts = header_line.split(': ')
        fields[parts[0]] = parts[1]

    return fields

def send_response(sock, request):
    status, body = get_body(request)

    # Construct response parts
    agent = "User-Agent: server_bot"
    length = "Content-Length: %d" % len(status)
    close = "Connection: close"
        
    # Construct full response
    response = "\n".join([status, agent, length, close, body])

    # Send response
    sock.send(response.encode())

def get_body(request):
    status = "200 OK"
    if (request["URI"] == "/time.php"):
        return status, "The time is " + time.strftime('%I:%M:%S %p') + "\n"
    elif (request["URI"] == "/agent.php"):
        if "User-Agent" not in request:
            return status, "Unknown agent\n"
        return status, "Greetings " + request["User-Agent"] + "\n"
    return "404 Not found", ""

if __name__ == '__main__':
    main()
