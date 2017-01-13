
from assistanthandlerwithauthcode import AssistantHandlerWithAuthCode
from abc import ABCMeta, abstractmethod

class AssistantHandlerSpotify(AssistantHandlerWithAuthCode):
	__metaclass__ = ABCMeta

	def __init__(self,action):
		AssistantHandlerWithAuthCode.__init__(self,action,"spotify")    
	
	def getBaseUrl(self,parameters):
		return "https://api.spotify.com/v1/"


	def getAuthUrl(self):
		return "https://accounts.spotify.com/authorize"


	def getTokenUrl(self):
		return "https://accounts.spotify.com/api/token"        
	
	def getScopes(self):
		return ['playlist-read-private','playlist-read-collaborative','playlist-modify-public','playlist-modify-private','streaming','user-follow-modify','user-follow-read','user-library-read','user-library-modify','user-read-private','user-read-birthdate','user-read-email']