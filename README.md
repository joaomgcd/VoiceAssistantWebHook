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
```python
from assistanthandlerbase import AssistantHandler

class AssistantHandlerHelloWorld(AssistantHandler):
    def __init__(self):
        AssistantHandler.__init__(self,"helloworld")

    def getUrl(self, parameters):
        return None

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

    def getUrl(self, parameters):
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = self.makeYqlQuery(parameters)
        if yql_query is None:
            return {}
        yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
        return yql_url

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
You can see how the **getUrl** method returns an URL that will get some weather results for the parameter called **geo-city**
The  **getSpeech** method parses the data out of the results and returns a string with today's weather for the city in the parameter.


# How do I use this with API.AI?
- Click this button: [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
- After your app is created in Heroku open [API.AI](https://api.ai/), go to the Fullfillment tab and paste your Webhook URL there. Your Webhook URL is your app's name followed by .herokuapp.com/webhook For example, if your app's name is **superduperapp** your URL will be **https://superduperapp.herokuapp.com/webhook**
- In the API.AI intents that you want to be handled by the webhook enable the **Use webhook** checkbox in the **Fulfillment** section of the intent
- To test it out try creating an Hello World intent in API.AI that has the **helloworld** action and see if you get back the **Hello World** speech.