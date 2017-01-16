
import urllib
import json
import requests

from abc import ABCMeta, abstractmethod

class AssistantHandler(object):
	__metaclass__ = ABCMeta


	def getUrl(self,parameters):
		url = self.getBaseUrl(parameters)
		endpoint = self.getEndpoint(parameters)
		if endpoint is not None:
			url = url + endpoint
		endpointParameters = self.getEndpointParameters(parameters)
		if endpointParameters is not None:
			url = url + "?" + urllib.urlencode(endpointParameters)
		return url

	@abstractmethod
	def getBaseUrl(self,parameters):
		pass

	@abstractmethod
	def getEndpoint(self,parameters):
		pass

	@abstractmethod
	def getEndpointParameters(self,parameters):
		pass

	def getPostData(self,parameters):
		pass


	def __init__(self, action):
		self.action = action

	def shouldHandle(self, req, parameters):	 
		result = req.get("result")
		if result is None:
			return False;
		action = result.get("action")
		if action != self.action:
			return False
		return True;

	def shouldCallUrl(self, parameters):
		return True

	def handle(self, parameters): 
		data = None
		if self.shouldCallUrl(parameters):
			url = self.getUrl(parameters)
			result = None
			if url is not None:
				postData = self.getPostData(parameters)
				print "postData: " + str(postData)
				print "url: " + url
				if postData is None:
					result = urllib.urlopen(url).read()
				else:
					result = requests.post(url, json = postData, headers = {"Content-Type":"application/json"}).text
			print("Result:")
			print(result)
			data = None
			if result is not None:
				data = json.loads(result)
		return self.getResponse(self.getSpeech(parameters, data))

	def getResponse(self,speech):
		return {
			"speech": speech,
			"displayText": speech,
			# "data": data,
			# "contextOut": [],
			"source": "joaomgcd_apiai_webhook"
		}
