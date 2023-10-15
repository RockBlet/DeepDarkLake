import csv


class Dataset:
    def __init__(self, dbFile: str):
        self.file = dbFile

    def get(self):
        bl = []
        with open(self.file, 'r') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                bl.append(row)

        return bl

    def Push(self, ip, port):
        with open(self.file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ip, port])

    def get_raddr(self, socket_string):
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

        ip = socket_string
        port = 0
        return ip, port

