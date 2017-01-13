
from assistanthandlerwithauth import AssistantHandlerWithAuth
import urllib
import json
import requests
import authutils
from abc import ABCMeta, abstractmethod

class AssistantHandlerWithAuthCode(AssistantHandlerWithAuth):
    __metaclass__ = ABCMeta

    def __init__(self, action, apiName):
        AssistantHandlerWithAuth.__init__(self,action, apiName)
    
    def handle(self, parameters): 
        url = self.getUrl(parameters)
        print "calling url " + url
        accessToken = authutils.getAccessToken(self.apiName)       
        result = requests.get(url, headers = {"Authorization": "Bearer " + accessToken})
        print("Result:")
        print result
        resultjson = result.json()
        return self.getResponse(self.getSpeech(parameters, resultjson))

