
from google import AssistantHandlerGoogle
import json
import urllib
from abc import ABCMeta, abstractmethod

class AssistantHandlerGmail(AssistantHandlerGoogle):
	__metaclass__ = ABCMeta

	def __init__(self,action):
		AssistantHandlerGoogle.__init__(self,action,"gmail")    

	def getBaseUrl(self,parameters):
		return "https://www.googleapis.com/gmail/v1/users/"
		

	def getScopes(self):
		return ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.compose','https://www.googleapis.com/auth/gmail.modify','https://mail.google.com/']