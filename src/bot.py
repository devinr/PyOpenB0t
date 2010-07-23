#########################################################################
# PyOpenB0t - a port of WinOCM's OpenB0t to Python.                     #
# Copyright (c) 2010 Devin Ryan                                         #
#########################################################################
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#########################################################################

import sys
import socket
import string
import os
import time
from threading import Thread

# todo: replace this config with a Config() class for ease-of-use
NICK='PyOpenB0t'
NICKPASS=''
IDENT='openb0t'
FULLNAME='PyOpenB0t by Skynet'
SERVERS='tripcode:irc.tripco.de'		# Seperate each by a space.
										# Format: netname:server
CHANNELS='tripcode:#a'					# Seperate each by a space.
										# Format: netname:#channel
PREFIXCHARS='#'							# Seperate each by ...nothing. (example: #!)

# no need to modify anything below
_connected = 0
s = socket.socket()
_threadnum = 0

def dprint(x, y=0):
	print "[" + str(y) + "] " + x

def onConnect(netname):
	global s
	global NICKPASS
	global CHANNELS
	for a in NICKPASS.split():
		a = a.split(":")
		s.send("PRIVMSG NickServ :IDENTIFY " + a[1] + "\n")
	for a in CHANNELS.split():
		a = a.split(":")
		s.send("JOIN :" + a[1] + "\n")

def parse(line):
	global _connected
	global NICK
	global IDENT
	global FULLNAME
	global PREFIXCHARS
	if _connected:
		split = line.rstrip()
		split = split.split()
		nick = split[0]
		nick = nick[1:]
		ident = ''
		host = ''
		if not len(split) < 3:
			if nick.find("!") != -1:
				# it's a user, get their nick, ident, and host
				orig = nick
				loc = orig.find("!")
				nick = orig[:loc]
				origloc = loc
				loc = orig.find("@")
				ident = orig[origloc:loc]
				host = orig[loc:]
			command = split[3]
			command = command[1:]
			if command == '\x01VERSION\x01':
				# ctcp VERSION, reply appropriately
				s.send("PRIVMSG " + nick + " :\x01VERSION PyOpenB0t-devel by Skynet - a port of OpenB0t to Python\x01\n")
			if PREFIXCHARS.find(command[:1]) != -1:
				command = command[1:]
				#parse stuff here
				if command=='hello':
					s.send("PRIVMSG " + split[2] + " :Hello, " + nick + "!\n")
		elif not len(split) < 2:
			if split[1] == 'PING':
				# pong!
				s.send("PONG " + split[2] + "\n")
	elif line.find(":are supported by this server") != -1:
		_connected = 1
		
class pingSender:
	def run(self, a, t):
		while 1:
			dprint("Sending ping to network " + a[0] + " (" + a[1] + ")...", t)
			s.send("PING :" + a[1])
			dprint("Sleeping 15 seconds...", t)
			time.sleep(15)
class doServerConnect:
	def run(self, a, t):
		dprint("Connecting to " + a[0] + " (" + a[1] + ")...", t)
		s.connect((svrinfo[1], 6667))
		dprint("Sending nick and ident...", t)
		s.send("NICK " + NICK + "\n")
		s.send("USER " + IDENT + " 8 * :" + FULLNAME + "\n")
		pingSender().run(a, t)

for a in SERVERS.split():
	svrinfo = a.split(":")
	_threadnum = _threadnum + 1
	doServerConnect().run(svrinfo, _threadnum)
	
while 1:
	try:
		line = s.recv(4096)
		parse(line)
		line = line.split("\n")
		for a in line:
			if not a=='':
				dprint(a[1:], _threadnum)
	except KeyboardInterrupt:
		s.send("QUIT :Ctrl-C at console.\n")
		dprint("Ctrl-C detected, exiting.")
		quit()