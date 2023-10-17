import yaml


class CFG:
    def __init__(self):
        self.cfgFile = "Server/ServerConfig.yaml"
    
    def GetCFG(self) -> dict:
        with open(self.cfgFile, "r") as stream:
            config = yaml.safe_load(stream)
            return config

