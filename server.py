import socket
import threading
import json
import time
import random

objects = []

objects.append({"position": (50, 50), "size": (100, 50)})

port = 8080
ip = "0.0.0.0"

clients = []
def HandleClients(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected")
                clients.remove(conn)
                conn.close()
                break
        except:
            print("Client disconnected unexpectedly")
            clients.remove(conn)
            conn.close()
            break

def send():
    data = json.dumps(objects).encode() + b"\n"
    for client in clients.copy():
        try:
            client.sendall(data)
        except:
            print(f"{client} client removed")
            clients.remove(client)

def ServerConnection():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()
    print(f"Server started on port {port}")

    while True:
        conn, addr = server.accept()
        print(f"{addr} connected")
        clients.append(conn)
        send()
        threading.Thread(target=HandleClients, args=(conn, addr), daemon=True).start()

def Main():
    while True:
        time.sleep(5)
        for object in objects:
            object["position"] = (random.randint(1, 500), random.randint(1, 500))
        send()
        print(objects)


if __name__ == "__main__":
    threading.Thread(target=ServerConnection, daemon=True).start()
    Main()