import socket


def main():
    host = socket.gethostname()
    port = 5000

    server_soket = socket.socket()
    server_soket.bind((host, port))
    server_soket.listen()
    conn, adress = server_soket.accept()
    print(f"Connection from: {adress}")
    while True:
        msg = conn.recv(1024).decode()
        if not msg:
            break
        print(f"Received message: {msg}")
        message = input('>>> ')
        conn.send(message.encode())
    conn.close()
    server_soket.close()

if __name__ == "__main__":
    main()
