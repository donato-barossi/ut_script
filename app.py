import logging
import time
import traceback
import cfg_server_config as cfg
import util_file_reader as reader
import ut_fun_msg as funMessages
import ut_cmd as commands
from util_ut_logparser import parse as utLogParse
from cfg_ut_const import UTMsgType
from cfg_ut_const import Body
from cfg_ut_const import GameType
from ut_server import UTServer



logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)s %(message)s",
                    filename='logs/app.log', filemode='w')


class App:
    def __init__(self):
        self.reader = reader.FileReader()
        self.running = False
        self.server = UTServer()
        self.switch = {
            UTMsgType.InitGame.value: self.__init_game__,
            UTMsgType.Exit.value: self.__game_over__,
            UTMsgType.ClientUserinfo.value: self.__update_user_info__,
            UTMsgType.ClientDisconnect.value: self.__user_disconnected__,
            UTMsgType.Hit.value: self.__update_hit_stats__,
            UTMsgType.Kill.value: self.__update_kill_stats__,
            UTMsgType.say.value: self.__run_user_command__,
        }
        self.exit_status = 0
        self.server.say("Funny script initialized!")

    def run(self):
        self.running = True
        while self.running:
            try:
                for line in self.reader.getNewLines():
                    data = utLogParse(line)
                    logging.debug(data)
                    if data:   
                        funct = self.switch.get(data['TYPE'], None)
                        if funct:
                            funct(data)
            except OSError:
                logging.error("No logs file found!")
            except Exception:
                logging.error("An error occurred while elaborating this line: [%s]" % line)
                track = traceback.format_exc()
                logging.error(track)
            time.sleep(cfg.TSleep)
        return self.exit_status

    def __init_game__(self, data):
        logging.debug("Removing current map [%s] from map list" % data['MAP'])
        self.server.resetPlayersStats()
        self.server.removeMap(data['MAP'])
        if len(self.server.maps) == 0:
            self.server.loadMapsFromFile()
        time.sleep(15)
        map = self.server.getRandomMap()
        self.server.socket.nextMap(map)

    def __game_over__(self, data):
        self.server.resetPlayersStats()

    def __update_user_info__(self, data):
        logging.debug('Update user [%s - %s - %s - %s]' % (data['ID'], data['GUID'], data['NAME'], data['WPMODE']))
        self.server.updatePlayer(data['ID'], data['GUID'], data['NAME'], data['WPMODE'])

    def __user_disconnected__(self, data):
        logging.debug('Player disconnected [%s]' % data['PLAYER_ID'])
        self.server.playerDisconnected(data['PLAYER_ID'])

    def __update_hit_stats__(self, data):
        logging.debug('%s hits %s on %s with %s' % (data['SHOOTER'], data['HIT'], data['BODYPART'], data['WEAPON']))
        hs = self.server.updatePlayerHits(data['SHOOTER'], data['BODYPART'])
        self.server.sendFunMsg(funMessages.getHitMsg(int(data['BODYPART'])), data['HIT'])
        if int(data['BODYPART']) in [Body.Head.value, Body.Helmet.value]:
            self.server.sendFunMsg(funMessages.getHSMsg(hs), data['SHOOTER'])

    def __update_kill_stats__(self, data):
        logging.debug('%s kills %s. Mode: %s' % (data['KILLER'], data['DEAD'], data['HOW']))
        kills = self.server.updatePlayerKills(data['KILLER'])
        deaths = self.server.updatePlayerDead(data['DEAD'])
        if self.server.sendFunMsg(funMessages.getKillMsg(int(data['HOW'])), data['DEAD']):
            time.sleep(cfg.MessageDelay)
        if self.server.sendFunMsg(funMessages.getKillStreakMsg(kills), data['KILLER']):
            time.sleep(cfg.MessageDelay)
        if self.server.sendFunMsg(funMessages.getSeriesOfDeadMsg(deaths), data['DEAD']):
            time.sleep(cfg.MessageDelay)
        killer = self.server.getPlayerById(data['KILLER'])
        if killer:
            self.server.sendFunMsg(funMessages.getFunKillMessage(killer.guid, int(data['HOW'])), data['DEAD'])
        dead = self.server.getPlayerById(data['DEAD'])
        if dead:
            self.server.sendFunMsg(funMessages.getFunDeadMessage(dead.guid, int(data['HOW'])))
        if data['KILLER'] != data['DEAD']:
            self.server.printPlayerStats(data['KILLER'])

    def __run_user_command__(self, data):
        logging.debug('%s send command %s %s' % (data['PLAYER'], data['CMD'], data['MSG']))
        player = self.server.getPlayerById(data['PLAYER'])
        if player and commands.isAuthorized(player, data['CMD']):
            cmd = commands.getUserCommand(data['CMD'])
            if cmd:
                if cmd == 'gametype' and data['MSG'] in GameType.__dict__:
                    data['MSG'] = GameType[data['MSG']].value
                self.__send_cmd__(cmd, data['MSG'])                
            elif data['CMD'] in commands.AppCmds:
                self.running = False
                self.exit_status = commands.AppCmds[data['CMD']]
            else:
                self.server.sendCmd(data['CMD'] + " " + data['MSG'])
        elif player:
            self.server.say(commands.NotAuthorizedMsg % player.name)

    def __send_cmd__ (self, cmd, data):
        if data:
            self.server.sendCmd(cmd % data)
        elif '%s' in cmd:
            self.server.sendCmd((cmd % '').strip())
        else:
            self.server.sendCmd(cmd)
    
    def __cycle_map__ (self, cmd, data):
        self.server.sendCmd(cmd)

def main():
    process = App()
    appmenu = {
        commands.AppCmds['restart']: __restart__,
        commands.AppCmds['pause']: __pause__,
        commands.AppCmds['resume']:  __resume__
    }

    status = process.run()
    while status > 0:
        function = appmenu.get(status, process)
        if function:
            process = function(process)
        status = process.run()


def __restart__(process):
    del process
    return App()


def __pause__(process):
    try:
        time.sleep(30)
    except Exception as e:
        logging.error(e)
    return process


def __resume__(process):
    # TODO
    logging.warning('Functionality not yet implemented!')
    return process


main()
