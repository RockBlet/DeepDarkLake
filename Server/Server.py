import socket
import threading


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server started and listening on {}:{}".format(self.host, self.port))

        # Запуск потока для чтения сообщений из терминала
        input_thread = threading.Thread(target=self.read_input)
        input_thread.start()

        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)

            # Обработка подключения клиента в отдельном потоке
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print("Received message: {}".format(message))
                    self.send_to_all_clients(message)
                else:
                    self.clients.remove(client_socket)
                    break
            except:
                self.clients.remove(client_socket)
                break

    def broadcast(self, message):
        for client in self.clients:
            client.send(message.encode())

    def source(self, cmd):
        cmdList = ["/msg - Broadcast",
                   "@bot - Bot list",
                   "$panic - to server down"
                   ]

        if cmd[0] == "/":
            self.broadcast(cmd)

        elif cmd == "@bot":
            for bot in self.clients:
                print(bot)

        elif cmd == "$panic":
            exit()

        elif cmd == "help":
            for cmd in cmdList:
                print(cmd)

    def read_input(self):
        while True:
            cmd = input(">> ")
            self.source(cmd)

    def stop(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()
        print("Server stopped")


if __name__ == '__main__':
    server = Server('localhost', 8080)
    server.start()