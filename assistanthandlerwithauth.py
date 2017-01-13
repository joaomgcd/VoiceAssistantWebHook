
from assistanthandlerbase import AssistantHandler
import urllib
import json
import requests
import authutils
from abc import ABCMeta, abstractmethod

class AssistantHandlerWithAuth(AssistantHandler):
	__metaclass__ = ABCMeta

	def __init__(self, action, apiName):
		AssistantHandler.__init__(self,action)
		self.apiName = apiName

	def getApiName(self):
		return self.apiName