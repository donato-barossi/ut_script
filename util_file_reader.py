import os
import cfg_server_config as cfg

class FileReader :
    def __init__(self, path = cfg.UrtPath + "/" + cfg.UrtLogPath, fromBeginning = False):
        self.path = path
        if fromBeginning:
            self.readsize = 0
        else:
            self.readsize = os.path.getsize(self.path)

    def getNewLines(self):
        newlines = []
        if os.path.getsize(self.path) > self.readsize:
            _file = open(self.path, "r")
            _file.seek(self.readsize)
            newlines = _file.read().split("\n")
            _file.close()
            self.readsize = os.path.getsize(self.path)
        elif os.path.getsize(self.path) < self.readsize:
            self.readsize = os.path.getsize(self.path)
        return newlines
