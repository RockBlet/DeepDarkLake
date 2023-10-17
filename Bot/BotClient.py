import socket
import threading


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        # Запуск потока для получения сообщений от сервера
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        print("[i] Connection - SUCCESS")

    def source(slef, cmd):
        if cmd == "/source":
            print("SOURCE FUNC <200>")

        elif cmd == "/ddos":
            pass

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()

                if message:
                    print("[rcv](command)> {}".format(message))
                    self.source(message)
            except:
                break

    def disconnect(self):
        self.client_socket.close()


if __name__ == '__main__':
    client = Client('localhost', 6666)
    client.connect()

