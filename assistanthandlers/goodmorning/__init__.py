from assistanthandlerbase import AssistantHandler
import urllib
import arrow
import os

class AssistantHandlerHelloName(AssistantHandler):
	def __init__(self):
		AssistantHandler.__init__(self,"goodmorning")
		self.time=arrow.now(os.getenv("TIMEZONE"))
	def getBaseUrl(self,parameters):
		pass


	def getEndpoint(self,parameters):
		pass


	def getEndpointParameters(self,parameters):
		pass

	def getSpeech(self, parameters, data):
		if self.time.hour>0 and self.time.hour<=11:
			return "good morning sir"
		elif self.time.hour>=12 and self.time.hour<=16:
			return "good afternoon sir"
		elif self.time.hour>16 and self.time.hour<=20:
			return "good evening sir"
		else:
			return "good night sir"
