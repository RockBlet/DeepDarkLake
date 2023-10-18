import time
import colorama
from colorama import Fore, Back, Style
import os
import random


class logo:
    def __init__(self, logoFilelist) -> None:
        self.logoFilelist = logoFilelist
        colorama.init(autoreset=True)

    def print_gradient_text(self, lines):
        red = Fore.RED
        white = Fore.WHITE
        gradient = max(len(line) for line in lines) - 1  
        
        for line in lines:
            time.sleep(0.12)
            for i, char in enumerate(line):
                color_index = int(i / len(line) * gradient)
                if color_index % 2 == 0:
                    color = red
                else:
                    color = white
                print(color + char, end='')
        
        print(Style.RESET_ALL)  

    def draw(self, lg):

        for i in range(len(lg)):
            print(Fore.RED + self.logo[i], end="")
            time.sleep(0.07)
        print("\n")

    def shw(self, host, port):

        try:
            os.system("cls")
        except:
            try:
                os.system("clear")
            except:
                pass

        self.logo = open(random.choice(self.logoFilelist)).readlines()

        hd = random.randint(1,2)

        if hd == 1:
            self.print_gradient_text(self.logo)
        elif hd == 2:
            self.draw(self.logo)

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

        