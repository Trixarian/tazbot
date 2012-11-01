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
## Splits the messages into chunks of 450 characters split by words ##
def word_wrap(msg):
	lines = []
	line = ""
	count = 0
	for word in msg.split():
		line = line+word+" "
		count = count+1
		if (len(line)+len(word)) > 450:
			lines.append(line)
			line = ""
		elif count == len(msg.split()) and line is not "":
			lines.append(line.strip())
	return lines

## Sends to the IRC socket with the cartrige return and newline added ##
def send(msg):
	sock.send("%s\r\n" % msg)

## Wrappers to make using this bot easier ###
def msg(target, msg):
	for line in word_wrap(msg):
		send("PRIVMSG %s :%s" % (target, line.strip())) 

def notice(target, msg):
	for line in word_wrap(msg):
		send("NOTICE %s :%s" % (target, line.strip()))

def act(target, msg):
	for line in word_wrap(msg):
		send("PRIVMSG %s :\001ACTION %s\001" % (target, line.strip()))

def ctcp(target, msg):
	pass

def join(target):
	send("JOIN %s" % target)

def part(target):
	send("PART %s" % target)

def quit():
	global running, sock
	send("QUIT :%s" % readconf("QUITMSG"))
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
		msg = readconf("ONJOIN").replace("#botnick", BOTNICK)
		msg = msg.replace("#nick", nick)
		notice(nick, msg)

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
			main.msg_parse(chan, nick, cmd, args)
		else:
			main.msg_parse(nick, nick, cmd, args, 1)

def loop():
	global sock, running, BOTNICK, CHANNELS
	running = True
	buffer = ""
	SERVER = readconf("SERVER")
	PORT = int(readconf("PORT"))
	BOTNICK = readconf("NICK")
	IDENT = readconf("IDENT")
	REALNAME = readconf("REALNAME")
	CHANNELS = str(readconf("CHANNELS")).split()

	## Connect to IRC ##
	sock=socket.socket()
	sock.connect((SERVER, PORT))
	send("NICK %s" % BOTNICK)
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