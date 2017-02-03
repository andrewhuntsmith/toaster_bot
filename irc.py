#irc.py

import socket
import sys
from time import sleep

class IRC:

	irc = socket.socket()
	
	def __init__(self):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = 6667
		
	def send(self, chan, msg):
		self.irc.send("PRIVMSG " + chan + " :" + msg + "\n")
	
	def connect (self, server, channel, nickname, oauth):
		print "connecting to: " + server
		self.irc.connect((server,self.port))
		self.irc.send("PASS " + oauth + "\r\n")
		#self.irc.send("USER " + nickname + " " + nickname + " " + nickname + " :Toastbot is here!\r\n")
		self.irc.send("NICK " + nickname + "\r\n")
		self.irc.send("JOIN " + channel + "\r\n")
		
	def get_text(self):
		text = self.irc.recv(2040)
		
		if text.find('PING') != -1:
			print(text)
			self.irc.send('PONG ' + text.split() [1] + '\r\n')
			print('PONG ' + text.split()[1])
			
		return text