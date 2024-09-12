from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def run_server():
    local_ip = get_local_ip()
    server_address = (local_ip, 4443)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('localhost.pem', 'localhost-key.pem')

    # Wrap the socket
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Server running on https://localhost:4443")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
