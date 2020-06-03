import enum
import random

UtCmds = {
    'gametype' : "g_gametype %s",
    'map' : "map %s",
    'next' : "g_nextmap %s",
    'cycle' : "cyclemap",
    'private' : "g_password %s",
    'only' : "g_gear %s",
    'all' : "g_gear %s"
}

AppCmds = {
    'stop' : 0,
    'restart' : 1,
    'pause' : 2,
    'resume' : 3
}

CustomComds = ['allow', 'deny', 'protection' ]

Auth = {
    'BF75A818B7749C51A991EB4EF4CB71DB' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick', 'slap', 'smite', 'nuke', 'timelimit'], # Dr.Geo
    'B44CA4A27A31FA0234CAA62E4F5EC67B' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick', 'slap', 'smite', 'nuke', 'timelimit'], # g1n8
    'C9F3DCA4B00F1EA9FA6A17E00642AC52' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick', 'slap', 'smite', 'nuke', 'timelimit'], # GJterror
    'A17B770E3619E2E1420DD21648ACD7E5' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick', 'slap', 'smite', 'nuke', 'timelimit'], # Capopattuglia
    'ABA582DE5E260E4C9C73D49CD66CBDDE' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick', 'slap', 'smite', 'nuke', 'timelimit'], # REVENGE
    '7012BEC27E05320119AF799B962C3A97' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick', 'slap', 'smite', 'nuke', 'timelimit'], # Maverick
    'D94814531BDCFD66595CC834F6EC5F87' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick', 'slap', 'smite', 'nuke', 'timelimit'], # giogio79
    '6F80784BD6672C739E8DFE010F3D063B' : ['*']  # dr.barossi
}

ProtectedPlayers = ["6F80784BD6672C739E8DFE010F3D063B"]
ProtectedPlayersMsgs = ["%s^7 e' sotto la protezione divina!", "Non vi azzardate a toccare %s^7!"]
NotAuthorizedMsgs = ["%s non sei autorizzato: ^1AH AH^7!", "Sfigato, questo comando non e' per te, %s"]

def getProtectedPlayersMsg():
    return ProtectedPlayersMsgs[random.randint(0, len(ProtectedPlayersMsgs)-1)]

def getNotAuthorizedMsg():
    return NotAuthorizedMsgs[random.randint(0, len(NotAuthorizedMsgs)-1)]

def isAuthorized (palyer, cmd):
    if palyer.guid in Auth:
        allowedcmds = Auth[palyer.guid]
        if cmd in allowedcmds or '*' in allowedcmds:
            return True
    return False

def getServerCommand (cmd):
    if cmd in UtCmds:
        return UtCmds[cmd]
    return None