import logging
import time
import cfg_server_config as cfg
import util_file_reader as reader
import ut_fun_msg as funMessages
import ut_cmd as commands
from util_ut_logparser import parse as utLogParse
from cfg_ut_const import UTMsgType
from ut_server import UTServer


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)s %(message)s", filename='logs/app.log', filemode='w')

class App:
    def __init__(self):
        self.reader = reader.FileReader()
        self.running = False
        self.data = {}
        self.server = UTServer()
        self.switch = {
            UTMsgType.InitGame.value: self.__init_game__(),
            UTMsgType.Exit.value: self.__game_over__(),
            UTMsgType.ClientUserinfo: self.__update_user_info__(),
            UTMsgType.ClientDisconnect: self.__user_disconnected__(),
            UTMsgType.Hit: self.__update_hit_stats__(),
            UTMsgType.Kill: self.__update_kill_stats__(),
            UTMsgType.say: self.__run_user_command__(),
        }
        self.exit_status = 0

    def run(self):
        self.running = True
        while self.running:
            for line in self.reader.getNewLines():
                try:
                    self.data  = utLogParse(line)
                    print(self.data)
                    self.switch.get(self.data['TYPE'], None)
                except Exception as e:
                    logging.error("An error occurred while elaborating this line: [%s]" % line)
                    logging.error(e)
            time.sleep(cfg.TSleep)
        return self.exit_status

    def __init_game__ (self):
        logging.debug("Removing current map [%s] from map list" % self.data['MAP'])
        self.server.removeMap(self.data['MAP'])
        if len(self.server.maps) == 0:
            self.server.loadMapsFromFile()
        time.sleep(15)
        map = self.server.getRandomMap()
        self.server.socket.nextMap(map)

    def __game_over__ (self):
        self.server.resetPlayersStats()

    def __update_user_info__ (self):
        logging.debug('Update user [%s - %s - %s - %s]' % (self.data['ID'], self.data['GUID'], self.data['NAME'], self.data['WPMODE']))
        self.server.updatePlayer(self.data['ID'], self.data['GUID'], self.data['NAME'], self.data['WPMODE'])
    
    def __user_disconnected__ (self):
        logging.debug('Player disconnected [%s]' % self.data['PLAYER'])
        self.server.playerDisconnected(self.data['PLAYER'])
        
    def __update_hit_stats__ (self):
        logging.debug('%s hits %s on %s with %s' % (self.data['SHOOTER'], self.data['HIT'], self.data['BODYPART'], self.data['WEAPON']))
        hs = self.server.updatePlayerHits(self.data['SHOOTER'], self.data['BODYPART'])
        self.server.sendFunMsg(funMessages.getHitMsg(int(self.data['BODYPART'])), self.data['HIT'])
        self.server.sendFunMsg(funMessages.getHSMsg(hs), self.data['SHOOTER'])

    def __update_kill_stats__ (self):
        logging.debug('%s kills %s. Mode: %s' % (self.data['KILLER'], self.data['DEAD'], self.data['HOW']))
        kills = self.server.updatePlayerKills(self.data['KILLER'])
        deaths = self.server.updatePlayerDead(self.data['DEAD'])
        self.server.sendFunMsg(funMessages.getKillMsg(int(self.data['HOW'])), self.data['DEAD'])
        self.server.sendFunMsg(funMessages.getKillStreakMsg(kills), self.data['KILLER'])
        self.server.sendFunMsg(funMessages.getSeriesOfDeadMsg(deaths), self.data['DEAD'])
        killer = self.server.getPlayerById(self.data['KILLER'])
        if killer:
            self.server.sendFunMsg(funMessages.getFunKillMessage(killer.guid, int(self.data['HOW'])), self.data['DEAD'])
        dead = self.server.getPlayerById(self.data['DEAD'])
        if dead:
            self.server.sendFunMsg(funMessages.getFunDeadMessage(dead.giud, int(self.data['HOW'])))
        self.server.printPlayerStats(self.data['KILLER'])

    def __run_user_command__ (self):
        logging.debug('%s send command %s %s' % (self.data['PLAYER'], self.data['CMD'], self.data['MSG']))
        player = self.server.getPlayerById(self.data['PLAYER'])
        if player and commands.isAuthorized(player, self.data['CMD']):
            cmd = commands.getUserCommand(self.data['CMD'])
            if cmd:
                self.server.sendCmd(cmd % self.data['MSG'])
            elif self.data['CMD'] in commands.AppCmds:
                self.running = False
                self.exit_status = commands.AppCmds[self.data['CMD']].value
        elif player:
            self.server.say(commands.NotAuthorizedMsg % player.name)


def main():
    process = App()
    appmenu = {
        commands.AppCmds['restart'] : __restart__(process),
        commands.AppCmds['pause'] : __pause__(process),
        commands.AppCmds['resume'] : __resume__(process)
        }
    
    status = process.run()
    while status > 0 :
        process = appmenu.get(status, process)
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
    #TODO
    logging.warning('Functionality not yet implemented!')
    return process

main()