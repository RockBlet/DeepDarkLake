import os
from dataset import Dataset


if __name__ == "__main__":
    db = Dataset("Server/BotTable.csv")

    while True:
        botList = db.get()
        print(f"\t: LBT : \nBots count _ {len(botList)} _\n")

        for i in botList:
            print(i)

        nbl = db.get()
        while nbl == botList:
            nbl = db.get()

        os.system("cls")