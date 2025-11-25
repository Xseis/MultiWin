import socket
import json
import pygame


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8080))

    print("Connected to server")

    buffer = b""
    while True:
        buffer += client.recv(1024)

        if b"\n" in buffer:
            data, buffer = buffer.split(b"\n", 1)
            data = json.loads(data.decode())
            print(data, type(data))
        if not data:
            break

if __name__ == "__main__":
    main()