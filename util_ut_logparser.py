import os
import re
from cfg_ut_const import UTMsgType

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)s %(message)s",
                    filename='logs/app.log', filemode='w')

currentLine = ''

def parse(line):
    global currentLine 
    currentLine = line
    regex = r"\d+\:\d+\ (?P<cmdtype>[a-zA-Z]+)"
    res = re.search(regex, line) 
    if res: 
        msgtype = res.group('cmdtype')
        logging.info("MSG TYPE:: %s" % msgtype)
        switch = {
            UTMsgType.InitGame.value: __get_game_info__,
            UTMsgType.Exit.value : __get_game_over__,
            UTMsgType.ClientUserinfo : __get_client_info__,
            UTMsgType.ClientDisconnect : __get_client_disconnected__,
            UTMsgType.Hit : __get_hit_info__,
            UTMsgType.Kill : __get_kill_info__,
            UTMsgType.say : __get_user_msg__,
        }
        logging.info(UTMsgType[msgtype])
        data = switch.get(UTMsgType[msgtype].value, None)
        data['TYPE'] = UTMsgType[msgtype].value
        return data
    else:
        return None

def __get_game_info__(line = currentLine):
    regex = r"InitGame:\ .*g_gametype\\(?P<gametype>[^\\]*).*mapname\\(?P<mapname>[^\\]*)"
    res = re.search(regex, line) 
    data = {}
    if res:
        data['MAP'] = res.group('mapname')
        data['GAMETYPE'] = res.group('gametype')
    return data

def __get_game_over__(line = currentLine):
    #regex = r"Exit:\ Timelimit\ hit"
    data = {}
    return data

def __get_client_info__(line = currentLine):
    regex = r"ClientUserinfo:\ (?P<id>\d+).*name\\(?P<name>[^\\]*)(\\|$).*cl_guid\\(?P<guid>[^\\]*?)(\\|$).*weapmodes\\(?P<wpmode>[^\\]*?)(\\|$)"
    res = re.search(regex, line) 
    data = {}
    if res:
        data['ID'] = res.group('id')
        data['NAME'] = res.group('player')
        data['GUID'] = res.group('guid')
        data['WPMODE'] = res.group('wpmode')
    return data

def __get_client_disconnected__(line = currentLine):
    regex = r"ClientDisconnect:\ (?P<player>\d+)"
    res = re.search(regex, line) 
    data = {}
    if res:
        data['PLAYER_ID'] = res.group('player')
    return data

def __get_hit_info__(line = currentLine):
    regex = r"Hit:\ (?P<dead>\d+)\ (?P<player>\d+)\ (?P<where>\d+)\ (?P<gun>\d+)"
    res = re.search(regex, line) 
    data = {}
    if res:
        data['SHOOTER'] = res.group('player')
        data['HIT'] = res.group('dead')
        data['BODYPART'] = res.group('where')
        data['WEAPON'] = res.group('gun')
    return data


def __get_kill_info__(line = currentLine):
    regex = r"Kill:\ (?P<player>\d+)\ (?P<dead>\d+)\ (?P<mode>\d+)"
    res = re.search(regex, line) 
    data = {}
    if res:
        data['KILLER'] = res.group('player')
        data['DEAD'] = res.group('dead')
        data['HOW'] = res.group('mode')
    return data

def __get_user_msg__(line = currentLine):
    regex = r"say:\ (?P<player>\d+)[^:]*:\ !(?P<cmd>[^\ ]*)(\ (?P<msg>.*))*"
    res = re.search(regex, line) 
    data = {}
    if res:
        data['PLAYER'] = res.group('player')
        data['CMD'] = res.group('cmd')
        data['MSG'] = res.group('msg')
    return data