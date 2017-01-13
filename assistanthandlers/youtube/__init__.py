
from assistanthandlerwithauthcode import AssistantHandlerWithAuthCode
import json
import urllib
from abc import ABCMeta, abstractmethod

class AssistantHandlerYouTube(AssistantHandlerWithAuthCode):
	__metaclass__ = ABCMeta

	def __init__(self,action):
		AssistantHandlerWithAuthCode.__init__(self,action,"youtube")    

	def getBaseUrl(self,parameters):
		return "https://content.googleapis.com/youtube/v3/"
		

	

