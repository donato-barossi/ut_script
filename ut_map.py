class UtMap:
    def __init__(self, name, alias = '', played = False):
        self.name  = name
        self.alias = alias
        self.played = played

    def __eq__(self, other):
        return self.name == other.name