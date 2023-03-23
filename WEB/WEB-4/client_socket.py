import socket

def main():
    host = socket.gethostname()
    port = 5000

    client_socet = socket.socket()
    client_socet.connect((host, port))

    message = input(">>> ")
    while message.lower().strip() != 'exit':
        client_socet.send(message.encode())
        msg = client_socet.recv(1024).decode()
        print(f"Received message: {msg}")
        message = input(">>> ")
    
    client_socet.close()


if __name__ == "__main__":
    main()