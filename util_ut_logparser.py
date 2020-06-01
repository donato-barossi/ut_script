import os
import re
from cfg_ut_const import UTMsgType

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)s %(message)s",
                    filename='logs/app.log', filemode='w')


class UtLogParser:
    def __init__(self):
        self.line = ''
        self.data = {}

    def parse(self, line):
        self.line = line
        msgtype = self.__get_cmd_type__()
        if msgtype: 
            switch = {
                UTMsgType.InitGame.value: self.__get_game_info__,
                UTMsgType.Exit.value : self.__get_game_over__,
                UTMsgType.ClientUserinfo : self.__get_client_info__,
                UTMsgType.ClientDisconnect : self.__get_client_disconnected__,
                UTMsgType.Hit : self.__get_hit_info__,
                UTMsgType.Kill : self.__get_kill_info__,
                UTMsgType.say : self.__get_user_msg__,
            }
            logging.info(UTMsgType[msgtype])
            logging.info(UTMsgType[msgtype].value)
            switch.get(UTMsgType[msgtype].value, None)
            self.data['TYPE'] = UTMsgType[msgtype].value
            return self.data
        else:
            return None

    def __get_cmd_type__ (self):
        regex = r"\d+\:\d+\ (?P<cmdtype>[a-zA-Z]+)"
        res = re.search(regex, self.line) 
        if res:
            return res.group('cmdtype')
        else:
            return None


    def __get_game_info__(self):
        regex = r"InitGame:\ .*g_gametype\\(?P<gametype>[^\\]*).*mapname\\(?P<mapname>[^\\]*)"
        res = re.search(regex, self.line) 
        self.data = {}
        if res:
            self.data['MAP'] = res.group('mapname')
            self.data['GAMETYPE'] = res.group('gametype')

    def __get_game_over__(self):
        #regex = r"Exit:\ Timelimit\ hit"
        self.data = {}

    def __get_client_info__(self):
        regex = r"ClientUserinfo:\ (?P<id>\d+).*name\\(?P<name>[^\\]*)(\\|$).*cl_guid\\(?P<guid>[^\\]*?)(\\|$).*weapmodes\\(?P<wpmode>[^\\]*?)(\\|$)"
        res = re.search(regex, self.line) 
        self.data = {}
        if res:
            self.data['ID'] = res.group('id')
            self.data['NAME'] = res.group('player')
            self.data['GUID'] = res.group('guid')
            self.data['WPMODE'] = res.group('wpmode')

    def __get_client_disconnected__(self):
        regex = r"ClientDisconnect:\ (?P<player>\d+)"
        res = re.search(regex, self.line) 
        self.data = {}
        if res:
            self.data['PLAYER_ID'] = res.group('player')

    def __get_hit_info__(self):
        regex = r"Hit:\ (?P<dead>\d+)\ (?P<player>\d+)\ (?P<where>\d+)\ (?P<gun>\d+)"
        res = re.search(regex, self.line) 
        self.data = {}
        if res:
            self.data['SHOOTER'] = res.group('player')
            self.data['HIT'] = res.group('dead')
            self.data['BODYPART'] = res.group('where')
            self.data['WEAPON'] = res.group('gun')


    def __get_kill_info__(self):
        regex = r"Kill:\ (?P<player>\d+)\ (?P<dead>\d+)\ (?P<mode>\d+)"
        res = re.search(regex, self.line) 
        self.data = {}
        if res:
            self.data['KILLER'] = res.group('player')
            self.data['DEAD'] = res.group('dead')
            self.data['HOW'] = res.group('mode')

    def __get_user_msg__(self):
        regex = r"say:\ (?P<player>\d+)[^:]*:\ !(?P<cmd>[^\ ]*)(\ (?P<msg>.*))*"
        res = re.search(regex, self.line) 
        self.data = {}
        if res:
            self.data['PLAYER'] = res.group('player')
            self.data['CMD'] = res.group('cmd')
            self.data['MSG'] = res.group('msg')