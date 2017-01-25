
from googlecalendar import AssistantHandlerGoogleCalendar

from utils import current_milli_time
import datetime as dt
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
		formatFromGoogle = '%Y-%m-%dT%H:%M:%SZ'
		formatForOutput = '%Y-%m-%d %H:%M'
		start = dt.datetime.strptime(data["start"]["dateTime"], formatFromGoogle).strftime(formatForOutput)
		end = dt.datetime.strptime(data["end"]["dateTime"], formatFromGoogle).strftime(formatForOutput)
		return "Added calendar appointment with the description \"" + data["summary"] + "\" starting on " + start
	
