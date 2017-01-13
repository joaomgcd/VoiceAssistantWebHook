
from googlefit import AssistantHandlerGoogleFit

from utils import current_milli_time
import json

class AssistantHandlerGoogleFitListSessions(AssistantHandlerGoogleFit):
	def __init__(self):
		AssistantHandlerGoogleFit.__init__(self,"googlefitlistsessions")    


	def	getEndpoint(self,parameters):
		return "users/me/sessions"

	def getEndpointParameters(self,parameters):
		return None

	def getSpeech(self, parameters, data):
		now = current_milli_time()
		aWeekAgo = now - 604800000L
		sessionsFromLastWeek = [session for session in data["session"] if long(session["startTimeMillis"]) > aWeekAgo]
		totalTime = sum([long(session["endTimeMillis"]) - long(session["startTimeMillis"])  for session in sessionsFromLastWeek])
		totalTimeMinutes = totalTime / 1000 / 60
		return "This past week you worked out for a total of " + str(totalTimeMinutes) + " minutes"
