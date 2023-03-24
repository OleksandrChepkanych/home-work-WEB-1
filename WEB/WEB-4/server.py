import socket
import pathlib
import urllib.parse
import mimetypes
import logging
import json
from datetime import datetime
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

base_dir = pathlib.Path()
buffer_size = 1024
port_http = 3000
port_soket = 5000
host_socket = "127.0.0.1"


def send_data_to_socket(data):
    client_socet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socet.sendto(data, (host_socket, port_soket))
    client_socet.close()


class App(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        print(route.query)
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
        send_data_to_socket(data)
        self.send_response(302)
        self.send_header("Location", "message.html")
        self.end_headers()
        self.send_html("message.html")


def save_data(data):
    parse_data = urllib.parse.unquote_plus(data.decode())
    try:
        with open("storage/data.json", "r", encoding="utf-8") as file_data:
            dict_parse = json.load(file_data)
        date_n = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        dict_parse[date_n] = {
            key: value for key, value in [el.split("=") for el in parse_data.split("&")]
        }

        with open("storage/data.json", "w", encoding="utf-8") as file_data:
            json.dump(dict_parse, file_data, ensure_ascii=False, indent=4)
    except ValueError as error:
        logging.debug(f"for data {parse_data}, error: {error}")
    except OSError as error:
        logging.debug(f"Write data {parse_data}, error: {error}")


def run_socket_servet(host, port):
    server_soket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_soket.bind((host, port))

    try:
        while True:
            msg, adress = server_soket.recvfrom(buffer_size)
            save_data(msg)
    except KeyboardInterrupt:
        logging.info("Socket server stoped")
    finally:
        server_soket.server_close()


def run_http_server():
    address = ("localhost", port_http)
    httpd = HTTPServer(address, App)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Socket server stoped")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    th_server = Thread(target=run_http_server)
    th_server.start()

    th_socket = Thread(target=run_socket_servet, args=(host_socket, port_soket))
    th_socket.start()
