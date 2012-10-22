#!/usr/bin/python
#######################################
# Tazbot v1.0
# By Brenton Edgar Scott
# Released under the CC0 License
#######################################
import ircbot, sys, fileinput, os, re, random

#####################
# Replacement fixes #
#####################
def botfilter(msg):
	msg = msg.replace("||", "$C4")
	msg = msg.replace("|-:", "$b7")
	msg = msg.replace(":-|", "$b6")
	msg = msg.replace(";-|", "$b5")
	msg = msg.replace("|:", "$b4")
	msg = msg.replace(";|", "$b3")
	msg = msg.replace("=|", "$b2")
	msg = msg.replace(":|", "$b1")
	return msg

def botunfilter(msg):
	msg = msg.replace("$C4", "||")
	msg = msg.replace("$b7", "|-:")
	msg = msg.replace("$b6", ";-|")
	msg = msg.replace("$b5", ":-|")
	msg = msg.replace("$b4", "|:")
	msg = msg.replace("$b3", ";|")
	msg = msg.replace("$b2", "=|")
	msg = msg.replace("$b1", ":|")
	return msg

#####################
# QBot db functions #
#####################
def dbread(key):
	value = None
	if os.path.isfile("qdb.dat"):
		file = open("qdb.dat")
		for line in file.readlines():
			reps = int(len(line.split(":=:"))-1)
			data = line.split(":=:")[0]
			data2 = r'\b%s[a-z]{,4}\b' % data.replace("+","\+")
			key2 = r'\b%s[a-z]{,4}\b' % key.replace("+","\+")
			if re.search(key2, data, re.IGNORECASE) or re.search(data2, key, re.IGNORECASE):
				if key is "":
					value = None
					break
				else:
					if reps > 1:
						repnum = random.randint(1, int(reps))
						try: value = int(line.split(":=:")[repnum].strip())
						except ValueError, err: value = line.split(":=:")[repnum].strip()
					else:
						try: value = int(line.split(":=:")[1].strip())
						except ValueError, err: value = line.split(":=:")[1].strip()
					break
		file.close()
	return value

def dbwrite(key, value):
	if dbread(key) is None:
		file = open("qdb.dat", "a")
		file.write(str(key)+":=:"+str(value)+"\n")
		file.close()

	else:
		for line in fileinput.input("qdb.dat",inplace=1):
			data = line.split(":=:")[0]
			data2 = r'\b%s\b' % data.replace("+","\+")
			key2 = r'\b%s\b' % key.replace("+","\+")
			if re.search(key2, data, re.IGNORECASE) or re.search(data2, key, re.IGNORECASE):
				print str(line.strip())+":=:"+str(value)
			else:
				print line.strip()

