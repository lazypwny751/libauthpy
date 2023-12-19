#!/usr/bin/env python3

import os
import sqlite3
from sqlite3 import Error

class Auth:
	def __init__(self, database):
		self.database	= database
		self.__initdb()

	# Authenticate the user.
	def authenticate(self, uid, authlvl=True):
		if not isinstance(authlvl, bool):
			# Fatal error, the authentication level parameter (authlvl) can be bool.
			raise ValueError(f"\"authlvl\" can not be {authlvl}, can be \"boolean\" (True or False) ")

		# Variable translation for insert the data to database
		if authlvl:
			# True
			realauthlvl = 0
		else:
			# False
			realauthlvl = 1
	
		if not self.cursor.execute(self.authQuery, (uid,)).fetchall():
			try:
				self.cursor.execute(self.authInsert, (uid, realauthlvl))
				self.conn.commit()
			except sqlite3.Error as err:
				print(f"Error occured while inserting \"{uid}\" and \"{authlvl}\" to table \"auth\": ", err)
				return(False)
			finally:
				return True
		else:
			return True

	# Is the user has registered before to auth table?
	def inAuthentication(self, uid):
		if self.cursor.execute(self.authBanQuery, (uid,)).fetchall():
			return True
		else:
			return False

	# Is the user allowed?
	def isAuthenticated(self, uid):
		if self.cursor.execute(self.authBanQuery, (uid,)).fetchall() and not self.cursor.execute(self.authBanQuery, (uid,)).fetchall()[0][0] == 1:
			return True
		else:
			return False

	
	def listAuthentication(self):
		return self.cursor.execute(self.listAuthQuery).fetchall()

	def dropAuthentication(self, uid):
		if self.inAuthentication(uid):
			try:
				self.cursor.execute(self.authDelete, (self.cursor.execute(self.authId, (uid,)).fetchall()[0][0],))
				self.conn.commit()
			except sqlite3.Error as err:
				raise ValueError("Could not drop data from auth: ", err)
				return False
			finally:
				return True
		else:
			return True

	# return: bool, true (inserted or already inserted data), false (fatal error).
	def register(self, uid):
		if not self.cursor.execute(self.queueQuery, (uid,)).fetchall():
			try:
				self.cursor.execute(self.queueInsert, (uid,))
				self.conn.commit()
			except sqlite3.Error as err:
				# Fatal
				print(f"Error occured while inserting \"{uid}\" to table \"queue\": ", err)
				return(False)
			finally:
				return True
		else:
			# Already registered.
			return True

	# return: bool, true is (yes it's in) and false (no it's not in).
	def inQueue(self, uid):
		if self.cursor.execute(self.queueQuery, (uid,)).fetchall():
			# yes it's in queue
			return True
		else:
			# nope
			return False

	def listRegister(self):
		return self.cursor.execute(self.listRegisterQuery).fetchall()

	def dropRegister(self, uid):
		if self.inQueue(uid):
			try:
				self.cursor.execute(self.queueDelete, (self.cursor.execute(self.queueId, (uid,)).fetchall()[0][0],))
				self.conn.commit()
			except sqlite3.Error as err:
				raise ValueError("Could not drop data from queue: ", err)
				return False
			finally:
				return True
		else:
			return True

	def __initdb(self):
		# Database options,
		# int auth table we have user id and authentication level,
		# so the user id must be an string but why it's not integer?
		# because the admin/user can be give an string yea, and the auth level
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

		# user id is in Queue?.
		self.queueQuery = "SELECT * FROM queue WHERE uid = ?"

		# Insert into user id to queue for registration. 
		self.queueInsert = "INSERT INTO queue (uid) VALUES (?)"

		# Get real data id of queue element.
		self.queueId = "SELECT id FROM queue WHERE uid = ?"

		# Check if user is there or not for authentication table. 
		self.authQuery = "SELECT * FROM auth WHERE uid = ?"

		# List all content of queue.
		self.listRegisterQuery = "SELECT * FROM queue"

		# Delete queue data by real id.
		self.queueDelete = "DELETE FROM queue WHERE id = ?"

		# is the member has banned or not?
		self.authBanQuery = "SELECT authlvl FROM auth WHERE uid = ?"

		# Insert into user and authentication level to table.
		self.authInsert = "INSERT INTO auth (uid, authlvl) VALUES (?, ?)"

		# Get real data id of auth element.
		self.authId = "SELECT id FROM auth WHERE uid = ?"

		# List all content of auth.
		self.listAuthQuery = "SELECT * FROM auth"

		# Delete auth data by real id.
		self.authDelete = "DELETE FROM auth WHERE id = ?"

		try:
			self.conn = sqlite3.connect(self.database, check_same_thread=False)
		except sqlite3.Error as err:
			raise ValueError("Error occured while initilaizing the database!")
			return(False)

		try:
			self.cursor = self.conn.cursor()
		except sqlite3.Error as err:
			print("Error occured while creating tables: ", err)
			return(False)
		finally:
			self.cursor.execute(self.auth)
			self.cursor.execute(self.queue)