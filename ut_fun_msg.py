import random
from cfg_ut_const import Body
from cfg_ut_const import UTMode


HitMsgs = {
    Body.Butt.value: ["Attento ^1%s^7: ti stanno sparando a culo!"],
    Body.RightFoot: ["[%s] Balla Spider!"],
    Body.LeftFoot: ["[%s] Balla Spider!"]
}

KillMsgs = {
    UTMode.MOD_SUICIDE.value: ["^1%s ^7ha deciso di suicidarsi!"],
    UTMode.MOD_TRIGGER_HURT.value: ["^1%s ^7che fine da pollo!"],
    # UTMode.UT_MOD_KNIFE : [""],
    UTMode.UT_MOD_NUKED.value: ["^1%s ^7e' stato silurato dall'admin!"],
    UTMode.UT_MOD_SMITED.value: ["^1%s ^7si e' beccato la punizione divina!"],
    UTMode.MOD_FALLING.value: ["^1%s ^7e' morto miseramente!"]
}

KillStreakMsgs = {
    5: ["%s ha fatto ^15^7 kills di fila: FERMATELO!"],
    10: ["%s ... Rambo in action!! ^110^7 kills di fila!"],
    15: ["%s e sono ^115^7... Il Chuck Norris di oggi!"]
}

SeriesOfDeadMsgs = {
    3: ["%s sei morto 3 volte di fila ... ti spiego come si gioca?"],
    5: ["%s siamo gia' a 5... forse e' meglio se ti dai all'ippica!"]
}

HeadShotsMsgs = {
    5: ["%s ^15^7 headshots .. puoi fare di meglio!"],
    10: ["%s ^110^7 headshots .. continua cosi' campione!"],
    15: ["%s hulala!! ^115^7 headshots!"],
    20: ["%s che precisione: ^120^7 headshots!"],
    25: ["%s e' in forma: ^125^7 headshots!"],
    30: ["%s un cecchino nato: ^130^7 headshots!"]
}

FunnyDeadMessage = {
    # Capopattuglia
    'A17B770E3619E2E1420DD21648ACD7E5': {
        UTMode.UT_MOD_KNIFE.value: [
            "Il ^1maiale^7 e' stato scannato"
        ]},
    # giogio79
    'D94814531BDCFD66595CC834F6EC5F87': {
        UTMode.UT_MOD_KNIFE.value: [
            "Spennata la ^1quaglia^7!!"
        ]},
}

FunnyKillMessage = {
    # Capopattuglia
    'A17B770E3619E2E1420DD21648ACD7E5': {
        UTMode.UT_MOD_KNIFE.value: [
            "La vendetta del maiale si e' abbattuta su %s",
            "E il maiale colpisce ancora (%s che finaccia!)"
        ]}
}

def getFunKillMessage(guid, mode):
    if guid in FunnyKillMessage and mode in FunnyKillMessage[guid]:
        msgs = FunnyKillMessage[guid][mode]
        return msgs[random.randint(0, len(msgs)-1)]
    else:
        return None

def getFunDeadMessage(guid, mode):
    if guid in FunnyDeadMessage and mode in FunnyDeadMessage[guid]:
        msgs = FunnyDeadMessage[guid][mode]
        return msgs[random.randint(0, len(msgs)-1)]
    else:
        return None

def getHSMsg(key):
    return __get_msg__(HeadShotsMsgs, key)


def getHitMsg(key):
    return __get_msg__(HitMsgs, key)


def getKillMsg(key):
    return __get_msg__(KillMsgs, key)


def getKillStreakMsg(key):
    return __get_msg__(KillStreakMsgs, key)


def getSeriesOfDeadMsg(key):
    return __get_msg__(SeriesOfDeadMsgs, key)


def __get_msg__(messages, key):
    if key in messages:
        msgs = messages[key]
        return msgs[random.randint(0, len(msgs)-1)]
    else:
        return None
