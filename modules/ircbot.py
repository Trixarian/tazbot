#######################################
# TazBot v1.0
# By Brenton Edgar Scott
# Released under the CC0 License
#######################################
import socket, re, sys, os
import tazbot as main

#################
# Conf Function #
#################
def readconf(target):
	infile = open(os.getcwd() + "/tazbot.conf")
	while infile:
		line = infile.readline()
		## Checks if the line isn't the End of File, a comment or a empty line ##
		if line != "" and "=" in line:
			if target in line:
				returnline = ''.join(line.split(" = ")[1])
				break
		if line == "": break
	else: infile.close()

	if returnline: return eval(returnline)

####################
# IRCBot Framework #
####################
## Sends to the IRC socket with the cartrige return and newline added ##
def send(msg):
	sock.send("%s\r\n" % msg)

## Wrappers to make using this bot easier ###
def msg(target, msg):
	send("PRIVMSG %s :%s" % (target, msg)) 

def notice(target, msg):
	send("NOTICE %s :%s" % (target, msg))

def act(target, msg):
	send("PRIVMSG %s :\001ACTION %s\001" % (target, msg))

def join(target):
	send("JOIN %s" % target)

def part(target):
	send("PART %s" % target)

def quit():
	global running, sock
	send("QUIT :Bye :(")
	running = False
	sock.close()
	sys.exit(0)

def rclean(msg):
	# Strips out characters that we don't want
	msg = re.sub("\003([0-9][0-9]?(,[0-9][0-9]?)?)?|[^\x20-\x7E]","", msg)
	return msg

def clean(msg):
	msg = msg.rstrip()
	msg = rclean(msg[:1].replace(":","")+msg[1:])
	msg = msg.split()
	return msg

## Grabs the nickname out of the IRC Raw messages ##
def getnick(s):
	s = s.split("!")
	s = s[0]
	if s != '':
		return s

def parse(msg):
	## This keeps us connected to the IRC server ##
	if msg[0] == "PING":
		send("PONG %s" % msg[1])

	## This controls what happens once the bot is connected ##
	if msg[1] == "005":
		for x in CHANNELS:
			if x is "": pass
			else: join(x)
	if msg[1] == "JOIN":
		nick = getnick(msg[0])
		notice(nick, "Hey %s, I can answer your questions. Type \"TazBot: help\" to learn how to use me!" % nick)

	if msg[1] == "PRIVMSG":
		chan = msg[2]
		nick = getnick(msg[0])
		try:
			cmd = msg[3].strip(":")
			args = msg[4:]
		except:
			cmd = ""
			args = ""
		if chan[:1] == "#":
			main.chan_parse(chan, nick, cmd, args)
		else:
			main.prvt_parse(nick, cmd, args)

def loop():
	global sock, running, NICK, CHANNELS, BOTMASTERS
	running = True
	buffer = ""
	BOTMASTERS = readconf("BOTMASTERS")
	SERVER = readconf("SERVER")
	PORT = int(readconf("PORT"))
	NICK = readconf("NICK")
	IDENT = readconf("IDENT")
	REALNAME = readconf("REALNAME")
	CHANNELS = str(readconf("CHANNELS")).split()

	## Connect to IRC ##
	sock=socket.socket()
	sock.connect((SERVER, PORT))
	send("NICK %s" % NICK)
	send("USER %s %s 0 :%s" % (IDENT, SERVER, REALNAME))

	## Checking the buffer for new data from the socket ##
	while running:
		buffer = buffer + sock.recv(1024)
		temp = buffer.split("\n")
		buffer = temp.pop()

		for line in temp:
			parse(clean(line))

	## Closing the socket and exiting the program ##
	sock.close()
	sys.exit(0)