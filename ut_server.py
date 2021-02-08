import random
import logging
import re
import os
import cfg_server_config as cfg
from ut_map import UtMap
from ut_player import Player
from util_file_reader import FileReader
from util_file_reader import FileWriter
from util_ut_socket import Sock
from cfg_ut_const import Body


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)s %(message)s",
                    filename='logs/app.log', filemode='w')


class UTServer:
    def __init__(self):
        self.socket = Sock()
        self.players = []
        self.maps = []
        self.admins = []
        self.banned = []
        self.loadMapsFromFile()

    def printAllStats (self):
        for player in self.players:
            self.printPlayerStats(player._id)

    def printPlayerStats(self, _id):
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
            self.socket.console(
                "%s^7 hai messo a segno %s colpi: [%s ^1HS^7 - %s in pieno petto - %s a culo]" % (player.name, hits,  hs, vest, butt))
            maxKilledBy = player.stats.getMaxDeads
            self.socket.console(
                "%s^7 sei stato ucciso %s volte da %s^7. Il tuo incubo peggiore!" 
                % (player.name, maxKilledBy[0], self.getPlayerById(maxKilledBy[1]).name))

    def tellToUser(self, user, msg):
        if user and isinstance(user, Player) and msg and isinstance(msg, str):
            self.socket.tell(user.name, msg)

    def say(self, msg):
        if msg and isinstance(msg, str):
            self.socket.say(msg)

    def sendCmd(self, cmd):
        if cmd and isinstance(cmd, str):
            logging.debug("sending command: %s" % cmd)
            self.socket.sendcmd(cmd)

    def sendFunMsg(self, msg, _id=None):
        if _id:
            logging.debug("sending big text %s %s" % (msg, _id))
            player = self.getPlayerById(_id)
            if msg and player:
                msg = msg % player.name
                self.socket.bigText(msg)
        elif msg:
            logging.debug("sending big text %s" % msg)
            self.socket.bigText(msg)
        else:
            return False
        return True

    def getPlayerById(self, _id):
        player = Player(_id)
        if player in self.players:
            return self.players[self.players.index(player)]
        else:
            return None

    def getPlayerByName(self, name):
        count = 0
        _player = None
        if name:
            pattern = re.compile(r'%s' % name)
            for player in self.players:
                _name = re.sub(r'\^\d', '', player.name)
                # _name == name or _name.startswith('name'):
                if pattern.match(_name):
                    _player = player
                    count = count + 1
        if count == 1:
            return _player
        else:
            return None

    def updatePlayerKills(self, _id, killed = None):
        player = self.getPlayerById(_id)
        if player:
            player.stats.killsInRow = player.stats.killsInRow + 1
            player.stats.deathsInRow = 0
            if killed:
                player.stats.updateKillsStats(killed)
            return player.stats.killsInRow
        return -1

    def updatePlayerDead(self, _id, killer = None):
        player = self.getPlayerById(_id)
        if player:
            player.stats.deathsInRow = player.stats.deathsInRow + 1
            player.stats.killsInRow = 0
            if killer:
                player.stats.updateDeadsStats(killer)
            return player.stats.deathsInRow
        return -1

    def updatePlayerHits(self, _id, where):
        where = int(where)
        player = self.getPlayerById(_id)
        if player:
            if player.stats.hits.has_key(where):
                player.stats.hits[where] += 1
            else:
                player.stats.hits[where] = 1
            if where in [Body.Head.value, Body.Helmet.value]:
                player.stats.hs = player.stats.hs + 1
            return player.stats.hs
        else:
            return -1

    def updatePlayer(self, _id, guid, name, weapmode, gear, isProtected):
        if guid in self.banned:
            logging.debug("Palyer %s is banned. Kicking him." % name)
            self.socket.sendcmd("kick " + name)
        else:
            p = Player(_id, guid, name, weapmode, gear, isProtected)
            if p in self.players:
                p = self.players[self.players.index(p)]
                p.guid = guid
                p.name = name
                p.weapmode = weapmode
                p.gear = gear
            else:
                self.players.append(p)

    def playerDisconnected(self, _id):
        p = Player(_id)
        if p in self.players:
            self.players.remove(p)

    def resetPlayersStats(self):
        for player in self.players:
            player.resetStats()

    def loadMapsFromFile(self, path=cfg.UrtPath + "/" + cfg.MapCyclePath):
        logging.debug("Reading maps file: %s" % path)
        fileReader = FileReader(path, True)
        maps = fileReader.getNewLines()
        logging.debug("Laded %s maps" % len(maps))
        if maps and len(maps) > 0:
            self.maps = []
            for map in maps:
                self.maps.append(UtMap(map))

    def removeMap(self, name):
        map = UtMap(name)
        if map in self.maps:
            self.maps.remove(map)

    def getRandomMap(self):
        index = random.randint(0, len(self.maps) - 1)
        return self.maps[index]

    def loadBannedPlayer (self):
        reader = FileReader("data/banlist.txt", True)
        for line in reader.getNewLines():
            self.banned.append(line)

    def banPlayer (self, player):
        writer  = FileWriter("data/banlist.txt")
        writer.writeNewLine(player.guid)
        self.banned.append(player.guid)
        