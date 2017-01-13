
from youtube import AssistantHandlerYouTube
import json

class AssistantHandlerYouTubeSubscribers(AssistantHandlerYouTube):
	def __init__(self):
		AssistantHandlerYouTube.__init__(self,"youtubesubscribers")    

	def	getEndpoint(self,parameters):
		return "channels"

	def getEndpointParameters(self,parameters):
		return {"mine":True,"part":"statistics"}

	def getSpeech(self, parameters, data):
		return "You have " + data["items"][0]["statistics"]["subscriberCount"] + " subscribers on YouTube"
