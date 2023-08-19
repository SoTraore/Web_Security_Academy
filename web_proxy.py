import http.server
import socketserver
import requests

# Replace with your public server URL
public_server_url = "185.15.172.212:3128"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            # Forward the GET request to the public server
            response = requests.get(public_server_url + self.path)
            self.send_response(response.status_code)
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.content)
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == "__main__":
    PORT = 7770  # Change this to the desired port
    Handler = ProxyHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)

    print("Proxy server is running on port", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Proxy server stopped.")
        httpd.server_close()
