
import os
from assistanthandlerbase import AssistantHandler
from assistanthandlerwithauthcode import AssistantHandlerWithAuthCode
from os.path import isfile, join
import imp
import inspect

mypath = "assistanthandlers"
onlyfiles = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(mypath)) for f in fn if f.endswith("__init__.py")]
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".py")]
#print(onlyfiles)
for f in onlyfiles:
	moduleName = f.replace("\\__init__.py","").replace("assistanthandlers\\","")
	imp.load_source( moduleName, f)

def itersubclasses(cls, _seen=None):  
	
	if not isinstance(cls, type):
		raise TypeError('itersubclasses must be called with '
						'new-style classes, not %.100r' % cls)
	if _seen is None: _seen = set()
	try:
		subs = cls.__subclasses__()
	except TypeError: # fails only when cls is type
		subs = cls.__subclasses__(cls)
	for sub in subs:
		isAbstract = inspect.isabstract(sub)
		#print str(sub) + "is abstract: " + str(isAbstract)
		if sub not in _seen:
			_seen.add(sub)
			if not isAbstract:
				print "Loading Handler: " + str(sub)
				yield sub
			for sub in itersubclasses(sub, _seen):
				yield sub	

#assistanHandlerClasses = vars()['AssistantHandler'].__subclasses__()
assistanHandlerClasses = [cls for cls in itersubclasses(AssistantHandler)]
#assistanHandlerClasses.remove(AssistantHandlerWithAuthCode)
#print assistanHandlerClasses
def getClass(name):
	for assistanHandlerClass in assistanHandlerClasses:
		if assistanHandlerClass.__name__ == name:
			return assistanHandlerClass
	return None
