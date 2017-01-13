from spotify import AssistantHandlerSpotify

class AssistantHandlerSpotifyUser(AssistantHandlerSpotify):
	def __init__(self):
		AssistantHandlerSpotify.__init__(self,"spotifyuser")	

	def	getEndpoint(self,parameters):
		return "me"

	def getEndpointParameters(self,parameters):
		return None

	def getSpeech(self, parameters, data):
		return "Your name on Spotify is " + data["display_name"] + " and you have " + str(data["followers"]["total"]) + " followers"
