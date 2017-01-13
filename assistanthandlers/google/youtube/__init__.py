
from google import AssistantHandlerGoogle
import json
import urllib
from abc import ABCMeta, abstractmethod

class AssistantHandlerYouTube(AssistantHandlerGoogle):
	__metaclass__ = ABCMeta

	def __init__(self,action):
		AssistantHandlerGoogle.__init__(self,action,"youtube")    

	def getBaseUrl(self,parameters):
		return "https://content.googleapis.com/youtube/v3/"
		

	def getScopes(self):
		return ['https://www.googleapis.com/auth/youtube']