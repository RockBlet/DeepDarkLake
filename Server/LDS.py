import time
import colorama
from colorama import Fore, Back, Style
import os


class logo:
    def __init__(self, logoFile) -> None:
        self.logo = open(logoFile).readlines()
        colorama.init(autoreset=True)

    def shw(self, host, port):

        try:
            os.system("cls")
        except:
            try:
                os.system("clear")
            except:
                pass

        for i in range(len(self.logo)):
            print(Fore.RED + self.logo[i], end="")
            time.sleep(0.07)
        print("\n")

        c  = Fore.YELLOW + "(C)" + Fore.RESET
        author = Fore.RED + "nemizuki" + Fore.RESET
        copyright = f"{c} by {author}"

        serverUpTitle = Fore.GREEN + Style.BRIGHT + "Server status [UP]"
        thost = Fore.BLUE + host
        tport = Fore.BLUE + str(port)

        print(copyright, "\n")
        print(serverUpTitle)
        print(f"  Host : {thost}")
        print(f"  Port : {tport}\n")

        