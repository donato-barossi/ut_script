import enum

UtCmds = {
   # cmds.allow.value : "",
   # cmds.deny.value : "",
    'gtype' : "g_gametype %s",
    'map' : "map %s",
    'next' : "g_nextmap %s",
    'cycle' : "map %s",
    'private' : "g_password %s",
    'only' : "g_gear %s",
    'all' : "g_gear %s"
}

AppCmds = {
    'stop' : 1,
    'restart' : 2,
    'pause' : 3,
    'resume' : 4
}

Auth = {
    'BF75A818B7749C51A991EB4EF4CB71DB' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick'], # Dr.Geo
    'B44CA4A27A31FA0234CAA62E4F5EC67B' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick'], # g1n8
    'C9F3DCA4B00F1EA9FA6A17E00642AC52' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick'], # GJterror
    'A17B770E3619E2E1420DD21648ACD7E5' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick'], # Capopattuglia
    'ABA582DE5E260E4C9C73D49CD66CBDDE' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick'], # REVENGE
    '7012BEC27E05320119AF799B962C3A97' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick'], # Maverick
    'D94814531BDCFD66595CC834F6EC5F87' : ['gtype', 'map', 'next', 'cycle', 'private', 'only', 'all', 'allow', 'deny', 'kick'], # giogio79
    '6F80784BD6672C739E8DFE010F3D063B' : ['*']  # dr.barossi
}

NotAuthorizedMsg = "%s non sei autorizzato: ^1AH AH^7!"

def isAuthorized (palyer, cmd):
    if palyer.guid in Auth:
        allowedcmds = Auth[palyer.guid]
        if cmd in allowedcmds or '*' in allowedcmds:
            return True
    return False

def getUserCommand (cmd):
    if cmd in UtCmds:
        return UtCmds[cmd]
    return None