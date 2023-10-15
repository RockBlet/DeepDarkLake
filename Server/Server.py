import socket
import threading
from dataset import Dataset
from loguru import logger
from colorama import Fore, Back, Style
import logging
from LoggingFormat import LogFormat


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = None

        self.botTable = "Server/BotTable.csv"

        self.dataset = Dataset(self.botTable)

        #Deep Logger
        self.Deeplogger = logging.getLogger()
        self.Deeplogger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler("Server/Loggs/Loggs.log")
        file_handler.setLevel(logging.DEBUG)

        log_formatter = LogFormat()
        file_handler.setFormatter(log_formatter)

        # добавление обработчика файла в регистратор логов
        self.Deeplogger.addHandler(file_handler)

    def log(self, type, data):
        serverTitle = Style.BRIGHT + Fore.BLUE + "Server" + Style.NORMAL
        data = f"{serverTitle} : {data}"


        if type == "info":
            logger.info(data)
        
        elif type == "debug":
            logger.debug(data)
        
        elif type == "waring":
            logger.warning(data) 

        elif type == "error":
            logger.error(data)
        
        elif type == "critical":
            logger.critical(data)


    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server started and listening on {}:{}".format(self.host, self.port))

        # Запуск потока для чтения сообщений из терминала
        input_thread = threading.Thread(target=self.console)
        input_thread.start()

        while True:
            client_socket, client_address = self.server_socket.accept()

            print(" ")

            self.log("info", f"Connect <{client_address}>")
            self.log("debug", f"Socket - (({client_socket}))")
            self.Deeplogger.info(f"Connect <{client_address}>")
            self.Deeplogger.debug(f"Socket - ({client_socket})")

            #print(".(Type Enter to countinue)")

            self.clients.append(client_socket)

            ip, port = self.dataset.get_raddr(str(client_socket))
            self.dataset.Push(ip, port)

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
        if cmd:
            if cmd[0] == "/":
                self.broadcast(cmd)

            elif cmd == "@bot":
                for bot in self.clients:
                    print(bot)

            elif cmd == "$log":
                self.isLogging = True
                self.logState = str(input("(Log state)>> "))

            elif cmd == "$panic":
                exit()

            elif cmd == "help":
                for cmd in cmdList:
                    print(cmd)

            else:
                pass

    def console(self):
        
        while True:
            cmd = input(">> ")
            self.source(cmd)

    def stop(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()
        print("Server stopped")


if __name__ == '__main__':
    server = Server("localhost", 8080)
    server.start()