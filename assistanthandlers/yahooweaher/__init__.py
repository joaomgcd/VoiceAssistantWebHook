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
