#Imports
import urllib 
import json
import sys
import pickle
import re
import os


#Functions & Classes
#Misc. functions
def DownloadSetData(setNums):
	"Returns a list. Every item is a json dict containing info about a set"
	setJSONList = []
	for s in setNums:
		setJSON = json.loads(urllib.urlopen('https://api.smash.gg/slippi/getBySet/' + s).read())
		if 'games' in setJSON:
			setJSONList.append(setJSON)
		else:
			print  "There is no data for set #{}".format(s)
	return setJSONList

def DownloadPhaseData(phase):
	"Returns a list containing all the set #s in a smash.gg phase"
	return [str(s['id']) for s in json.loads(urllib.urlopen('https://api.smash.gg/phase_group/{}?expand[]=sets'.format(phase)).read())['entities']['sets']]



#Extract data from JSON
def ExtractPlayerIDs(set):
	"Pass in a set(json), returns list of playerIDs in the set"
	return [int(id) for id in set['summary']]

def ExtractGameInfo(setData):
	data = {}
	for s in setData:
		playerIdList = ExtractPlayerIDs(s)
		for game in s['games']:
			data[game] = {'stage' : s['games'][game]['stage'], 'p1' : playerIdList[0], 'p2' : playerIdList[1]}
			for player in s['games'][game]['players']:
				if player['playerId'] == playerIdList[0]:
					data[game]['p1Char'] = player['sCharacterId']
				else:
					data[game]['p2Char'] = player['sCharacterId']
	return data



#Convert/Analyze extracted data functions
def CalculatePreHitPercent(move, killer, victimFinalPercent):
	"Takes a move char and percent after hit and returns percent before hit"
	return None

def ConvertMove(id):
	idList = {1 : 'Turnip?', 2 : 'Jab 1', 3 : 'Jab 2', 4 : 'Jab 3', 6 : 'Dash Attack', 7: 'Ftilt', 8 : 'Utilt', 9 : 'Dtilt', 10 : 'Fsmash', 11 : 'Usmash', 12 : 'Dsmash', 13 : 'Nair', 14 : 'Fair', 15 : 'Bair', 16 : 'Uair', 17 : 'Dair', 18 : 'Nspecial', 19 : 'Fspecial', 20 : 'Uspecial', 21 : 'Dspecial', 50 : 'Get-up Attack', 52 : 'Dthrow', 53 : 'Fthrow', 54 : 'Bthrow', 55 : 'Uthrow'}
	return(idList[id])

def ConvertPlayerId(id):
	idList = {1012 : 'PewPewU', 1017 : 'S2J', 4465 : 'Leffen', 4101 : 'Infinite Numbers', 6189 : 'Armada', 13932 : 'Lucky', 1004 : 'Hungrybox', 1008 : 'Westballz', 1055 : 'Swedish Delight', 16342 : 'Axe', 1028 : 'Wizzrobe', 1037 : 'Duck', 1019 : 'SFAT', 4507 : 'The Moon', 4442 : 'Druggedfox', 1000 : 'Mang0', 15179 : 'ChuDat', 1003 : 'Mew2King', 1013 : 'Shroomed', 19573 : 'Ice', 1036 : 'HugS', 15990 : 'Plup'}
	return(idList[id])

def ConvertCharacter(id):
	idList = {0 : 'Captain Falcon', 2 : 'Fox', 7 : 'Luigi', 9 : 'Marth', 12 : 'Peach', 13 : 'Pikachu', 15 : 'Jigglypuff', 16 : 'Samus', 18 : 'Zelda', 19 : 'Sheik', 20 : 'Falco', 25 : 'Ganondorf', 14 : 'Ice Climbers'}
	return(idList[id])

def ConvertStage(id):
	idList = {2 : 'Fountain of Dreams', 3 : 'Pokemon Stadium', 8 : "Yoshi's Story", 28 : 'Dreamland', 31 : 'Battlefield', 32 : 'Final Destination'}
	return(idList[id])


#User Interaction Function:
def userInput():
	while True:
		resultType = raw_input("Set or Whole Bracket [s/b]? ")
		if resultType.lower() == 'b':
			print "\nTo get the correct link: go to the event's bracket. Near the top it says 'All Pools', change it to 'Bracket'.\n"
			inLink = raw_input('Paste the smash.gg bracket link: ')
			inLink = re.search(r'(?<=id%22%3A)(\d*)', inLink)
			try:
				setNums = DownloadPhaseData(inLink.group(1))
				print '\n\nDownloading stats for {} sets: {}\n\n'.format(len(setNums), setNums)
				break
			except:
				print('Bad Link\n')
				continue
		elif resultType.lower() == 's':
			print "\nTo get the correct link: go to a bracket and click on a set.\n"
			inLink = raw_input('Paste the smash.gg set link: ')
			inLink = re.search(r'(?<=/set/)(\d*)', inLink)
			setNums = [inLink.group(1)] 
			if not setNums:
				print ('Bad Link\n')
				continue
			print '\n\nDownloading stats for 1 set: {}\n\n'.format(setNums)
			break
		else:
			print "Please enter either s or b\n"
			continue
	return setNums

#Main
def main():
	setNums = userInput()
	setData = DownloadSetData(setNums)	#List containing all of the data about every set in setNums
	print "\nExtrating and Parsing. Please wait."
	gameInfo = ExtractGameInfo(setData)	#Takes a list of dicts with game info and returns a list of kills + info about kills
	with open('DownloadedInfo.pkl', 'w+b') as p:
		pickle.dump([setData, gameInfo], p, -1)
	print '\n\nDone'
	if (raw_input("\n\nDo you want to do extract kill statistics [y/n]? ")).lower() == 'y':
		os.system('python killAnalyze.py')
	return None

if __name__ == "__main__":
	main()
