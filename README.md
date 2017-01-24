# Voice Assistant Webhook

This is an easy way to create a Webhook to use with API.AI.

You'll be able to do stuff like this:

[![Testing Voice Assistant Webhook](https://img.youtube.com/vi/4SDeHLhWpAk/0.jpg)](https://www.youtube.com/watch?v=4SDeHLhWpAk)

The best way to create your custom interactions with API.AI on Android is by using [AutoVoice Natural Language](https://play.google.com/store/apps/details?id=com.joaomgcd.autovoice). At this time the natural language features are still in beta, so get that [here](https://joaoapps.com/beta-testing/) to give it a try.

You can use this to allow API.AI to access other APIs. Included is an example that gets the current weather from the Yahoo Weather API.

You start by creating an intent in API.AI and then create a handler for that intent in the webhook to make it do whatever you want.

For example, you could create an intent that would get the current value for your favorite stock or what the latest movie releases are. If you can access an API you can use it with API.AI :)

More info about Api.ai webhooks could be found here:
[Api.ai Webhook](https://docs.api.ai/docs/webhook)

# How do I use this with API.AI?
- Click this button: [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
- After your app is created in Heroku open [API.AI](https://api.ai/), go to the Fullfillment tab and paste your Webhook URL there. Your Webhook URL is your app's name followed by .herokuapp.com/webhook For example, if your app's name is **superduperapp** your URL will be **https://superduperapp.herokuapp.com/webhook**
- Install the PostgreSQL add-on on Heroku [here](https://elements.heroku.com/addons/heroku-postgresql).
- (Optional) If you want to use APIs where you need authentication visit the [Auth Page](static/auth.html) to login with your user. For example if your app's name is **superduperapp** your auth URL will be **https://superduperapp.herokuapp.com/static/auth.html**
- In the API.AI intents that you want to be handled by the webhook enable the **Use webhook** checkbox in the **Fulfillment** section of the intent
- To test it out try creating an Hello World intent in API.AI that has the **helloworld** action, enable the webhook option, test it out and see if you get back the **Hello World** speech.
- To easily edit the code you can use Heroku's Dropbox integration. It'll create a folder in your dropbox for you where you can edit the code and deploy it back to your Heroku app. Look for this option in the **Deploy** tab in your Heroku dashboard.

# How do I add my own services?
You create a new folder in the assistanthandlers folder, and in that folder a file with the name \_\_init\_\_.py
You then create a subclass of AssistantHandler with **getBaseUrl**, **getEndpoint**, **getEndpointParameters** and **getSpeech** methods.
This class should have an empty constructor and it should call the superclass constructor setting the handler's action
You can look at the existing handlers to get an idea how it works

Here's a very basic example:
```python
from assistanthandlerbase import AssistantHandler

class AssistantHandlerHelloWorld(AssistantHandler):
	def __init__(self):
		AssistantHandler.__init__(self,"helloworld")

	def getBaseUrl(self,parameters):
		pass

	def getEndpoint(self,parameters):
		pass

	def getEndpointParameters(self,parameters):
		pass

	def getSpeech(self, parameters, data):
		return "Hello World!"
```
This handler is triggered when the API.AI command's action is "helloworld"
It simply returns the static string "Hello World!" as the speech response.

Here's a more complex example:

```python
from assistanthandlerbase import AssistantHandler
import urllib
import json

class AssistantHandlerYahooWeather(AssistantHandler):
	def __init__(self):
		AssistantHandler.__init__(self,"yahooWeatherForecast")
	
	def getBaseUrl(self,parameters):
		return "https://query.yahooapis.com/v1/public/"

	def getEndpoint(self,parameters):
		return "yql"

	def getEndpointParameters(self,parameters):
		return {"q":self.makeYqlQuery(parameters),"format":"json"}

	def makeYqlQuery(self, parameters):
		city = parameters.get("geo-city")
		if city is None:
			return None

		return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"

	def getSpeech(self, parameters, data):
		query = data.get('query')
		if query is None:
			return "No query"

		result = query.get('results')
		if result is None:
			return "No results"

		channel = result.get('channel')
		if channel is None:
			return "No channel"

		item = channel.get('item')
		location = channel.get('location')
		units = channel.get('units')
		if (location is None) or (item is None) or (units is None):
			return "No location or item or units"

		condition = item.get('condition')
		if condition is None:
			return "No condition"

		# print(json.dumps(item, indent=4))

		speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
				 ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

		print("Response:")
		print(speech)

		return speech

```
You can see how the **getBaseUrl** method returns the base URL for the yahoo query API, the **getEndpoint** method returns the **yql** endpoint and the **getEndpointParameters** method returns the query that will get some weather results for the parameter called **geo-city**
The  **getSpeech** method parses the data out of the results and returns a string with today's weather for the city in the parameter.

# Handler with OAuth 2

## Attach Database
To manage authentication you need to be able to store persistent data. To do that install the [PostgreSQL Add-On](https://elements.heroku.com/addons/heroku-postgresql) and attach it to your app in Heroku. After installing the add-on you can use the special authentication handlers 

## Use Special Handler
You can use the **AssistantHandlerWithAuthCode** class as a base for a handler that supports **OAuth 2**. Take a look at the **AssistantHandlerSpotifyUser** class as an example:

```python


from assistanthandlerwithauthcode import AssistantHandlerWithAuthCode
from abc import ABCMeta, abstractmethod

class AssistantHandlerSpotify(AssistantHandlerWithAuthCode):
	__metaclass__ = ABCMeta

	def __init__(self,action):
		AssistantHandlerWithAuthCode.__init__(self,action,"spotify")    
	
	def getBaseUrl(self,parameters):
		return "https://api.spotify.com/v1/"


	def getAuthUrl(self):
		return "https://accounts.spotify.com/authorize"


	def getTokenUrl(self):
		return "https://accounts.spotify.com/api/token"        
	
	def getScopes(self):
		return ['playlist-read-private','playlist-read-collaborative','playlist-modify-public','playlist-modify-private','streaming','user-follow-modify','user-follow-read','user-library-read','user-library-modify','user-read-private','user-read-birthdate','user-read-email']
        
from spotify import AssistantHandlerSpotify

class AssistantHandlerSpotifyUser(AssistantHandlerSpotify):
	def __init__(self):
		AssistantHandlerSpotify.__init__(self,"spotifyuser")	

	def	getEndpoint(self,parameters):
		return "me"

	def getEndpointParameters(self,parameters):
		return None

	def getSpeech(self, parameters, data):
		return "Your name on Spotify is " + data["display_name"] + " and you have " + str(data["followers"]["total"]) + " followers"

```
Here you can see that there's a base **AssistantHandlerSpotify** that defines the base properties for the Spotify API like the base URL for the API calls, the auth URLs and the auth scopes it needs. Then you have an implementation of an endpoint with the **AssistantHandlerSpotifyUser** which gets user data and returns it as speech.
To be able to use these you need to use the [Auth Page](static/auth.html) to enter the API's details and sign-in with your user.

# IMPORTANT: SUBJECT TO CHANGE
The plugin structure for this is not final and could change at any moment, so be aware of that. 
