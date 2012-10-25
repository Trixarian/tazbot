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
def msg_parse(dest, nick, cmd, args, pvt_msg=0):
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
				ircbot.msg(dest, "New response learned for %s" % key)
			except: ircbot.msg(dest, "Sorry, I couldn't learn that!")
		else: ircbot.msg(dest, "Sorry %s, only my masters can teach me!" % nick)

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
					ircbot.msg(dest, "I've forgotten %s" % key)
				except: ircbot.msg(dest, "Sorry, I couldn't forget that!")
			else: ircbot.msg(dest, "You have to teach me something before you can make me forget it!")
		else: ircbot.msg(dest, "Sorry %s, only my masters can make me forget!" % nick)

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
		else: ircbot.msg(dest, "I don't know anything yet!")

	if cmd == "!responses":
		iscmd = 1
		if os.path.isfile("qdb.dat"):
			rcount = 0
			file = open("qdb.dat")
			for line in file.readlines():
				if line is "": pass
				else: rcount = rcount+1
			file.close()
			if rcount < 1: ircbot.msg(dest, "I've learned no responses")
			elif rcount == 1: ircbot.msg(dest, "I've learned %d responses" % rcount)
			else: ircbot.msg(dest, "I've learned %d responses" % rcount)
		else: ircbot.msg(dest, "I don't know anything yet!")

	if cmd == "!quit":
		iscmd = 1
		if nick in ircbot.BOTMASTERS:
			ircbot.quit()

	base_key = ("%s %s" % (cmd, ' '.join(args[0:]))).strip()
	if ircbot.NICK.lower() in base_key.lower() or pvt_msg:
		if "help" in base_key.lower(): 
			msg = ircbot.HELP.replace("#botnick", ircbot.NICK)
			msg = msg.replace("#nick", nick)
			ircbot.msg(dest, msg)
		elif "topics" in base_key.lower():
			if os.path.isfile("qdb.dat"):
				topics = ""
				file = open("qdb.dat")
				for line in file.readlines():
					key = line.split(":=:")[0]
					if topics == "": topics = key
					else: topics = topics+", "+key
				file.close()
				ircbot.msg(dest, "Help topics: %s" % topics)
			else: ircbot.msg(dest, "I don't know anything yet!")
		else:
			try:
				reply = dbread(base_key)
				if reply:
					reply = reply.replace("#nick", nick)
					reply = botunfilter(reply)
					if reply[:1] == "+":
						ircbot.act(dest, "%s" % reply[1:])
					else:
						ircbot.msg(dest, "%s: %s" % (nick, reply))
				elif args[0] is not "":
					msg = ircbot.NOHELP.replace("#botnick", ircbot.NICK)
					msg = msg.replace("#nick", nick)
					if pvt_msg:
						ircbot.msg(dest, msg)
					else:
						if ircbot.NICK.lower() in cmd.lower():
							ircbot.msg(dest, msg)
				else: pass
			except: pass

	if pvt_msg:
		## Private Messages ##
		if cmd == "!join":
			if nick in ircbot.BOTMASTERS:
				try:
					ircbot.join(args[0])
					ircbot.msg(dest, "Joining %s" % args[0])
				except: ircbot.msg(nick, "Error joining channel!")

		if cmd == "!part":
			if nick in ircbot.BOTMASTERS:
				try:
					ircbot.part(args[0])
					ircbot.msg(dest, "Parting %s" % args[0])
				except: ircbot.msg(nick, "Error parting channel!")


if __name__ == '__main__':
	ircbot.loop()