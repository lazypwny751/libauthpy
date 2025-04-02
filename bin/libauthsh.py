#!/usr/bin/env python3

import os
import sys
import shlex
import libauth

rel = "0.0.1"

properties = {
	"database": None,
	"id": None
}

prompt = f"{os.path.basename(sys.argv[0])} shell[{rel}]:> "

class Shell:
	def __init__(self, sub=None, option=None):
		self.sub = sub
		self.option = option

	def select(self):
		if self.__checkOpt(True, True):
			if self.sub.lower() == "database":
				properties.update({"database": self.option})
			elif self.sub.lower() == "id":
				properties.update({"id": self.option})
			else:
				print(self.sub, "is an unknown sub command, you can type \"select\" database/id <value>")
				return False
		else:
			print("Missing parameter \"select\" <database/id?> <option?>")
			return(False)
		
	def show(self):
		if self.__checkOpt(True):
			if self.sub.lower() == "database":
				print(properties["database"])
			elif self.sub.lower() == "id":
				print(properties["id"])
			else:
				print(self.sub, "is an unknown sub command, you can type \"show\" database/id")
				return False			
		else:
			print("Missing parameter \"show\" <database/id?>")
	
	def listTables(self):
		if self.__checkOpt(True):
			None
		else:
			print(self.sub, "is an unknown sub command, you can type \"list\" authentication/register")

	def __checkOpt(self, sub: bool=False, option: bool=False):
		if sub is True and option is True:
			if not self.sub is None and not self.option is None:
				return True
		elif sub is True:
			if not self.sub is None:
				return True
		elif option is True:
			if not self.sub is None:
				return True
		else:
			return False

class Options:
	def __init__(self, option):
		self.option = option
		self.options = {
			"help": "Print information about command(s).",
			"select" : "Select database or id number.",
			"show" : "Show selected database or id number you have.",
			"list" : "List authentication or register tables.",
			"exit": "End this shell process and exit to main shell."
		}

	def options(self):
		return self.options

	def execOption(self, sub=None, option=None):
		opt = self.option.lower()
		if opt == "help":
			self.__help(sub)
		elif opt == "select":
			Shell(sub, option).select()
		elif opt == "show":
			Shell(sub).show()
		elif opt == "list":
			Shell(sub).list()
		elif opt == "exit":
			self.__exit()

	def __exit(self):
		print("Bye ( ͡° ͜ʖ ͡°)!")
		exit(True)

	def __help(self, sub):
		if sub == None:
			for opt in self.options:
				print(opt, "\t~>" ,self.options[opt]) 
		elif sub in self.options:
			print(sub, "\t~>", self.options[sub])
		else:
			print(sub, " is an unknown option, if you don't know which are that commands, you can type \"help\".")

while True:
	usrin = input(prompt)
	lex = shlex.split(usrin)

	try:
		lex[0]
	except IndexError:
		cmd = None
	else:
		cmd = lex[0]

	if not cmd is None and cmd.lower() in Options(None).options:
		try:
			lex[1]
		except IndexError:
			sub = None
		else:
			sub = lex[1]

		try:
			lex[2]
		except IndexError:
			option = None
		else:
			option = lex[2]

		Options(cmd.lower()).execOption(sub, option)
	else:
		if not cmd is None:
			print("Unknown option:", usrin)
		else:
			None