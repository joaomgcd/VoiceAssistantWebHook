
from google import AssistantHandlerGoogle
import json
import urllib
from abc import ABCMeta, abstractmethod

class AssistantHandlerGoogleCalendar(AssistantHandlerGoogle):
	__metaclass__ = ABCMeta

	def __init__(self,action):
		AssistantHandlerGoogle.__init__(self,action,"google_calendar")    

	def getBaseUrl(self,parameters):
		return "https://www.googleapis.com/calendar/v3/"
		

	def getScopes(self):
		return ['https://www.googleapis.com/auth/calendar']