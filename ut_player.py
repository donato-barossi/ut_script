class UtStats:
    def __init__(self):
        self.hits = {}
        self.kills = {}
        self.deads = {}
        self.hs = 0
        self.killsInRow = 0
        self.deathsInRow = 0

    def updateKillsStats (self, _id):
        if _id in self.kills:
            self.kills[_id] = self.kills[_id]  + 1
        else:
            self.kills[_id] = 1

    def getMaxKills (self):
        return max(zip(self.kills.values(), self.kills.keys())) 

    def updateDeadsStats (self, _id):
        if _id in self.deads:
            self.deads[_id] = self.deads[_id]  + 1
        else:
            self.deads[_id] = 1

    def getMaxDeads (self):
        return max(zip(self.deads.values(), self.deads.keys())) 

class Player:
    def __init__(self, _id, guid = '', name = '', weapmode = '', gear = '', isProtected = False):
        self._id = _id
        self.guid = guid
        self.name = name
        self.gear = gear
        self.weapmode = weapmode
        self.stats = UtStats()
        self.isProtected = isProtected

    def resetStats(self):
        self.stats = UtStats()
        
    def __eq__(self, other):
        return self._id == other._id