#################
# QBot's parser #
#################
def chan_parse(chan, nick, cmd, args):
	if cmd == "!teach" or cmd == "!learn":
		iscmd = 1
		if nick in ircbot.BOTMASTERS:
			try:
				doesschool = ' '.join(args[0:])
				key = doesschool.split("|")[0].strip()
				rnum = int(len(doesschool.split("|"))-1)
				if rnum > 1: 
					array = doesschool.split("|")
					rcount = 1
					for value in array:
						if rcount == 1:	rcount = rcount+1
						else: dbwrite(key[0:], botfilter(value[0:].strip()))
				else:
					value = doesschool.split("|")[1].strip()
					dbwrite(key[0:], botfilter(value[0:]))
				ircbot.msg(chan, "New response learned for %s" % key)
			except: ircbot.msg(chan, "Sorry, I couldn't learn that!")
		else: ircbot.msg(chan, "Sorry %s, only my masters can teach me!" % nick)

	if cmd == "!forget":
		iscmd = 1
		if nick in ircbot.BOTMASTERS:
			key = ' '.join(args[0:]).strip()
			if os.path.isfile("qdb.dat"):
				try:
					for line in fileinput.input("qdb.dat", inplace =1):
						data = line.split(":=:")[0]
						data2 = r'\b%s\b' % data.replace("+","\+")
						key2 = r'\b%s\b' % key.replace("+","\+")
						if re.search(key2, data, re.IGNORECASE) or re.search(data2, key, re.IGNORECASE):
							pass
						else: print line.strip()
					ircbot.msg(chan, "I've forgotten %s" % key)
				except: ircbot.msg(chan, "Sorry, I couldn't forget that!")
			else: ircbot.msg(chan, "You have to teach me something before you can make me forget it!")
		else: ircbot.msg(chan, "Sorry %s, only my masters can make me forget!" % nick)

	if cmd == "!find":
		iscmd = 1
		key = ' '.join(args[0:]).strip()
		if os.path.isfile("qdb.dat"):
			rcount = 0
			matches = ""
			file = open("qdb.dat")
			for line in file.readlines():
				data = line.split(":=:")[0]
				data2 = r'\b%s[a-z]{,4}\b' % data.replace("+","\+")
				key2 = r'\b%s[a-z]{,4}\b' % key.replace("+","\+")
				if re.search(key2, data, re.IGNORECASE) or re.search(data2, key, re.IGNORECASE):
					if key.lower() is "": pass
					else:
						rcount = rcount+1
						if matches == "": matches = data
						else: matches = matches+", "+data
			file.close()
			if rcount < 1: msg = "I have no match for %s" % key
			elif rcount == 1: msg = "I found 1 match: %s" % matches
			else: msg = "I found %d matches: %s" % (rcount, matches)
		else: ircbot.msg(chan, "I don't know anything yet!")

	if cmd == "!responses":
		iscmd = 1
		if os.path.isfile("qdb.dat"):
			rcount = 0
			file = open("qdb.dat")
			for line in file.readlines():
				if line is "": pass
				else: rcount = rcount+1
			file.close()
			if rcount < 1: ircbot.msg(chan, "I've learned no responses")
			elif rcount == 1: ircbot.msg(chan, "I've learned %d responses" % rcount)
			else: ircbot.msg(chan, "I've learned %d responses" % rcount)
		else: ircbot.msg(chan, "I don't know anything yet!")

	if cmd == "!quit":
		iscmd = 1
		if nick in ircbot.BOTMASTERS:
			ircbot.quit()

	if ircbot.NICK.lower() in cmd.lower():
		if "help" in (' '.join(args[0:]).lower()): 
			ircbot.msg(chan, "I can answer any question directed at me (by putting \"TazBot:\" before the question) that falls within my answers database (use \"TazBot: topics\" to see them). I can also answer questions containing topics (\"TazBot: How do I become root?\").")
		elif "topics" in (' '.join(args[0:]).lower()):
			if os.path.isfile("qdb.dat"):
				topics = ""
				file = open("qdb.dat")
				for line in file.readlines():
					key = line.split(":=:")[0]
					if topics == "": topics = key
					else: topics = topics+", "+key
				file.close()
				ircbot.msg(chan, "Help topics: %s" % topics)
			else: ircbot.msg(chan, "I don't know anything yet!")
		else:
			try:
				key = (' '.join(args[0:])).strip()
				reply = dbread(key)
				if reply:
					reply = reply.replace("#nick", nick)
					reply = botunfilter(reply)
					if reply[:1] == "+":
						ircbot.act(chan, "%s" % reply[1:])
					else:
						ircbot.msg(chan, "%s: %s" % (nick, reply))
				else: ircbot.msg(chan, "Sorry %s, I don't have an answer for that (yet)! Try searching the forums (http://forum.slitaz.org/search.php), IRC logs (http://irc.slitaz.org/search/), the documentation (http://doc.slitaz.org) and google for answers. If all else fails, ask on the forums and be patient!" % nick)
			except: pass

def prvt_parse(nick, cmd, args):
	## Private Messages ##
	if cmd == "!join":
		if nick in ircbot.BOTMASTERS:
			try:
				ircbot.join(args[0])
				ircbot.msg(nick, "Joining %s" % args[0])
			except: ircbot.msg(nick, "Error joining channel!")

	if cmd == "!part":
		if nick in ircbot.BOTMASTERS:
			try:
				ircbot.part(args[0])
				ircbot.msg(nick, "Parting %s" % args[0])
			except: ircbot.msg(nick, "Error parting channel!")

	if cmd == "!quit":
		if nick in ircbot.BOTMASTERS:
			ircbot.quit()

if __name__ == '__main__':
	ircbot.loop()