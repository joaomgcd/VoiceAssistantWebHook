from assistanthandlerbase import AssistantHandler
import urllib

class AssistantHandlerHelloName(AssistantHandler):
    def __init__(self):
        AssistantHandler.__init__(self,"helloname")

    def getUrl(self, parameters):
        return None

    def getSpeech(self, parameters, data):
        return "Hello to you too " + parameters.get("name") + "!"
