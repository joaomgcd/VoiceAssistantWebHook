
from google import AssistantHandlerGoogle
import json
import urllib
from abc import ABCMeta, abstractmethod

class AssistantHandlerGoogleFit(AssistantHandlerGoogle):
	__metaclass__ = ABCMeta

	def __init__(self,action):
		AssistantHandlerGoogle.__init__(self,action,"google_fit")    

	def getBaseUrl(self,parameters):
		return "https://www.googleapis.com/fitness/v1/"
		

	def getScopes(self):
		return ['https://www.googleapis.com/auth/fitness.activity.read','https://www.googleapis.com/auth/fitness.activity.write','https://www.googleapis.com/auth/fitness.location.read','https://www.googleapis.com/auth/fitness.location.write','https://www.googleapis.com/auth/fitness.body.read','https://www.googleapis.com/auth/fitness.body.write']