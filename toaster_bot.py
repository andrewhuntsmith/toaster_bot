#toaster_bot.py


from irc import *
from time import sleep
import os
import random
import thread
import re
from config import *

state = 0		# 0 = normal, 1 = gathering votes
votingDict = {}


def voteTimer():
	sleep(20)
	state = 0
	irc.send(CHAN,"Voting has ended!")
	
def addGuess(user, guess):
	votingDict[user] = int(guess)
	print(votingDict)
	
def clearDict():
	votingDict.clear()

def tally(result):
	print("Tallying results")
	print(votingDict)
	closestUser = ""
	closestGuess = 999999
	for user in votingDict:
		guess = votingDict[user]
		if (abs(guess-result) < abs(closestGuess-result)):
			closestUser = user
			closestGuess = guess
	return [closestUser,closestGuess]

irc = IRC()
irc.connect(HOST,CHAN,NICK,PASS)

while 1:
	text = irc.get_text()
	print text
	
	if "PRIVMSG" in text and CHAN in text:
		sender = text.split("!")[0].split(":")[1]
		message = text.split(":")[2]
		#print(sender)
		#print(message)
		if sender == 'xandotoaster':
			if "!" in message:
				command = message.split("!")[1]
				if command == "initGuess\r\n":
					state = 1
					#print(state)
					irc.send(CHAN,"Voting has begun! Votes should look like: '!vote 123'")
					thread.start_new_thread(voteTimer, ())
					
				if command == "result\r\n":
					state = 0
					result = re.findall(r"[0-9]+",command)[0]
					print(result)
					winner = tally(int(result))
					irc.send(CHAN,"The results are in! The winner is " + winner[0] + " with a guess of " + str(winner[1]) +"!")
					clearDict()
					print(votingDict)
					
			
			
		if "!guess" in message and state != 0:
			guess = message.split(" ")[1]
			addGuess(sender,guess)
			irc.send(CHAN,sender + " has guessed " + guess)
		if "!guess" in message and state == 0:
			irc.send(CHAN,"Sorry, " + sender + ", but there is no vote right now")
			
	sleep(1.5)
	