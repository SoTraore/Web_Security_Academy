# dns_server.py
from dnslib.server import DNSServer, DNSHandler

local_ip = "10.188.9.189"  # Your local IP address
local_dns_port = 53       # DNS port
upstream_dns = ("8.8.8.8", 53)  # Upstream DNS server (e.g., Google DNS)

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

if __name__ == "__main__":
    run_dns_server()
