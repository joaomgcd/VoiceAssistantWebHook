#!/usr/bin/env python

import urllib
import json
import os
import imp

from flask import Flask
from flask import request
from flask import make_response
from assistanthandlerbase import AssistantHandler
from os import listdir


from os.path import isfile, join
mypath = "assistanthandlers"

onlyfiles = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(mypath)) for f in fn if f.endswith("__init__.py")]
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".py")]
#print(onlyfiles)
for f in onlyfiles:
    moduleName = f.replace("\\__init__.py","").replace("assistanthandlers\\","")
    imp.load_source( f.replace(".py",""), f)
#from assistanthandlers.assistanthandleryahooweather import AssistantHandlerYahooWeather

# Flask app should start in global layout
app = Flask(__name__)



assistantHandlerNames = [cls.__name__ for cls in vars()['AssistantHandler'].__subclasses__()]
assistanHandlerClasses = vars()['AssistantHandler'].__subclasses__()
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = None
    for assistanHandlerClass in assistanHandlerClasses:
        assistantHandler = assistanHandlerClass()
        if assistantHandler.shouldHandle(req):
            result = req.get("result")
            parameters = result.get("parameters")         
            res = assistantHandler.handle(parameters)

            break
            # print(res)
    if res is None:
        res = {}
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    #print(assistanHandlerClasses)
    print "Starting app on port %d" % port
    
    app.run(debug=False, port=port, host='0.0.0.0')
