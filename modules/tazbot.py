#!/usr/bin/python
#######################################
# Tazbot v2.0
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
			dlen = r'\b.{2,}\b'
			if re.search(dlen, key, re.IGNORECASE):
				if key.lower() in data.lower() or data.lower() in key.lower():
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
			else:
				value = None
				break
		file.close()
	return value

def dbwrite(key, value, add=0):
	if dbread(key) is None:
		file = open("qdb.dat", "a")
		file.write(str(key)+":=:"+str(value)+"\n")
		file.close()

	else:
		for line in fileinput.input("qdb.dat",inplace=1):
			data = line.split(":=:")[0]
			dlen = r'\b.{2,}\b'
			if re.search(dlen, key, re.IGNORECASE):			
				if key.lower() in data.lower() or data.lower() in key.lower():
					if add == 1: print str(line.strip())+":=:"+str(value)
					else: print str(key.strip())+":=:"+str(value)
				else: print line.strip()
			else: print line.strip()


###################
# Messages parser #
###################
def msg_parse(dest, nick, cmd, args, pvt_msg=0):

	if cmd[:1] == "!":
		if cmd == "!teach" or cmd == "!learn":
			if nick in ircbot.readconf("ADMIN"):
				try:
					data = ' '.join(args[0:])
					if "|" in data:
						key = data.split("|")[0].strip()
						rnum = int(len(data.split("|"))-1)
						if rnum >= 1: 
							array = data.split("|")
							skip = 0
							for value in array:
								if skip == 1: dbwrite(key[0:], botfilter(value[0:].strip()), 1)
								else: skip = skip+1
						ircbot.msg(dest, "New response(s) learned for \"%s\"" % key)
					else: ircbot.msg(dest, "Sorry, there's a syntax error in that command!")
				except: ircbot.msg(dest, "Sorry, I couldn't learn that!")
			else: ircbot.msg(dest, "Sorry %s, only my masters can teach me!" % nick)
			
		if cmd == "!reteach" or cmd == "!relearn":
			if nick in ircbot.readconf("ADMIN"):
				try:
					data = ' '.join(args[0:])
					if "|" in data:
						key = data.split("|")[0].strip()
						rnum = int(len(data.split("|"))-1)
						if rnum >= 1: 
							array = data.split("|")
							rcount = 0
							for value in array:
								if rcount == 1:
									dbwrite(key[0:], botfilter(value[0:]))
									rcount = rcount+1
								elif rcount > 1:
									dbwrite(key[0:], botfilter(value[0:].strip()), 1)
									rcount = rcount+1
								else:
									rcount = rcount+1
						if rcount > 1: ircbot.msg(dest, "Responses retaught for \"%s\"" % key)
						else: ircbot.msg(dest, "Response retaught for \"%s\"" % key)
					else: ircbot.msg(dest, "Sorry, there's a syntax error in that command!")
				except: ircbot.msg(dest, "Sorry, I couldn't relearn that!")
			else: ircbot.msg(dest, "Sorry %s, only my masters can reteach me!" % nick)

		if cmd == "!forget":
			if nick in ircbot.readconf("ADMIN"):
				key = ' '.join(args[0:]).strip()
				if os.path.isfile("qdb.dat"):
					try:
						for line in fileinput.input("qdb.dat", inplace =1):
							data = line.split(":=:")[0]
							dlen = r'\b.{2,}\b'
							if re.search(dlen, key, re.IGNORECASE):			
								if key.lower() in data.lower() or data.lower() in key.lower():
									pass
								else: print line.strip()
						ircbot.msg(dest, "I've forgotten \"%s\"" % key)
					except: ircbot.msg(dest, "Sorry, I couldn't forget that!")
				else: ircbot.msg(dest, "You have to teach me something before you can make me forget it!")
			else: ircbot.msg(dest, "Sorry %s, only my masters can make me forget!" % nick)

		if cmd == "!find" or cmd == "!search":
			key = ' '.join(args[0:]).strip()
			if os.path.isfile("qdb.dat"):
				rcount = 0
				matches = ""
				file = open("qdb.dat")
				for line in file.readlines():
					data = line.split(":=:")[0]
					dlen = r'\b.{2,}\b'
					if re.search(dlen, key, re.IGNORECASE):			
						if key.lower() in data.lower() or data.lower() in key.lower():
							if key.lower() == "": pass
							else:
								rcount = rcount+1
								if matches == "": matches = data
								else: matches = matches+", "+data
				file.close()
				if rcount < 1: msg = "I have no match for \"%s\"" % key
				elif rcount == 1: msg = "I found 1 match: %s" % matches
				else: msg = "I found %d matches: %s" % (rcount, matches)
			else: ircbot.msg(dest, "I don't know anything yet!")

		if cmd == "!nick":
			if nick in ircbot.readconf("ADMIN"):
				try: 
					ircbot.send("NICK %s" % args[0])
					ircbot.BOTNICK = args[0]
				except: ircbot.msg(nick, "Error changing nickname to %s!" % args[0])

		if cmd == "!join":
			if nick in ircbot.readconf("ADMIN"):
				try:
					ircbot.join(args[0])
					ircbot.msg(dest, "Joining %s" % args[0])
				except: ircbot.msg(nick, "Error joining %s!" % args[0])

		if cmd == "!part":
			if nick in ircbot.readconf("ADMIN"):
				try:
					ircbot.part(args[0])
					ircbot.msg(dest, "Parting %s" % args[0])
				except: ircbot.msg(nick, "Error parting %s!" % args[0])

		if cmd == "!quit":
			if nick in ircbot.readconf("ADMIN"):
				ircbot.quit()

	else:
		base_key = ("%s %s" % (cmd, ' '.join(args[0:]))).strip()
		if ircbot.BOTNICK.lower() in base_key.lower() or pvt_msg:
			if "help" in base_key.lower(): 
				msg = ircbot.readconf("HELP").replace("#botnick", ircbot.BOTNICK)
				msg = msg.replace("#nick", nick)
				ircbot.msg(dest, msg)
			elif "topic" in base_key.lower():
				if "about" not in base_key.lower() or "for" not in base_key.lower():
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
			# Couple of Easter eggs ;)
			elif "42" in base_key.lower(): 
				ircbot.msg(dest, "%s: It's the Answer to the Ultimate Question about Life, the Universe and Everything!" % nick)
			elif "overlord" in base_key.lower(): 
				ircbot.msg(dest, "BOW TO ME FOR I AM YOUR ROBOT OVERLORD!")
			elif "girls" in base_key.lower(): 
				ircbot.msg(dest, "All I know is that pankso owns all the girls...")
			elif "windows 8" in base_key.lower():
				ircbot.act(dest, "slaps %s" % nick)
				ircbot.msg(dest, "Don't use that bloat! Use a Real OS like SliTaz instead! :D")
			elif "xyzzy" in base_key.lower():
				ircbot.msg(dest, "Nothing Happens")
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
