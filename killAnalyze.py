import pickle
import DownloadStats
from collections import Counter

#Functions
#Info Extraction Functions
def ExtractKillInfo(setData, gameInfo):
    "Returns a list containing kill objects when given a list of sets and game info"
    kills = []
    for s in setData:
        for game in s['games']:
            for player in s['games'][game]['players']:
                victim = player['playerId']
                victimChar = player['sCharacterId']
                killer = gameInfo[game]['p1'] if not gameInfo[game]['p1'] == victim else gameInfo[game]['p2']
                killerChar =  gameInfo[game]['p1Char'] if not gameInfo[game]['p1Char'] == victimChar else gameInfo[game]['p2Char']
                for stock in player['stocks']:
                    if not stock['frameEnd'] == 0 and not stock['moveLastHitBy'] == 0 and not stock['moveLastHitBy'] == 56:
                        kills.append(Kill(stock['moveLastHitBy'], killer, victim, killerChar, victimChar, stock['percent'], gameInfo[game]['stage']))
    return kills

#Satistics Functions
def AveragePerStage(kills):
    percents = {}
    for kill in kills:
        if not kill.stage in percents:
            percents[kill.stage] = [kill.percent]
        else:
            percents[kill.stage].append(kill.percent)
    for key in percents:
        percents[key] = int(round(sum(percents[key])/len(percents[key])))
    return percents

def MovePerPlayer(kills):
    moves = {}
    for kill in kills:
        if not kill.killer in moves:
            moves[kill.killer] = [kill.move]
        else:
            moves[kill.killer].append(kill.move)
    for player in moves:
        moves[player] = Counter(moves[player]).most_common(1)[0][0]
    return moves

def AveragePercentPerMovePerCharacter(char, kills):
    percents = {}
    for kill in kills:
        if kill.killerChar == char.title():
            if not kill.move in percents:
                percents[kill.move] = [kill.percent]
            else:
                percents[kill.move].append(kill.percent)
    for move in percents:
        percents[move] =  int(round(sum(percents[move])/len(percents[move])))
    return (char, percents)


#Classes
class Kill:
    def __init__(self, move, killer, victim, killerChar, victimChar, victimFinalPercent, stage):
        self.move = DownloadStats.ConvertMove(move)                                #Move used to kill
        self.killer = DownloadStats.ConvertPlayerId(killer)                             #Killer Player Tag
        self.victim = DownloadStats.ConvertPlayerId(victim)                            #Victim Player Tag    
        self.killerChar = DownloadStats.ConvertCharacter(killerChar)                    #Killer's Character
        self.victimChar = DownloadStats.ConvertCharacter(victimChar)                    #Victim's Character
        self.stage = DownloadStats.ConvertStage(stage)
        #self.victimPreHitPercent = CalculatePreHitPercent(move, killer, victimFinalPercent) #Victim's Percent Before Getting Hit
        ##Implement this later^^
        self.percent = victimFinalPercent
        
    def __str__(self):
        #"Returns the the kill in the format: KillerTag(KillerChar) killed Victim(VictimChar) at %___"
        s = "{}({}) killed {}({}) at %{} with {} on {}".format(self.killer, self.killerChar, self.victim, self.victimChar, self.percent, self.move, self.stage)
        return s 
    
#Main Function
def main():
    ggInfo = pickle.load(open('DownloadedInfo.pkl', 'rb'))
    kills = ExtractKillInfo(ggInfo[0], ggInfo[1]) #Get a list of all the kills in a list of sets
    #Calculate Stats
    PercentxStage = AveragePerStage(kills)
    MovexPlayer = MovePerPlayer(kills)
    PercentxMovexChar = AveragePercentPerMovePerCharacter('fox', kills)
    #Ouput Stats
    with open('kills.txt', 'w+b') as f:
        for kill in kills: 
            #print kill
            f.write(str(kill)+'\n')
    with open('stats.txt', 'w+b') as f:
        #print '\n\nAverage death percent per stage:'
        f.write('Average death percent per stage:\n')
        for stage in PercentxStage:
            #print '\t{0:>18}:  {1}%'.format(stage, PercentxStage[stage])
            f.write('\t{0:>18}:  {1}%\n'.format(stage, PercentxStage[stage]))
        #print '\n\nFavorite kill move per player:'
        f.write('\n\nFavorite kill move per player:\n')
        for player in MovexPlayer:
            #print '\t{0:>15}:  {1}'.format(player, MovexPlayer[player])
            f.write('\t{0:>15}:  {1}\n'.format(player, MovexPlayer[player]))
       #print '\n\nAverage kill percentage per move for: Fox'
        f.write('\n\nAverage kill percentage per move for: Fox\n')
        for move in PercentxMovexChar[1]:
            #print '\t{0:>13}:  {1}%'.format(move, PercentxMovexChar[1][move])
            f.write('\t{0:>13}:  {1}%\n'.format(move, PercentxMovexChar[1][move]))
    print '\n\nAll kills written to kills.txt & All sample stats written to stats.txt'        
    
if __name__ == "__main__":
    main()

