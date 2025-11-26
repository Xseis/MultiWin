import socket
import json
import pygame
import threading
import win32gui

objects = []

def ServerConnection():
    global objects
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
            objects = data
        if not data:
            break

def Main():
    pygame.init()
    win = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    deltatime = 0
    hwnd = pygame.display.get_wm_info()["window"]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        windowrect = win32gui.GetWindowRect(hwnd)
        win.fill((200, 100, 100))
        for object in objects:
            x, y = object["position"]
            width, height = object["size"]
            pygame.draw.rect(win, (255, 255, 255), (x-windowrect[0], y-windowrect[1], width, height))

        pygame.display.update()
        deltatime = clock.tick(60)

if __name__ == "__main__":
    threading.Thread(target=ServerConnection, daemon=True).start()
    Main()