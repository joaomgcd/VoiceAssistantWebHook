from assistanthandlerbase import AssistantHandler
from jsondb import JsonDb
import arrow,datehelper


class AssistantHandlerHelloWorld(AssistantHandler):
	def __init__(self):
		AssistantHandler.__init__(self,"statetime")
		self.db=JsonDb()

	def getBaseUrl(self,parameters):
		pass

	def getEndpoint(self,parameters):
		pass

	def getEndpointParameters(self,parameters):
		pass

	def error(self):
		return "I am sorry,something went wrong"

	def getSpeech(self, parameters, data):
		a=[]
		src=parameters.get("src")
		dst=parameters.get("dest")
		srctime=self.db.get("phone/states/{}/exit".format(src))
		dsttime=self.db.get("phone/states/{}/enter".format(dst))
		if (not srctime) or (not dsttime):
			return self.error()
		diff=arrow.get(dsttime)-arrow.get(srctime)
		days=diff.days # Get Day 
		hours,reminder=divmod(diff.seconds,3600) # Get Hour 
		minutes,seconds=divmod(reminder,60) #
		if days>0:
			a.append("{} days".format(days))
		if hours>0:
			a.append("{} hours".format(hours))
		if minutes>0:
			a.append("{} minutes".format(minutes))
		if seconds>0:
			a.append("{} seconds".format(seconds))
		time=datehelper.toLocal(arrow.get(dsttime))
		if len(a)==0:
			return "You reached {} the moment you left {} {}".format(dst,src,time.humanize())
		return "You reached {1} at {3}, It took {0} for you to reach {1} from {2}".format(" ".join(a),dst,src,time.format("hh:mm a"))
