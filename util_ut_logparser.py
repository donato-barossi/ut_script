import os
import re
from cfg_ut_const import UTMsgType

def parse(line):
    msgtype = line.split(':')[0]
    switch = {
        UTMsgType.InitGame.value: __get_game_info__(line),
        UTMsgType.Exit.value : __get_game_over__(line),
        UTMsgType.ClientUserinfo : __get_client_info__(line),
        UTMsgType.ClientDisconnect : __get_client_disconnected__(line),
        UTMsgType.Hit : __get_hit_info__(line),
        UTMsgType.Kill : __get_kill_info__(line),
        UTMsgType.say : __get_user_msg__(line),
    }

    data = switch.get(UTMsgType[msgtype].value, None)
    data['TYPE'] = UTMsgType[msgtype].value
    return data


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
    regex = r"ClientUserinfo:\ (?P<id>\d+).*name\\(?P<name>[^\\]*)(\\|$).*cl_guid\\(?P<guid>[^\\]*?)(\\|$).*weapmodes\\(?P<wpmode>[^\\]*?)(\\|$)"
    res = re.search(regex, line) 
    data = {}
    if res:
        data['ID'] = res.group('id')
        data['NAME'] = res.group('player')
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