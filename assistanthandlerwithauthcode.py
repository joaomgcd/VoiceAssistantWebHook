
from assistanthandlerwithauth import AssistantHandlerWithAuth
import urllib
import json
import requests
import authutils
from abc import ABCMeta, abstractmethod

class AssistantHandlerWithAuthCode(AssistantHandlerWithAuth):
	__metaclass__ = ABCMeta
	httpMethodMap = {"GET" : requests.get, "POST": requests.post, "PUT": requests.put, "DELETE": requests.delete}
	def __init__(self, action, apiName):
		AssistantHandlerWithAuth.__init__(self,action, apiName)
	
	def handle(self, parameters):
		resultjson = None
		if self.shouldCallUrl(parameters):
			url = self.getUrl(parameters)
			print "calling url " + url
			accessToken = authutils.getAccessToken(self.apiName)   
			if accessToken is None:
				raise ValueError(self.getApiName() + ' is not authorized. Please visit /static/auth.html to authorize')
			headers = {"Authorization": "Bearer " + accessToken}
			postData = self.getPostData(parameters)
			if postData is not None:
				postData = json.dumps(postData, indent=4)
				headers['content-type'] = 'application/json'
				print "postData: " + postData
			
			httpMethod = self.getHttpMethod()
			if httpMethod is None:
				if postData is None:
					result = requests.get(url, headers = headers)
				else:
					result = requests.post(url, data = postData, headers = headers)
			else:
				print "Using custom HTTP method: " + httpMethod
				requestMethod = self.httpMethodMap[httpMethod]
				result = requestMethod(url, data = postData, headers = headers)
			print("Result:")
			print result
			resultjson = result.json()
		return self.getResponse(self.getSpeech(parameters, resultjson))

	@abstractmethod
	def getAuthUrl(self):
		pass

	@abstractmethod
	def getTokenUrl(self):
		pass

	@abstractmethod
	def getScopes(self):
		pass 

	def getHttpMethod(self):
		pass 