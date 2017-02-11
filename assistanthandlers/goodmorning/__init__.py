from assistanthandlerbase import AssistantHandler
import urllib
import arrow


class AssistantHandlerHelloName(AssistantHandler):
	def __init__(self):
		AssistantHandler.__init__(self,"goodmorning")
		self.time=arrow.now()

	def getBaseUrl(self,parameters):
		pass


	def getEndpoint(self,parameters):
		pass


	def getEndpointParameters(self,parameters):
		pass

	def getSpeech(self, parameters, data):
		if self.time.hour>0 and self.time.hour<=11:
			return "good morning"
		elif self.time.hour>=12 and self.time.hour<=16:
			return "good afternoon"
		elif self.time.hour>16 and self.time.hour<=20:
			return "good evening"
		else:
			return "good night"
