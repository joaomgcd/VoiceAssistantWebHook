from assistanthandlerbase import AssistantHandler

class AssistantHandlerHelloWorld(AssistantHandler):
	def __init__(self):
		AssistantHandler.__init__(self,"helloworld")


	def getBaseUrl(self,parameters):
		pass


	def getEndpoint(self,parameters):
		pass


	def getEndpointParameters(self,parameters):
		pass

	def getSpeech(self, parameters, data):
		return "Hello World!"
