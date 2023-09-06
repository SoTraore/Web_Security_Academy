# http_server.py
import socket

local_http_ip = "0.0.0.0"  # Listen on all available network interfaces
local_http_port = 8080       # HTTP port

def run_http_server():
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.bind((local_http_ip, local_http_port))
    http_server.listen(1)

    while True:
        client_socket, client_address = http_server.accept()
        http_request = client_socket.recv(1024)

        # Log the HTTP request
        print(f"Received HTTP request:\n{http_request.decode('utf-8')}")

        # You can implement custom logic here to capture and possibly modify HTTP requests

        # Send a simple HTTP response
        http_response = b"HTTP/1.1 200 OK\r\n\r\nHello, World!"
        client_socket.send(http_response)
        client_socket.close()

if __name__ == "__main__":
    run_http_server()
