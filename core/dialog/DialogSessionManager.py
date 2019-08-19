# -*- coding: utf-8 -*-
import copy
from typing import Optional, Dict

from paho.mqtt.client import MQTTMessage

from core.commons import commons
import core.base.Managers as managers
from core.base.Manager import Manager
from core.dialog.model.DialogSession import DialogSession


class DialogSessionManager(Manager):
	"""
	We need to handle the sessions for different reason. One of the main reason is to keep track of the speaker based on the
	wakeword model id that woke snips up. Since the topic for wakeword detection happens before a session is created we cannot
	track the session id in traditional ways. But fortunately, only one session at a time is allowed per site id so we can
	use this for pre tracking. Another one is to store the sessions data to avoid having to parse them again and again in
	every module calls
	"""

	NAME = 'DialogSessionManager'

	def __init__(self, mainClass):
		super().__init__(mainClass, self.NAME)

		managers.DialogSessionManager = self
		self._preSessions: Dict[str, DialogSession] = dict()
		self._sessions: Dict[str, DialogSession] = dict()
		self._terminatedSessions: Dict[str, DialogSession] = dict()
		self._revivePendingSessions: Dict[str, DialogSession] = dict()


	@property
	def sessions(self) -> dict:
		return self._sessions


	def preSession(self, siteId: str, user: str) -> DialogSession:
		"""
		Pre sessions hold the speaker based on the site id. They are deleted as soon as a session id
		is attributed to the related dialog
		:param siteId: int
		:param user: string
		"""
		session = DialogSession(siteId)
		session.user = user
		self._preSessions[siteId] = session
		return session


	def addSession(self, sessionId: str, message: MQTTMessage) -> DialogSession:
		"""
		Adds a session from an existing pre session. If the pre session doesn't exist
		it means the session was started programatically so we create a session
		:param sessionId: str
		:param message: dict
		"""
		siteId = commons.parseSiteId(message)
		if siteId not in self._preSessions.keys():
			session = DialogSession(siteId)
		else:
			session = self._preSessions.pop(siteId)

		session.extend(message, sessionId)

		self._sessions[sessionId] = session
		return session


	def addTempSession(self, sessionId: str, message: MQTTMessage) -> DialogSession:
		"""
		Adds a temporary session. This is usefull for sessions that are not
		Snips handeled and aren't ended
		:param sessionId: str
		:param message: dict
		"""
		siteId = commons.parseSiteId(message)
		if siteId not in self._preSessions.keys():
			session = DialogSession(siteId)
		else:
			session = self._preSessions.pop(siteId)

		session.extend(message, sessionId)

		self._sessions[sessionId] = session
		managers.ThreadManager.doLater(func=self._sessions.pop, interval=20, args=[sessionId])
		return session


	def removeSession(self, sessionId: str):
		if sessionId in self._sessions.keys():
			self._terminatedSessions[sessionId] = self._sessions.pop(sessionId)


	def getSession(self, sessionId: str) -> Optional[DialogSession]:
		if sessionId in self._sessions.keys():
			return self._sessions[sessionId]
		else:
			return None


	def getUser(self, sessionId: str) -> str:
		if sessionId in self._sessions:
			return self._sessions[sessionId].user
		else:
			self._logger.warning("[{}] Trying to get user from a session that doesn't exist".format(self.name))
			return 'unknown'


	def addPreviousIntent(self, sessionId: str, previousIntent: str):
		if not sessionId in self._sessions.keys():
			self._logger.warning('[{}] Was asked to add a previous intent but session was not found'.format(self.name))
			return

		session = self._sessions[sessionId]
		session.intentHistory.append(previousIntent)


	def planSessionRevival(self, session: DialogSession):
		self._revivePendingSessions[session.siteId] = session


	def onSessionStarted(self, session: DialogSession):
		if session.siteId in self._revivePendingSessions.keys():
			oldSession = self._revivePendingSessions[session.siteId]
			self._revivePendingSessions.pop(session.siteId)
			session.reviveOldSession(oldSession)