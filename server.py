import socket
import threading
import json

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

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()
    print(f"Server started on port {port}")

    def send():
        data = json.dumps(objects).encode() + b"\n"
        for client in clients.copy():
            client.sendall(data)

    while True:
        conn, addr = server.accept()
        print(f"{addr} connected")
        clients.append(conn)
        send()
        threading.Thread(target=HandleClients, args=(conn, addr)).start()

if __name__ == "__main__":
    main()