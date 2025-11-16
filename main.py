import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket


SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 5000


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/message":
            data = self.rfile.read(int(self.headers['Content-Length']))
            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict = {key: value for key, value in 
                         (item.split("=") for item in data_parse.split("&"))}

            # Відправка даних socket-серверу
            self.send_to_socket(dict(data_dict))

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_html_file("error.html", 404)

    def send_to_socket(self, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(str(data).encode(), (SOCKET_HOST, SOCKET_PORT))
        except Exception as e:
            print("Socket error:", e)

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        requested = pr_url.path.lstrip("/")

        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        else:
            # статичні файли (css, png)
            if pathlib.Path(requested).exists():
                self.send_static(requested)
            else:
                self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as f:
            self.wfile.write(f.read())

    def send_static(self, filepath):
        self.send_response(200)
        mt = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
        self.send_header("Content-type", mt)
        self.end_headers()
        with open(filepath, "rb") as f:
            self.wfile.write(f.read())




server_address = ("", 3000)
http = HTTPServer(server_address, HttpHandler)
print("HTTP server started on port 3000")
try:
    http.serve_forever()
except KeyboardInterrupt:
    http.server_close()



