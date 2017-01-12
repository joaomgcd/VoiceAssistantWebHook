from assistanthandlerbase import AssistantHandler

class AssistantHandlerHelloWorld(AssistantHandler):
    def __init__(self):
        AssistantHandler.__init__(self,"helloworld")

    def getUrl(self, parameters):
        return None

    def getSpeech(self, parameters, data):
        return "Hello World!"
