import os
import cfg_server_config as cfg

class FileReader :
    def __init__(self, path = cfg.UrtPath + "/" + cfg.UrtLogPath):
        self.path = path
        self.readsize = 0
        self.newlines = []

    def getNewLines(self):
        if os.path.getsize(self.path) > self.readsize:
            _file = open(self.path, "r")
            _file.seek(self.readsize)
            newlines = _file.read().split("\n")
            _file.close()
            self.readsize = os.path.getsize(self.path)
            return newlines
        elif os.path.getsize(self.path) < self.readsize:
            self.readsize = os.path.getsize(self.path)
            return None
