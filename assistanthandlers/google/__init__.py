
from assistanthandlerwithauthcode import AssistantHandlerWithAuthCode
import json
import urllib
from abc import ABCMeta, abstractmethod

class AssistantHandlerGoogle(AssistantHandlerWithAuthCode):
	__metaclass__ = ABCMeta

	def __init__(self,action, apiName):
		AssistantHandlerWithAuthCode.__init__(self,action,apiName)    

	def getAuthUrl(self):
		return "https://accounts.google.com/o/oauth2/auth"


	def getTokenUrl(self):
		return "https://accounts.google.com/o/oauth2/token"   
	

