import logging
import time
import traceback
import cfg_server_config as cfg
import util_file_reader as reader
import ut_fun_msg as funMessages
import ut_cmd as commands
import util_ut_logparser as logparser
from cfg_ut_const import UTMsgType
from ut_server import UTServer


logging.basicConfig(level=logging.info, format="%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)s %(message)s",
                    filename='logs/app.log', filemode='w')


class App:
    def __init__(self):
        self.utLogParse = logparser.UtLogParser()
        self.reader = reader.FileReader()
        self.running = False
        self.server = UTServer()
        self.switch = {
            UTMsgType.InitGame.value: self.__init_game__,
            UTMsgType.Exit.value: self.__game_over__,
            UTMsgType.ClientUserinfo: self.__update_user_info__,
            UTMsgType.ClientDisconnect: self.__user_disconnected__,
            UTMsgType.Hit: self.__update_hit_stats__,
            UTMsgType.Kill: self.__update_kill_stats__,
            UTMsgType.say: self.__run_user_command__,
        }
        self.exit_status = 0

    def run(self):
        self.running = True
        while self.running:
            try:
                for line in self.reader.getNewLines():
                    _type = self.utLogParse.parse(line)
                    logging.info(_type)
                    logging.info(self.utLogParse.data)
                    self.switch.get(int(_type), None)
            except OSError:
                logging.error("No logs file found!")
            except Exception:
                logging.error("An error occurred while elaborating this line: [%s]" % line)
                track = traceback.format_exc()
                logging.error(track)
            time.sleep(cfg.TSleep)
        return self.exit_status

    def __init_game__(self):
        logging.info(
            "Removing current map [%s] from map list" % self.utLogParse.data['MAP'])
        self.server.removeMap(self.utLogParse.data['MAP'])
        if len(self.server.maps) == 0:
            self.server.loadMapsFromFile()
        time.sleep(15)
        map = self.server.getRandomMap()
        self.server.socket.nextMap(map)

    def __game_over__(self):
        self.server.resetPlayersStats()

    def __update_user_info__(self):
        logging.info('Update user [%s - %s - %s - %s]' % (self.utLogParse.data['ID'],
                                                           self.utLogParse.data['GUID'], self.utLogParse.data['NAME'], self.utLogParse.data['WPMODE']))
        self.server.updatePlayer(
            self.utLogParse.data['ID'], self.utLogParse.data['GUID'], self.utLogParse.data['NAME'], self.utLogParse.data['WPMODE'])

    def __user_disconnected__(self):
        logging.info('Player disconnected [%s]' % self.utLogParse.data['PLAYER'])
        self.server.playerDisconnected(self.utLogParse.data['PLAYER'])

    def __update_hit_stats__(self):
        logging.info('%s hits %s on %s with %s' % (
            self.utLogParse.data['SHOOTER'], self.utLogParse.data['HIT'], self.utLogParse.data['BODYPART'], self.utLogParse.data['WEAPON']))
        hs = self.server.updatePlayerHits(
            self.utLogParse.data['SHOOTER'], self.utLogParse.data['BODYPART'])
        self.server.sendFunMsg(funMessages.getHitMsg(
            int(self.utLogParse.data['BODYPART'])), self.utLogParse.data['HIT'])
        self.server.sendFunMsg(funMessages.getHSMsg(hs), self.utLogParse.data['SHOOTER'])

    def __update_kill_stats__(self):
        logging.info('%s kills %s. Mode: %s' % (
            self.utLogParse.data['KILLER'], self.utLogParse.data['DEAD'], self.utLogParse.data['HOW']))
        kills = self.server.updatePlayerKills(self.utLogParse.data['KILLER'])
        deaths = self.server.updatePlayerDead(self.utLogParse.data['DEAD'])
        self.server.sendFunMsg(funMessages.getKillMsg(
            int(self.utLogParse.data['HOW'])), self.utLogParse.data['DEAD'])
        self.server.sendFunMsg(
            funMessages.getKillStreakMsg(kills), self.utLogParse.data['KILLER'])
        self.server.sendFunMsg(
            funMessages.getSeriesOfDeadMsg(deaths), self.utLogParse.data['DEAD'])
        killer = self.server.getPlayerById(self.utLogParse.data['KILLER'])
        if killer:
            self.server.sendFunMsg(funMessages.getFunKillMessage(
                killer.guid, int(self.utLogParse.data['HOW'])), self.utLogParse.data['DEAD'])
        dead = self.server.getPlayerById(self.utLogParse.data['DEAD'])
        if dead:
            self.server.sendFunMsg(funMessages.getFunDeadMessage(
                dead.giud, int(self.utLogParse.data['HOW'])))
        self.server.printPlayerStats(self.utLogParse.data['KILLER'])

    def __run_user_command__(self):
        logging.info('%s send command %s %s' %
                      (self.utLogParse.data['PLAYER'], self.utLogParse.data['CMD'], self.utLogParse.data['MSG']))
        player = self.server.getPlayerById(self.utLogParse.data['PLAYER'])
        if player and commands.isAuthorized(player, self.utLogParse.data['CMD']):
            cmd = commands.getUserCommand(self.utLogParse.data['CMD'])
            if cmd:
                self.server.sendCmd(cmd % self.utLogParse.data['MSG'])
            elif self.utLogParse.data['CMD'] in commands.AppCmds:
                self.running = False
                self.exit_status = commands.AppCmds[self.utLogParse.data['CMD']].value
        elif player:
            self.server.say(commands.NotAuthorizedMsg % player.name)


def main():
    process = App()
    appmenu = {
        commands.AppCmds['restart']: __restart__,
        commands.AppCmds['pause']: __pause__,
        commands.AppCmds['resume']:  __resume__
    }

    status = process.run()
    while status > 0:
        process = appmenu.get(status, process)
        status = process.run()


def __restart__():
    #del process
    return App()


def __pause__():
    try:
        time.sleep(30)
    except Exception as e:
        logging.error(e)


def __resume__(process):
    # TODO
    logging.warning('Functionality not yet implemented!')


main()
