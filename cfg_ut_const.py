import enum


class Body(enum.Enum):
    Head = 1
    Helmet = 2
    Torso = 3
    Vest = 4
    LeftArm = 5
    RightArm = 6
    Butt = 8
    LeftUpperLeg = 9
    RightUpperLeg = 10
    LeftLowerLeg = 11
    RightLowerLeg = 12
    LeftFoot = 13
    RightFoot = 14
    Groin = 7


class GameType(enum.Enum):
    LMS = 1
    FFA = 2
    TDM = 3
    TS = 4
    FTL = 5
    CNH = 6
    CTF = 7
    BM = 8
    JUMP = 9
    FT = 10


class UTMode(enum.Enum):
    UT_MOD_KNIFE = 12
    UT_MOD_BERETTA = 2
    UT_MOD_DEAGLE = 3
    UT_MOD_SPAS = 4
    UT_MOD_UMP45 = 17
    UT_MOD_LR300 = 8
    UT_MOD_G36 = 20
    UT_MOD_PSG1 = 10
    UT_MOD_HEGRENADE = 25
    UT_MOD_SR8 = 14
    UT_MOD_AK103 = 15
    UT_MOD_NEGEV = 36
    UT_MOD_M4 = 19
    UT_MOD_GLOCK = 39
    UT_MOD_MAC11 = 41
    UT_MOD_P90 = 44
    UT_MOD_HK69 = 22
    UT_MOD_NUKED = 35
    UT_MOD_BLED = 23
    MOD_FALLING = 6
    MOD_SUICIDE = 7
    MOD_TRIGGER_HURT = 9
    UT_MOD_SMITED = 33
    UT_MOD_KNIFE_THROWN = 13
    UT_MOD_FLAG = 47

class UTGearItems(enum.Enum):
    Helmet = "W"
    SmokeGrenade = "Q"
    TacticalGoggles	= "S"
    KevlarVest = "R"
    Negev = "c"
    
class UTMsgType(enum.Enum):
    InitGame = 0
    Exit = 1
    ClientUserinfo = 2
    ClientDisconnect = 3
    Hit = 4
    Kill = 5
    say = 6
   