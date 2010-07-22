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
PREFIXCHAR='#'							# Seperate each by a space.

# no need to modify anything below
_connected = 0
s = socket.socket()

def dprint(x, y=0):
	print "[" + str(y) + "] " + x

def onConnect():
	global s
	global NICKPASS
	global CHANNELS
	if not NICKPASS=='':
		s.send("PRIVMSG NickServ :IDENTIFY " + NICKPASS + "\n")
	for a in CHANNELS.split():
		s.send("JOIN :" + a + "\n")

def parse(line):
	global _connected
	global NICK
	global IDENT
	global FULLNAME
	if _connected:
		split = line.rstrip()
		split = split.split()
		command = split[3]
		command = command[2:]
		#parse stuff here
	elif line.find(":End of /MOTD") != -1:
		_connected = 1
		onConnect()
		
for a in SERVERS.split():
	svrinfo = a.split(":")
	dprint("Connecting to " + svrinfo[0] + " (" + svrinfo[1] + ")...")
	s.connect((svrinfo[1], 6667))
	s.send("NICK " + NICK + "\n")
	s.send("USER " + IDENT + " 8 * :" + FULLNAME + "\n")
	
while 1:
	try:
		line = s.recv(4096)
		parse(line)
		line = line.split("\n")
		for a in line:
			if not a=='':
				dprint(a[1:])
	except KeyboardInterrupt:
		s.send("QUIT :Ctrl-C at console.\n")
		dprint("Ctrl-C detected, exiting.")
		quit()