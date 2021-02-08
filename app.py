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
        self.blockedPlayers = [] 
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
        logging.debug("Print all player stats")
        self.server.printAllStats()
        logging.debug("Reset all player stats")
        self.server.resetPlayersStats()
        logging.debug("Removing current map [%s] from map list" % data['MAP'])
        self.server.removeMap(data['MAP'])
        if len(self.server.maps) == 0:
            logging.debug("Loading map list")
            self.server.loadMapsFromFile()
        time.sleep(2)
        logging.debug("Getting random map")
        map = self.server.getRandomMap()
        logging.debug("Configuring %s as next map" % map.name)
        self.server.socket.nextMap(map)
        self.server.say("Next map: %s" % map.name)

    def __game_over__(self, data):
        #time.sleep(15)
        self.server.printAllStats()
        self.server.resetPlayersStats()

    def __update_user_info__(self, data):
        logging.debug('Update user [%s - %s - %s - %s]' % (data['ID'], data['GUID'], data['NAME'], data['WPMODE']))
        self.server.updatePlayer(data['ID'], data['GUID'], data['NAME'], data['WPMODE'], data['GEAR'], data['GUID'] in commands.ProtectedPlayers)
        self.server.sendFunMsg(funMessages.getFunGearMessage(data['GEAR']), data['ID'])

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
        kills = self.server.updatePlayerKills(data['KILLER'], data['DEAD'])
        deaths = self.server.updatePlayerDead(data['DEAD'], data['KILLER'])
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
        
        if player and commands.isAuthorized(player, data['CMD']) and player.guid not in self.blockedPlayers:
            cmd = commands.getServerCommand(data['CMD'])
            # commands to manage server
            if cmd:
                if cmd.startswith('g_gametype') and data['MSG'] in GameType.__dict__:
                    msg = GameType[data['MSG']].value
                else:
                    msg = data['MSG']
                target = self.server.getPlayerByName(msg)
                if target and target.isProtected:                   
                    self.server.sendFunMsg(commands.getProtectedPlayersMsg(), target._id)
                else: 
                    self.__send_cmd__(cmd, msg)
            # custom commands like protect, allow, deny
            elif data['CMD']  in commands.CustomComds:
                self.__exec_custom_command__(player, data['CMD'], data['MSG'])
            # commands to manage the app like stop, restart ...
            elif data['CMD'] in commands.AppCmds:
                self.running = False
                self.exit_status = commands.AppCmds[data['CMD']]
            # all other commands
            else:
                target = self.server.getPlayerByName(data['MSG'])
                if target and target.isProtected:                   
                    self.server.sendFunMsg(commands.getProtectedPlayersMsg(), target._id)
                elif target:
                    self.server.sendCmd(data['CMD'] + " " + target.name)
                else:
                    self.server.sendCmd(data['CMD'] + " " + data['MSG'])
        elif player:
            self.server.say(commands.getNotAuthorizedMsg() % player.name)

    def __exec_custom_command__ (self, player, cmd, data):
        if cmd == 'protection':
            data = data.split(' ')
            if len(data) == 2:
                target = self.server.getPlayerByName(data[1])
                if target and data[0] == 'on':
                    logging.debug('Adding protection to %s' % target.name)
                    target.isProtected = True
                elif target and data[0] == 'off':
                    logging.debug('Removing protection to %s' % target.name)
                    target.isProtected = False
        elif cmd == 'deny' or cmd == 'block':
            target = self.server.getPlayerByName(data)
            if target:
                logging.debug('Deny %s' % target.name)
                if target.guid not in self.blockedPlayers:
                    self.blockedPlayers.append(target.guid)
        elif cmd == 'allow':
            target = self.server.getPlayerByName(data)
            if target:
                logging.debug('Allow %s' % target.name)
                if target.guid in self.blockedPlayers:
                    self.blockedPlayers.remove(target.guid)
        elif cmd == 'kill':
            target = self.server.getPlayerByName(data)
            if target and not target.isProtected:
                logging.debug('Kill %s' % target.name)
                self.server.sendCmd("smite " + target.name)
            elif data == 'all':
                logging.debug('Kill all players')
                for user in self.server.players:
                    if user != player:
                        logging.debug('Kill %s' % user.name)
                        self.server.sendCmd("smite " + user.name)
        elif cmd == 'maplist':
            if data == 'reset':
                self.server.loadMapsFromFile()
            else:
                self.server.loadMapsFromFile('data/' + data + '.txt')
        elif cmd == 'ban':
            player = self.server.getPlayerByName(data)
            logging.debug('Banning %s (data=%s)' % player.name, data)
            if player:
                self.server.banPlayer(player)

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
