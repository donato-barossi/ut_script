import random
from cfg_ut_const import Body
from cfg_ut_const import UTMode
from cfg_ut_const import UTGearItems


HitMsgs = {
    Body.Butt.value: ["Attento ^1%s^7: ti stanno sparando a culo!"],
    # Body.Groin.value: ["uuuh.. ^1%s^7 questa fa male.. dritto alle palle!", "^1%s^7 i gioielli di famiglia sono ancora li?"],
    Body.RightFoot.value: ["[%s] Balla Spider!"],
    Body.LeftFoot.value: ["[%s] Balla Spider!"]
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
    5: ["%s^7 ha fatto ^15^7 kills di fila: FERMATELO!", "^15^7 kills senza schiattare, %s^7 ma sei un killer!"],
    10: ["%s^7 ... Rambo in action!! ^110^7 kills di fila!"],
    15: ["%s^7 e sono ^115^7... Il Chuck Norris di giornata!"]
}

SeriesOfDeadMsgs = {
    3: ["%s^7 sei morto 3 volte di fila ... ti spiego come si gioca?"],
    5: ["%s^7 siamo gia' a 5... forse e' meglio se ti dai all'ippica!"]
}

HeadShotsMsgs = {
    5: ["%s ^15^7 headshots .. puoi fare di meglio!"],
    10: ["%s^7 ^110^7 headshots .. continua cosi' campione!"],
    15: ["%s^7 hulala!! ^115^7 headshots!"],
    20: ["%s^7 che precisione: ^120^7 headshots!"],
    25: ["%s^7 e' in forma: ^125^7 headshots!"],
    30: ["%s^7 un cecchino nato: ^130^7 headshots!"]
}

FunnyDeadMessage = {
    # Capopattuglia
    'A17B770E3619E2E1420DD21648ACD7E5': {
        UTMode.UT_MOD_KNIFE.value: [
            "Il ^1maiale^7 e' stato scannato!",
            "Un ^1maiale^7 e' stato macellato!",
            "Accendete la brace, le costolette sono pronte!"
        ]},
    # giogio79
    'D94814531BDCFD66595CC834F6EC5F87': {
        UTMode.UT_MOD_KNIFE.value: [
            "Spennata la ^1quaglia^7!!",
            "Era una ^1quaglia^7 zoppa.. troppo facile!",
            "Piu' che una quaglia sembrava una ^1gallina^7!!"
        ]},
    # g1n8
    'B44CA4A27A31FA0234CAA62E4F5EC67B' : {
        UTMode.UT_MOD_HEGRENADE: [
            "Caccia grossia al ^1cinghiale^7!!"
        ]}
}

FunnyKillMessage = {
    # Capopattuglia
    'A17B770E3619E2E1420DD21648ACD7E5': {
        UTMode.UT_MOD_KNIFE.value: [
            "La vendetta del maiale si e' abbattuta su ^1%s",
            "E il maiale colpisce ancora (^1%s^7 che finaccia!)",
            "^1%s^7 attento! Questo maiale e' proprio vendicativo"
        ]}
}

def getFunGearMessage (guid, gear):
    #Tactical Goggles	
    if gear.__contains__("S") == True:
        return "%s, solo i froci portano gli occhialini!"
    #Kevlar Vest
    if gear.__contains__("R") == False:
        return "%s a petto nudo.. Ti senti forte!"
    #Helmet
    if gear.__contains__("W") == False:
        return "%s senza elmetto.. Ti senti fortunato!"
    #Smoke Grenade
    if gear.__contains__("Q") == True:
        return "%s, a chi vo roppe' li coglioni co ste fumogene?"
    #IMI Negev
    if gear.__contains__("c") == True:
        return "%s, hai preso un arma di fino!!"


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
