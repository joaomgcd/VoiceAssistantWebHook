#!/usr/bin/python
# -*- coding: utf-8 -*-
from assistanthandlerbase import AssistantHandler
import urllib
import arrow
import os


class AssistantHandlerHelloName(AssistantHandler):

    def __init__(self):
        AssistantHandler.__init__(self, 'location.get')
        
    def getBaseUrl(self, parameters):
        pass

    def getEndpoint(self, parameters):
        pass

    def getEndpointParameters(self, parameters):
        pass

    def getSpeech(self, parameters, data):
        timezone = os.getenv("TIMEZONE")
        time=arrow.get(parameters.get("statetime")).to(str(timezone)).humanize()
        state=parameters.get("location")
        return "Sriram is at {} since {}".format(state,time)
