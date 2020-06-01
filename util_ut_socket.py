import socket
import time
import cfg_server_config as cfg

class Sock:

    def __init__(self):
        self.rcon = cfg.ServerRcon
        self.host = cfg.ServerIp
        self.port = cfg.ServerPort
        self.header = chr(255) + chr(255) + chr(255) + chr(255) + "rcon " + self.rcon + " "
        self.socket = self.__initSocket__()
        self.isopen = False
        self.__connect__()

    def __initSocket__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(cfg.ServerTimeout)
        return s

    def __connect__ (self):
        self.socket.connect((self.host, self.port))
        self.isopen = True
    
    def disconnect(self):
        self.socket.close()
        self.isopen = False

    def say(self, msg):
        self.sendcmd('say "%s"' % msg)

    def bigText(self, msg):
        self.sendcmd('bigtext "%s"' % msg)

    def tell(self, user, msg):
        self.sendcmd('tell %s "%s"' % (user, msg))

    def console(self, msg):
        self.sendcmd('"%s"' % msg)

    def nextMap(self, map):
        self.sendcmd("g_nextmap " + map.name)

    def mapList(self, user, maplist):
        sep = ', '
        mapsArray = []
        _map = []
        index = 0
        for map in maplist:
            if index > 0 and index % 8 == 0:
                mapsArray.append(_map)
                _map = []
            _map.append(map.name)
            index = index + 1
        for sublist in mapsArray:
            self.tell(user.name, sep.join(sublist))
            time.sleep(0.25)
       
    def changeMap(self, map):
        self.sendcmd('map ' + map.name )

    def sendcmd(self,cmd):
        cmd = self.header + cmd
        try:
            self.socket.send(cmd)
        except:
            time.sleep(0.5)
            self.socket = self.__initSocket__()
            self.__connect__()
            if self.isopen:
                self.socket.send(cmd)
            else:
                raise
