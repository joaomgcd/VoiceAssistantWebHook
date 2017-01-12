# Voice Assistant Webhook

This is an easy way to create a Webhook to use with API.AI.

More info about Api.ai webhooks could be found here:
[Api.ai Webhook](https://docs.api.ai/docs/webhook)

# Deploy to:
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# How do I add my own services?
You create a new folder in the assistanthandlers folder, and in that folder a file with the name __init__.py
You then create a subclass of AssistantHandler with getUrl and getSpeech methods.
This class should have an empty constructor and it should call the superclass constructor setting the handler's action
You can look at the existing handlers to get an idea how it works

Here's a very basic example:

	from assistanthandlerbase import AssistantHandler

	class AssistantHandlerHelloWorld(AssistantHandler):
	    def __init__(self):
	        AssistantHandler.__init__(self,"helloworld")

	    def getUrl(self, parameters):
	        return None

	    def getSpeech(self, parameters, data):
	        return "Hello World!"

This handler is triggered when the API.AI command's action is "helloworld"
It simply returns the static string "Hello World!" as the speech response.