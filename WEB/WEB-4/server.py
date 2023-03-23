import socket
import pathlib
import urllib.parse
import mimetypes
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

base_dir = pathlib.Path()
buffer_size = 1024


class App(BaseHTTPRequestHandler):
    def do_GET(self):
        print(urllib.parse.urlparse(self.path))
        route = urllib.parse.urlparse(self.path)

        match route.path:
            case "/":
                self.send_html("index.html")
            case "/message.html":
                self.send_html("message.html")
            case _:
                file = base_dir.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html("error.html", 404)

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mt = mimetypes.guess_type(filename)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def do_POST(self):
        lenght = self.headers.get("Content-Length")
        data = self.rfile.read(int(lenght))
        self.save_data(data)
        self.send_response(302)
        self.send_header("Location", "message.html")
        self.end_headers()
        self.send_html("message.html")


def save_data(data):
    parse_data = urllib.parse.unquote_plus(data.decode())
    dict_parse = [el for el in parse_data.split("&")]
    print(dict_parse)


def run_socket_servet(host, port):
    server_soket = socket.socket()
    server_soket.bind((host, port))
    server_soket.listen()

    try:
        while True:
            msg, adress = server_soket.recvfrom(buffer_size)
            save_data(msg)
    except KeyboardInterrupt:

    server_soket.close()


def run():
    address = ("localhost", 3000)
    httpd = HTTPServer(address, App)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    run()
