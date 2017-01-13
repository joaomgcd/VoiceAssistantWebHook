
from assistanthandlerwithauthcode import AssistantHandlerWithAuthCode
from abc import ABCMeta, abstractmethod

class AssistantHandlerSpotify(AssistantHandlerWithAuthCode):
	__metaclass__ = ABCMeta

	def __init__(self,action):
		AssistantHandlerWithAuthCode.__init__(self,action,"spotify")    
	
	def getBaseUrl(self,parameters):
		return "https://api.spotify.com/v1/"

