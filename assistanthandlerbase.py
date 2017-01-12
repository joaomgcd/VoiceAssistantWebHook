
import urllib
import json

class AssistantHandler(object):
    def __init__(self, action):
        self.action = action

    def shouldHandle(self, req):     
        result = req.get("result")
        if result is None:
            return False;
        action = result.get("action")
        if action != self.action:
            return False
        return True;

    def handle(self, parameters): 
        url = self.getUrl(parameters)
        result = None
        if url is not None:
            result = urllib.urlopen(url).read()
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
