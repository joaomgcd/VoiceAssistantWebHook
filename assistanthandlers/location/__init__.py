#!/usr/bin/python
# -*- coding: utf-8 -*-
from assistanthandlerbase import AssistantHandler
import urllib
import arrow
import os


class AssistantHandlerHelloName(AssistantHandler):

    def __init__(self):
        AssistantHandler.__init__(self, 'runtask')
        self.time = arrow.now(os.getenv('TIMEZONE'))

    def getBaseUrl(self, parameters):
        pass

    def getEndpoint(self, parameters):
        pass

    def getEndpointParameters(self, parameters):
        pass

    def getSpeech(self, parameters, data):
        dur=parameters.get('duration')
        if dur:
            j=json.loads(dur)
            
