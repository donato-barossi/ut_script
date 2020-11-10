class UtStats:
    def __init__(self):
        self.hits = {}
        self.kills = {}
        self.hs = 0
        self.killsInRow = 0
        self.deathsInRow = 0

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