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

################
# DB functions #
################
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
						array = line.split(":=:")
						count = 1
						for response in array:
							if count == 2: value = str(response.strip())
							elif count > 2: value = value+"\n"+str(response.strip())
							count = count+1
					else:
						value = str(line.split(":=:")[1].strip())
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


###################
# Messages parser #
###################
def msg_parse(dest, nick, cmd, args, pvt_msg=0):

	if cmd[:1] == "!":
		if cmd == "!teach":
			if nick in ircbot.readconf("BOTMASTERS"):
				try:
					data = ' '.join(args[0:])
					key = data.split("|")[0].strip()
					rnum = int(len(data.split("|"))-1)
					if rnum > 1: 
						array = data.split("|")
						rcount = 1
						for value in array:
							if rcount == 1:	rcount = rcount+1
							else: dbwrite(key[0:], botfilter(value[0:].strip()))
					else:
						value = data.split("|")[1].strip()
						dbwrite(key[0:], botfilter(value[0:]))
					ircbot.msg(dest, "New response learned for %s" % key)
				except: ircbot.msg(dest, "Sorry, I couldn't learn that!")
			else: ircbot.msg(dest, "Sorry %s, only my masters can teach me!" % nick)

		if cmd == "!forget":
			if nick in ircbot.readconf("BOTMASTERS"):
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

		if cmd == "!nick":
			if nick in ircbot.readconf("BOTMASTERS"):
				try: 
					ircbot.send("NICK %s" % args[0])
					ircbot.BOTNICK = args[0]
				except: ircbot.msg(nick, "Error changing nickname to %s!" % args[0])

		if cmd == "!join":
			if nick in ircbot.readconf("BOTMASTERS"):
				try:
					ircbot.join(args[0])
					ircbot.msg(dest, "Joining %s" % args[0])
				except: ircbot.msg(nick, "Error joining %s!" % args[0])

		if cmd == "!part":
			if nick in ircbot.readconf("BOTMASTERS"):
				try:
					ircbot.part(args[0])
					ircbot.msg(dest, "Parting %s" % args[0])
				except: ircbot.msg(nick, "Error parting %s!" % args[0])

		if cmd == "!quit":
			if nick in ircbot.readconf("BOTMASTERS"):
				ircbot.quit()

	else:
		base_key = ("%s %s" % (cmd, ' '.join(args[0:]))).strip()
		if ircbot.BOTNICK.lower() in base_key.lower() or pvt_msg:
			if "help" in base_key.lower(): 
				msg = ircbot.readconf("HELP").replace("#botnick", ircbot.BOTNICK)
				msg = msg.replace("#nick", nick)
				ircbot.msg(dest, msg)
			elif "topic" in base_key.lower():
				if os.path.isfile("qdb.dat"):
					topics = ""
					file = open("qdb.dat")
					for line in file.readlines():
						key = line.split(":=:")[0]
						if topics == "": topics = key
						else: topics = topics+", "+key
					file.close()
					ircbot.msg(dest, "Topics: %s" % topics)
				else: ircbot.msg(dest, "I don't know anything yet!")
			elif "version" in base_key.lower(): 
				ircbot.msg(dest, "TazBot 1.0 by Trixar_za: https://github.com/Trixarian/tazbot")
			elif "overlord" in base_key.lower(): 
				ircbot.msg(dest, "BOW TO ME FOR I AM YOUR ROBOT OVERLORD!")
			else:
				try:
					reply = dbread(base_key).split("\n")
					if reply:
						linecount = 1
						if len(reply) > int(ircbot.readconf("LINES")): dest = nick
						for line in reply:
							line = line.replace("#nick", nick)
							line = line.replace("#botnick", ircbot.BOTNICK)
							line = botunfilter(line)
							if line[:1] == "+":
								ircbot.act(dest, "%s" % line[1:])
							else:
								prefix_nick = bool(ircbot.readconf("PREFIX"))
								if prefix_nick and dest is not nick and linecount == 1:
									ircbot.msg(dest, "%s: %s" % (nick, line))
								else:
									ircbot.msg(dest, line)
							linecount = linecount+1
					elif args[0] is not "":
						msg = ircbot.readconf("NOHELP").replace("#botnick", ircbot.BOTNICK)
						msg = msg.replace("#nick", nick)
						if pvt_msg:
							ircbot.msg(dest, msg)
						else:
							if ircbot.BOTNICK.lower() in cmd.lower():
								ircbot.msg(dest, msg)
					else: pass
				except: pass


if __name__ == '__main__':
	ircbot.loop()