import socket
import threading
from dataset import Dataset
from loguru import logger
from colorama import Fore, Back, Style
import logging
from LoggingFormat import LogFormat
from LDS import logo


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = None

        self.botTable = "Server/BotTable.csv"
        self.lds = "Server/lds/lds.txt"
        self.LoggHandler = "Server/Loggs/Loggs.log"

        self.dataset = Dataset(self.botTable)

        #   Deep Logger
        self.Deeplogger = logging.getLogger()
        self.Deeplogger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(self.LoggHandler)
        file_handler.setLevel(logging.DEBUG)

        log_formatter = LogFormat()
        file_handler.setFormatter(log_formatter)

        # добавление обработчика файла в регистратор логов
        self.Deeplogger.addHandler(file_handler)

        # LDS module
        self.lds = logo(self.lds)


    def log(self, type, data):
        serverTitle = Style.BRIGHT + Fore.BLUE + "Server[OUT](Con.Log)" + Style.NORMAL
        deepData = data
        data = f"{serverTitle} : {data}"

        if type == "info":
            logger.info(data)
            self.Deeplogger.info(deepData)

        elif type == "debug":
            logger.debug(data)
            self.Deeplogger.debug(deepData)

        elif type == "waring":
            logger.warning(data) 
            self.Deeplogger.warning(deepData)

        elif type == "error":
            logger.error(data)
            self.Deeplogger.error(deepData)

        elif type == "critical":
            logger.critical(data)
            self.Deeplogger.critical(deepData)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.lds.shw(self.host, self.port)
        
        print("Server started and listening on {}:{}".format(self.host, self.port))

        # Запуск потока для чтения сообщений из терминала
        input_thread = threading.Thread(target=self.console)
        input_thread.start()
        self.Deeplogger.debug("[Console](read).Thread $Start")

        while True:
            client_socket, client_address = self.server_socket.accept()

            print(" ")

            self.log("info", f"New connection <{client_address}>:S85")
            self.log("debug", f"Socket - (({client_socket})):S86")

            #print(".(Type Enter to countinue)")

            self.clients.append(client_socket)

            ip, port = self.dataset.get_raddr(str(client_socket))
            self.dataset.Push(ip, port)

            # Обработка подключения клиента в отдельном потоке
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            self.Deeplogger.info(f"new Thread {client_address}")


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
        self.Deeplogger.debug(f"[broadcasst].msg <{message}>")
        
        for client in self.clients:
            client.send(message.encode())
            self.Deeplogger.info(f"[send]\n\t|>>>>({client})>({message})")


    def source(self, cmd):
        cmdList = ["/msg - Broadcast",
                   "@bot - Bot list",
                   "$panic - to server down",
                   "$log - show last n loggs",
                   "$lds - Call Lds"
                   ]

        if cmd:
            self.Deeplogger.info(f"[input]({cmd})")

            if cmd[0] == "/":
                self.broadcast(cmd)

            elif cmd == "@bot":
                self.Deeplogger.debug(f"count of @bot <Server.bot.connected>")

                
                if len(self.clients) == 0:
                    print("[@bot]() - 0 bots conected")
                
                elif len(self.clients) > 0:     
                    for bot in self.clients:
                        print(bot)
                    print(f"[@bot]() - {len(self.clients)} bots conected")

                else:
                    self.Deeplogger.warning("@bot error - ERR <List len>")

            elif cmd == "$log":
                self.isLogging = True
                self.logState = int(input("[Loggs](count) > ")) 

                with open(self.LoggHandler, 'r') as file:
                    lines = file.readlines()
                    lastnlines = [line.strip() for line in lines[-self.logState:]][::-1]

                    print("="*96)          
                    for log in lastnlines:
                        print("{")
                        print(f"  {log}")
                        print("}")

                    print("="*96)          

            elif cmd == '$lds':
                self.lds.shw()

            elif cmd == "$panic":
                self.Deeplogger.error("Panic Func is brkn <Server actully UP[ok]>")
                exit()

            elif cmd == "help":
                print(f"- - CMDS list - -")
                for cmd in cmdList:
                    print(f"|- - {cmd}")
                print("\n")

            else:
                self.Deeplogger.warning(f"[Unknown input]({cmd})")

    def console(self):
        st = Fore.CYAN + "Server" + Fore.RESET
        arr = Fore.CYAN + "> "+ Fore.RESET
        title = f"[{st}](cmd) {arr}"
        while True:
            cmd = input(title)
            self.source(cmd)

    def stop(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()
        print("Server stopped")


if __name__ == '__main__':
    server = Server("localhost", 8080)
    server.start()