
from googlecalendar import AssistantHandlerGoogleCalendar

from utils import current_milli_time
import json

class AssistantHandlerGoogleCalendarAdd(AssistantHandlerGoogleCalendar):
	def __init__(self):
		AssistantHandlerGoogleCalendar.__init__(self,"googlecalendaradd")    
	
	def getHttpMethod(self):
		return "POST"

	def	getEndpoint(self,parameters):
		return "calendars/primary/events/quickAdd"

	def getEndpointParameters(self,parameters):
		return {"text":parameters["text"],"sendNotifications":True}

	def getSpeech(self, parameters, data):		
		return "Added calendar appointment with the text \"" + data["summary"] + "\" which will start at " + data["start"]["dateTime"] + " and end at " + data["end"]["dateTime"]
	
