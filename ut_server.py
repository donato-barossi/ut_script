import random
import time
import logging
import cfg_server_config as cfg
from ut_map import UtMap
from ut_player import Player
from util_file_reader import FileReader
from util_ut_socket import Sock
from cfg_ut_const import Body 



logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)s %(message)s", filename='logs/app.log', filemode='w')

class UTServer:
    def __init__(self):
        self.socket = Sock()
        self.players = []
        self.maps = []
        self.admins = []
        self.loadMapsFromFile()
        
    def printPlayerStats (self, _id):
        player = self.getPlayerById(_id)
        if player:
            hs = player.stats.hs
            vest = 0
            butt = 0
            if Body.Torso.value in player.stats.hits:
                vest = vest + player.stats.hits[Body.Torso.value]
            if Body.Vest.value in player.stats.hits:
                vest = vest + player.stats.hits[Body.Vest.value]
            if Body.Butt.value in player.stats.hits:
                butt = butt + player.stats.hits[Body.Butt.value]
            hits = sum(player.stats.hits.values())
            self.socket.say("%s^7 hai messo a segno %s colpi: [%s ^1HS^7 - %s in pieno petto - %s a culo]" % (player.name, hits,  hs, vest, butt))

    def tellToUser (self, user, msg):
        if user and isinstance(user, Player) and msg and isinstance(msg, str):
            self.socket.tell(user.name, msg)

    def say (self, msg):
        if msg and isinstance(msg, str):
            self.socket.say(msg)

    def sendCmd (self, cmd):
        if cmd and isinstance(cmd, str):
            self.socket.sendcmd(cmd)

    def sendFunMsg(self, msg, _id = None):
        if _id:
            logging.debug("sending big text %s %s" % (msg, _id))
            player = self.getPlayerById(_id)
            if msg and player:
                msg = msg % player.name
                self.socket.bigText(msg)
        elif msg:
            logging.debug("sending big text %s" % msg)
            self.socket.bigText(msg)
        time.sleep(cfg.MessageDelay)

    def getPlayerById(self, _id):
        player = Player(_id)
        if player in self.players:
            return self.players[self.players.index(player)]
        else:
            return None

    def updatePlayerKills (self, _id):
        player = self.getPlayerById(_id)
        if player: 
            player.stats.killsInRow = player.stats.killsInRow +1
            player.stats.deathsInRow = 0
            return player.stats.killsInRow
        return -1

    def updatePlayerDead (self, _id):
        player = self.getPlayerById(_id)
        if player: 
            player.stats.deathsInRow = player.stats.deathsInRow +1
            player.stats.killsInRow = 0
            return player.stats.deathsInRow
        return -1

    def updatePlayerHits (self, _id, where):
        where = int(where)
        player = self.getPlayerById(_id)
        if player:
            if player.stats.hits.has_key(where):
                player.stats.hits[where] += 1
            else:
                player.stats.hits[where] = 1
            if where in [Body.Head.value, Body.Helmet.value]:
                player.stats.hs = player.stats.hs +1
            return player.stats.hs
        else:
            return -1

    def updatePlayer(self, _id, guid, name, weapmode):
        p = Player(_id, guid, name, weapmode)
        if p in self.players:
            p = self.players[self.players.index(p)]
            p.guid = guid
            p.name = name
            p.weapmode = weapmode
        else:
            self.players.append(p)
    
    def playerDisconnected (self, _id):
        p = Player(_id)
        if p in self.players:
            self.players.remove(p)

    def resetPlayersStats(self):
        for player in self.players:
            player.resetStats()

    def loadMapsFromFile (self, path = cfg.UrtPath + "/" + cfg.MapCyclePath):
        fileReader = FileReader(path)
        maps = fileReader.getNewLines()
        if maps and len(maps) > 0:
            self.maps = []
            for map in maps:
                self.maps.append(UtMap(map))

    def removeMap(self, name):
        map = UtMap(name)
        if map in self.maps:
            self.maps.remove()

    def getRandomMap(self):
        index = random.randint(0, len(self.maps) -1)
        return self.maps[index]