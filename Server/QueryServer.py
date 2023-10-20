from colorama import Fore, Back, Style
import os
import socket
import logging
from LoggingFormat import LogFormat
from Config import CFG


class QueryListServer:
    def __init__(self, ip:str, port:str) -> None:
        self.ip = ip
        self.port = port
    
        self.QueryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.QueryServer.bind((self.ip, self.port))
        self.QueryServer.listen(5)

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

        try: 
            os.system("cls")
        except:
            os.system("clear")

        print(Style.BRIGHT + Fore.CYAN + ":QUERY SERVER [UP]:" + Fore.RESET + Style.RESET_ALL)

    def framePP(self, socket:str, addr:str) -> None:
        ipT = Fore.GREEN + self.ip + Fore.RESET
        portT = Fore.GREEN + str(self.port) + Fore.RESET
        i = Fore.GREEN + "i" + Fore.RESET
        up = Fore.GREEN + "UP" + Fore.RESET
        p = Fore.BLUE + "+" + Fore.RESET

        sockT = Fore.BLUE + str(socket) + Fore.RESET
        addrT = Fore.BLUE + str(addr[0]) +" : "+ str(addr[1]) + Fore.RESET

        print(f"[{p}]: Server is {up}")
        print(f"[{i}]<IP> {ipT}")
        print(f"[{i}]<PORT> {portT}")

        print("{")
        print(f"  {sockT}")
        print(f"  {addrT}")
        print("}")
    
    def err(self, e, **kwargs) -> None:
        errT = Fore.RED + "ERROR" + Fore.RESET
        errT = f"[-]    <{errT}>    [-]"
        openT = Fore.RED + "{" + Fore.RESET
        closeT = Fore.RED + "}" + Fore.RESET
        print("\n",errT)
        print(openT)
        print("\t",e)
        print(closeT, "\n")

        if kwargs:
            for key in kwargs:
                print(f"\t{key} :: {kwargs[key]} ")
    
    def debugOut(self, data: str):
        debugLog = Fore.BLUE + "[debug]" + Fore.RESET
        self.Deeplogger.debug(f"|QUERY| {data}")
        print(f"{debugLog} : {data}")

    # data & data
    def dataSource(self, data:str):
        try:
            ft, st, ip, port = data.split("&")
            return [ft, st, ip, port]
        except Exception as e:
            self.err(e, data)

    def output(self, ft:str, st:str, ip:str, port) -> None:
        reqT = Fore.GREEN + f"{ip}:{port}" + Fore.RESET
        reqT = f"[{reqT}]"
        ft = Fore.BLUE + str(ft) + Fore.RESET
        string = f"{reqT}(Bot)<{ft}>: {st}"
        print(string)

    def QueryRecv(self):
        mainFrame_Socket, mainFrame_Address = self.QueryServer.accept()
        
        self.framePP(mainFrame_Socket, mainFrame_Address)

        while True:
            data = mainFrame_Socket.recv(1024).decode()
            if data != '':
                self.debugOut(data)
                try: 
                    ft = self.dataSource(data)[0]
                    st = self.dataSource(data)[1]
                    ip = self.dataSource(data)[2]
                    port = self.dataSource(data)[3]
                    self.output(ft=ft, st=st, ip=ip, port=port)
                except Exception as e:
                    self.err(e)

if __name__ == "__main__":
    q = QueryListServer("localhost", 7777)
    q.QueryRecv()
