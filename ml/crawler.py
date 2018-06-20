import dota2api
import time

def show_time(time):
	sec = 1
	min = 60*sec
	hour = 60*min
	if time > hour:
		hours = time / hour
		mins = (time % hour) / min
		print("%d hours and %d mins" % (hours, mins))
	elif time > min:
		mins = time / min
		secs = time % min
		print("%d mins and %d secs" % (mins, secs))
	else:
		secs = time
		print("%d secs" % secs)

def match_string(match):
	dire = []
	rad = []
	for player in match['players']:
		team = rad if player['player_slot'] < 100 else dire
		team.append(player['hero_id'])
	rad_wins = 1 if match['radiant_win'] else 0
	ret = '%d %d' % (match['match_id'], rad_wins)
	for hero in rad + dire:
		ret +=  ' %d' % hero
	ret += '\n'
	return ret

def is_valid_match(match):
	if not 'game_mode' in match: return False

	# 1=all pick, 2=captains mode, 3=random draft, 4=single draft, 5=all random, 16=captains draft, 22=ranked all pick
	if not match['game_mode'] in [1, 2, 3, 4, 5, 16, 22]: return False

	if not 'lobby_type' in match: return False

	# 0=Public Matchmaking, 7=Ranked Matchmaking
	if not match['lobby_type'] in [0, 7]: return False

	if not 'radiant_win' in match: return False

	for player in match['players']:
		if not 'leaver_status' in player: return False
		if not 'player_slot' in player: return False
		if player['leaver_status'] != 0: return False

	return True

file = open('dota_recent.txt', 'a')

id = 3954827880+1

begin = time.time()

time_limit = 24 * 60 * 60 * 1000

last_time = 0

api = dota2api.Initialise("27F135E2B03D83D8BFBD19E9A98DCD44")#, raw_mode=True)

i = 0

while True:
	id -= 1
	i += 1

	now = time.time()

	#if now - begin > time_limit: break
	if (now - last_time) <= 500: continue

	try:
		match = api.get_match_details(match_id=id)
	except:
		continue

	if not is_valid_match(match): continue

	print(str(id) + " : " + str(match['game_mode']))
	show_time(now - begin)

	dire = []
	rad = []

	for player in match['players']:
		team = rad if player['player_slot'] < 100 else dire
		team.append(player['hero_id'])

	rad_wins = 1 if match['radiant_win'] else 0

	file.write('%d %d %d' % (match['match_id'], rad_wins, match['game_mode']))
	for hero in rad + dire:
		file.write(' %d' % hero)
	file.write('\n')

file.close()
