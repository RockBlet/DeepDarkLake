from colorama import Fore, Back, Style
import os
import socket


class QueryListServer:
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
    
        self.QueryServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.QueryServer.bind((self.ip, self.port))
        self.QueryServer.listen(5)

        try: 
            os.system("cls")
        except:
            os.system("clear")

        print(Style.BRIGHT + Fore.CYAN + ":QUERY SERVER [UP]:" + Fore.RESET + Style.RESET_ALL)

    def framePP(self, socket, addr):
        ipT = Fore.GREEN + self.ip + Fore.RESET
        portT = Fore.GREEN + str(self.port) + Fore.RESET
        i = Fore.GREEN + "i" + Fore.RESET
        up = Fore.GREEN + "UP" + Fore.RESET
        p = Fore.BLUE + "+" + Fore.RESET

        sockT = Fore.BLUE + str(socket) + Fore.RESET
        addrT = Fore.BLUE + str(addr[0]) + str(addr[1]) + Fore.RESET

        print(f"[{p}]: Server is {up}")
        print(f"[{i}]<IP> {ipT}")
        print(f"[{i}]<PORT> {portT}")

        print("{")
        print(f"  {sockT}")
        print(f"  {addrT}")
        print("}")


    # data & data
    def dataSource(self, data):
        ft, st = data.split("&")
        return ft , st

    def output(self, ft , st):
        reqT = Fore.GREEN + "req" + Fore.RESET
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
                ft, st = self.dataSource(data)
                self.output(ft, st)

if __name__ == "__main__":
    q = QueryListServer("localhost", 7777)
    q.QueryRecv()
