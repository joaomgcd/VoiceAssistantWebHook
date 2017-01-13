from assistanthandlerbase import AssistantHandler
import urllib

class AssistantHandlerHelloName(AssistantHandler):
	def __init__(self):
		AssistantHandler.__init__(self,"helloname")

	def getBaseUrl(self,parameters):
		pass


	def getEndpoint(self,parameters):
		pass


	def getEndpointParameters(self,parameters):
		pass

	def getSpeech(self, parameters, data):
		return "Hello to you too " + parameters.get("name") + "!"
