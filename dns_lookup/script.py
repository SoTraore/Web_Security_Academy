import socket
import threading
from dnslib.server import DNSServer, DNSHandler

# DNS proxy server settings
local_ip = "10.188.9.189"  # Your local IP address
local_dns_port = 53       # DNS port
upstream_dns = ("8.8.8.8", 53)  # Upstream DNS server (e.g., Google DNS)

# HTTP proxy server settings
local_http_ip = "0.0.0.0"  # Listen on all available network interfaces
local_http_port = 8080    # HTTP proxy port
target_server = ("34.246.129.62", 443)  # IP and port of the target server you want to intercept

class InterceptDNSHandler(DNSHandler):
    def resolve(self, request, handler):
        qname = request.q.qname

        # Log the DNS request
        print(f"Received DNS request for {qname}")

        # Forward the DNS request to the upstream DNS server
        response = request.send(upstream_dns)

        return response

def run_dns_server():
    dns_server = DNSServer(InterceptDNSHandler, port=local_dns_port, address=local_ip)
    dns_server.start()

def run_http_proxy():
    http_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_proxy.bind((local_http_ip, local_http_port))
    http_proxy.listen(1)

    while True:
        client_socket, client_address = http_proxy.accept()
        http_request = client_socket.recv(1024)

        # Log the HTTP request
        print(f"Received HTTP request:\n{http_request.decode('utf-8')}")

        # Forward the HTTP request to the target server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_socket:
            target_socket.connect(target_server)
            target_socket.send(http_request)

            # Receive the HTTP response from the target server
            http_response = target_socket.recv(4096)

            # Log the HTTP response
            print(f"Received HTTP response:\n{http_response.decode('utf-8')}")

            # Send the HTTP response back to the client
            client_socket.send(http_response)

if __name__ == "__main__":
    dns_thread = threading.Thread(target=run_dns_server)
    dns_thread.daemon = True
    dns_thread.start()

    http_thread = threading.Thread(target=run_http_proxy)
    http_thread.daemon = True
    http_thread.start()

    dns_thread.join()
    http_thread.join()
