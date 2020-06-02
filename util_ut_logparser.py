import os
import re
import logging
from cfg_ut_const import UTMsgType



logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)s %(message)s",
                    filename='logs/app.log', filemode='w')


def __get_cmd_type__(line):
    regex = r"\d+\:\d+\ (?P<cmdtype>[a-zA-Z]+)"
    res = re.search(regex, line)
    if res:
        return res.group('cmdtype')
    else:
        return None


def __get_game_info__(line):
    regex = r"InitGame:\ .*g_gametype\\(?P<gametype>[^\\]*).*mapname\\(?P<mapname>[^\\]*)"
    res = re.search(regex, line)
    data = {}
    if res:
        data['MAP'] = res.group('mapname')
        data['GAMETYPE'] = res.group('gametype')
    return data


def __get_game_over__(line):
    #regex = r"Exit:\ Timelimit\ hit"
    data = {}
    return data


def __get_client_info__(line):
    regex = r"ClientUserinfo:\ (?P<id>\d+).*name\\(?P<name>[^\\]*)(\\|$).*cl_guid\\(?P<guid>[^\\]*?)(\\|$).*(weapmodes\\(?P<wpmode>[^\\]*?)(\\|$))*"
    res = re.search(regex, line)
    data = {}
    if res:
        data['ID'] = res.group('id')
        data['NAME'] = res.group('name')
        data['GUID'] = res.group('guid')
        data['WPMODE'] = res.group('wpmode')
    return data


def __get_client_disconnected__(line):
    regex = r"ClientDisconnect:\ (?P<player>\d+)"
    res = re.search(regex, line)
    data = {}
    if res:
        data['PLAYER_ID'] = res.group('player')
    return data


def __get_hit_info__(line):
    regex = r"Hit:\ (?P<dead>\d+)\ (?P<player>\d+)\ (?P<where>\d+)\ (?P<gun>\d+)"
    res = re.search(regex, line)
    data = {}
    if res:
        data['SHOOTER'] = res.group('player')
        data['HIT'] = res.group('dead')
        data['BODYPART'] = res.group('where')
        data['WEAPON'] = res.group('gun')
    return data


def __get_kill_info__(line):
    regex = r"Kill:\ (?P<player>\d+)\ (?P<dead>\d+)\ (?P<mode>\d+)"
    res = re.search(regex, line)
    data = {}
    if res:
        data['KILLER'] = res.group('player')
        data['DEAD'] = res.group('dead')
        data['HOW'] = res.group('mode')
    return data


def __get_user_msg__(line):
    regex = r"say:\ (?P<player>\d+)[^:]*:\ !(?P<cmd>[^\ ]*)(\ (?P<msg>.*))*"
    res = re.search(regex, line)
    data = {}
    if res:
        data['PLAYER'] = res.group('player')
        data['CMD'] = res.group('cmd')
        data['MSG'] = res.group('msg')
    return data


def parse(line):
    if line:
        logging.debug(line)
        msgtype = __get_cmd_type__(line)
        
        switch = {
            UTMsgType.InitGame.value : __get_game_info__,
            UTMsgType.Exit.value : __get_game_over__,
            UTMsgType.ClientUserinfo.value: __get_client_info__,
            UTMsgType.ClientDisconnect.value : __get_client_disconnected__,
            UTMsgType.Hit.value: __get_hit_info__,
            UTMsgType.Kill.value : __get_kill_info__,
            UTMsgType.say.value : __get_user_msg__,
        }

        if msgtype and msgtype in UTMsgType.__dict__:
            funct = switch.get(int(UTMsgType[msgtype].value), None)
            if funct:
                data = funct(line)
                if data:
                    data['TYPE'] = UTMsgType[msgtype].value
                logging.debug(data)
                return data

    return None
