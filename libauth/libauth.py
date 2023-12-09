#!/usr/bin/env python3

import os
import sqlite3

class Auth:
	def __init__(self, database):
		self.database	= database
		self.__initdb()

	def isAuthenticated(self, uid):
		return None
	
	def inQueue(self, uid):
		return None

	def register(self, uid):
		return None

	def __initdb(self):
		# Database options,
		# int auth table we have user id and authentication level,
		# so the user id must be an string but why it's not integer?
		# because the user can be give an string yea, and the auth level
		# must be boolean, 0: authenticated, 1: banned.
		self.auth = """
			CREATE TABLE IF NOT EXISTS auth (
				id integer PRIMARY KEY,
				uid TEXT NOT NULL UNIQUE,
				authlvl BOOLEAN NOT NULL CHECK (authlvl IN (0, 1))
			);
		"""

		# Queue option, any user can be send a one register request,
		# and the admin can be authenticate it.
		self.queue = """
			CREATE TABLE IF NOT EXISTS queue (
				id integer PRIMARY KEY,
				uid TEXT NOT NULL UNIQUE				
			);
		"""

		try:
			self.conn = sqlite3.connect(self.database)
		except sqlite3.Error as err:
			print("Error occured while initilaizing the database: ", err)
		
		try:
			self.cursor = self.conn.cursor()
		except sqlite3.Error as err:
			print("Error occured while creating tables: ", err)
		finally:
			self.cursor.execute(self.auth)
			self.cursor.execute(self.queue)