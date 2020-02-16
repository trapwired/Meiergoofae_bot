import sys
import time
import random
import datetime
import json
import telepot

chat_id_dict = {}
name_to_wait = -1

def getDict(dict):
	if dict:
		result = json.dumps(dict, indent = 4)
		return result
	else:
		return 'dict is empty'

def id_stored(chat_id, dict):
	for d in dict:
		if dict[d] == chat_id:
			return True
	return False

def get_name(chat_id, dict):
	for d in dict:
		if dict[d] == chat_id:
			return d
	return 'Name not found'

def handle(msg):
	global chat_id_dict, name_to_wait
	chat_id = msg['chat']['id']
	command = msg['text']
	command = command.lower()
	
	print 'Got command: %s (%s)' % (command, chat_id)

	if command == '/start':
		if not id_stored(chat_id, chat_id_dict):
			name_to_wait = chat_id
			bot.sendMessage(chat_id, 'What\'s your name?')
		else:
			bot.sendMessage(chat_id, 'Hi %s ;)' % get_name(chat_id, chat_id_dict))
	
	elif command == 'hello':
		bot.sendMessage(chat_id, 'hello back')
	elif command == 'time':
		bot.sendMessage(chat_id, str(datetime.datetime.now()))
	elif command == 'dict':
		bot.sendMessage(chat_id, getDict(chat_id_dict))
	elif command == 'send':
		zahl = random.randint(1,10)
		print(zahl)
		for i in range(1,zahl):
			bot.sendMessage(chat_id, 'Hello Domi')
	else:
		if chat_id == name_to_wait:
			chat_id_dict[command] = chat_id
			name = str(command)
			bot.sendMessage(chat_id, str('Hi ' + name + ' ;)'))
		else:
			bot.sendMessage(chat_id, command)

bot = telepot.Bot('1058220791:AAFQW9Cwaae0iNZkfOvzntvpSh3KzpDoSBw')
bot.message_loop(handle)
print 'I am listening'

while 1:
	time.sleep(10)


